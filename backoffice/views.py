from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from datetime import datetime, timedelta
from functools import wraps
from decimal import Decimal
import logging

from .models import Reservation, UserProfile, ReservationAuditLog
from .forms import ReservationForm, UserProfileForm
from .currency_rates import EXCHANGE_RATES
from .email_service import BanbasEmailService
from resort.models import Contact


def admin_required(view_func):
    """Decorator to ensure only admin users can access a view"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this area.')
            return redirect('backoffice:login')
        
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No user profile found.')
            return redirect('backoffice:dashboard')
        
        if profile.role != 'admin':
            # Security logging
            logger = logging.getLogger('security')
            logger.warning(f'Unauthorized user management access attempt by {request.user.username} (role: {profile.role}) to {request.path}')
            
            messages.error(request, f'Access denied: User management requires administrative privileges. Your role: {profile.get_role_display()}')
            return redirect('backoffice:dashboard')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class RoleRequiredMixin:
    """Mixin to require specific roles for access"""
    required_role = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backoffice:login')
        
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("Access denied: No role assigned")
        
        if self.required_role and profile.role != self.required_role:
            return HttpResponseForbidden("Access denied: Insufficient permissions")
        
        return super().dispatch(request, *args, **kwargs)


class ViewerAllowedMixin:
    """Mixin for views that viewers can access (read-only)"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this area.')
            return redirect('backoffice:login')
        
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No user profile found.')
            return redirect('backoffice:dashboard')
        
        # Allow viewer, agent, and admin roles
        if profile.role not in ['viewer', 'agent', 'admin']:
            messages.error(request, f'Access denied: Invalid role. Your role: {profile.get_role_display()}')
            return redirect('backoffice:dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class AgentRequiredMixin(ViewerAllowedMixin):
    """Mixin for views that require agent or admin access"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this area.')
            return redirect('backoffice:login')
        
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No user profile found.')
            return redirect('backoffice:dashboard')
        
        # Allow only agent and admin roles
        if profile.role not in ['agent', 'admin']:
            messages.error(request, f'Access denied: Agent or Admin role required. Your role: {profile.get_role_display()}')
            return redirect('backoffice:dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    """Strict admin-only access mixin with comprehensive security checks"""
    required_role = 'admin'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this area.')
            return redirect('backoffice:login')
        
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No user profile found. Contact administrator.')
            return redirect('backoffice:dashboard')
        
        # Strict admin role check
        if profile.role != 'admin':
            # Log the access attempt for security auditing
            import logging
            logger = logging.getLogger('security')
            logger.warning(f'Unauthorized access attempt by {request.user.username} (role: {profile.role}) to admin-only view: {request.path}')
            
            messages.error(request, f'Access denied: Administrative privileges required. Your role: {profile.get_role_display()}')
            return redirect('backoffice:dashboard')
        
        # Additional security check for user management
        if 'user' in request.resolver_match.url_name:
            if not profile.can_edit_reservations():  # Admin check method
                messages.error(request, 'Access denied: User management requires full administrative privileges.')
                return redirect('backoffice:dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'backoffice/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user profile
        try:
            profile = self.request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
        
        context['user_profile'] = profile
        
        # Basic stats available to all users
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        
        context['stats'] = {
            'total_reservations': Reservation.objects.count(),
            'recent_reservations': Reservation.objects.filter(created_at__date__gte=last_30_days).count(),
            'current_occupancy': Reservation.objects.filter(
                arrival_date__lte=today,
                departure_date__gte=today
            ).aggregate(rooms=Sum('number_of_rooms'))['rooms'] or 0,
            'total_inquiries': Contact.objects.count(),
        }
        
        # Revenue data (admin only) with explicit currency selection and conversion
        if profile and profile.can_view_revenue():
            allowed_currencies = ['NRS', 'USD', 'INR', 'EUR']
            selected_currency = self.request.GET.get('currency')
            if selected_currency not in allowed_currencies:
                existing = list(Reservation.objects.values_list('payment_currency', flat=True).distinct())
                selected_currency = existing[0] if existing else 'USD'
            context['selected_currency'] = selected_currency
            context['available_currencies'] = allowed_currencies
            
            # Prepare Decimal-based rates map to avoid float precision issues
            rates = {code: Decimal(str(rate)) for code, rate in EXCHANGE_RATES.items()}
            
            def convert_amount(amount_dec: Decimal, from_cur: str, to_cur: str) -> Decimal:
                if not amount_dec:
                    return Decimal('0')
                if from_cur == to_cur:
                    return amount_dec
                # Convert to NRS, then to target
                amount_in_nrs = amount_dec / rates[from_cur]
                return (amount_in_nrs * rates[to_cur]).quantize(Decimal('0.01'))
            
            # Total revenue across all reservations converted to selected currency
            total_revenue_converted = Decimal('0')
            for amount, cur in Reservation.objects.values_list('total_price', 'payment_currency'):
                total_revenue_converted += convert_amount(amount, cur, selected_currency)
            
            # Monthly revenue (last 30 days) converted to selected currency
            monthly_revenue_converted = Decimal('0')
            for amount, cur in Reservation.objects.filter(created_at__date__gte=last_30_days).values_list('total_price', 'payment_currency'):
                monthly_revenue_converted += convert_amount(amount, cur, selected_currency)
            
            context['stats']['total_revenue'] = total_revenue_converted
            context['stats']['monthly_revenue'] = monthly_revenue_converted
        
        # Recent activity
        context['recent_reservations'] = Reservation.objects.select_related('created_by')[:5]
        context['recent_inquiries'] = Contact.objects.filter(is_read=False)[:5]
        
        return context


class ReservationListView(ViewerAllowedMixin, ListView):
    model = Reservation
    template_name = 'backoffice/reservation_list.html'
    context_object_name = 'reservations'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Reservation.objects.select_related('created_by', 'source_contact')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(guest_full_name__icontains=search) |
                Q(company_name__icontains=search) |
                Q(contact_number__icontains=search)
            )
        
        # Date filtering
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(arrival_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(departure_date__lte=date_to)
        
        return queryset


class ReservationDetailView(ViewerAllowedMixin, DetailView):
    model = Reservation
    template_name = 'backoffice/reservation_detail.html'
    context_object_name = 'reservation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audit_logs'] = self.object.audit_logs.select_related('user')[:10]
        
        # Check if user can edit: admin can edit all; agents can edit their own
        try:
            profile = self.request.user.userprofile
            is_admin = (profile.role == 'admin')
            is_owner = (self.object.created_by_id == self.request.user.id)
            context['can_edit'] = is_admin or is_owner
        except UserProfile.DoesNotExist:
            context['can_edit'] = False
        
        return context


class ReservationCreateView(AgentRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'backoffice/reservation_form.html'
    success_url = reverse_lazy('backoffice:reservation_list')
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill booked_by with current user for convenience
        me = self.request.user
        initial.setdefault('booked_by', me.get_full_name() or me.username)
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass user to form so it can disable fields for non-admins
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Create audit log
        ReservationAuditLog.objects.create(
            reservation=self.object,
            user=self.request.user,
            action='created',
            changes={'status': 'Created new reservation'}
        )
        
        # Send confirmation email to guest
        try:
            email_sent = BanbasEmailService.send_reservation_confirmation(self.object)
            if email_sent:
                messages.success(self.request, f'Reservation for {self.object.guest_full_name} created successfully! Confirmation email sent.')
            else:
                messages.warning(self.request, f'Reservation for {self.object.guest_full_name} created successfully! However, confirmation email could not be sent.')
        except Exception as e:
            messages.warning(self.request, f'Reservation for {self.object.guest_full_name} created successfully! However, confirmation email could not be sent: {str(e)}')
        
        return response


class ReservationEditView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'backoffice/reservation_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Allow admins to edit any reservation and agents to edit only their own
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("Access denied")
        
        # Fetch target reservation for ownership check
        obj = get_object_or_404(Reservation, pk=kwargs.get('pk'))
        is_admin = (profile.role == 'admin')
        is_owner = (obj.created_by_id == request.user.id)
        
        if not (is_admin or is_owner):
            messages.error(request, 'You can only edit reservations you created. Administrators can edit all reservations.')
            return redirect('backoffice:reservation_detail', pk=kwargs['pk'])
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass user to form so it can disable fields for non-admins
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Track changes for audit log
        old_values = {}
        new_values = {}
        
        # Form-only fields that don't exist on the model
        form_only_fields = ['single_rooms', 'double_rooms', 'triple_rooms']
        
        for field in form.changed_data:
            if field in form_only_fields:
                # For room type fields, get the old values from room_types JSON
                if field == 'single_rooms':
                    old_values[field] = self.object.room_types.get('single', 0) if self.object.room_types else 0
                elif field == 'double_rooms':
                    old_values[field] = self.object.room_types.get('double', 0) if self.object.room_types else 0
                elif field == 'triple_rooms':
                    old_values[field] = self.object.room_types.get('triple', 0) if self.object.room_types else 0
                new_values[field] = form.cleaned_data[field]
            else:
                # For regular model fields
                old_values[field] = getattr(self.object, field, None)
                new_values[field] = form.cleaned_data[field]
        
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        
        # Create audit log for changes
        if form.changed_data:
            ReservationAuditLog.objects.create(
                reservation=self.object,
                user=self.request.user,
                action='updated',
                changes={
                    'fields_changed': form.changed_data,
                    'old_values': {k: str(v) for k, v in old_values.items()},
                    'new_values': {k: str(v) for k, v in new_values.items()}
                }
            )
        
        messages.success(self.request, f'Reservation for {self.object.guest_full_name} updated successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('backoffice:reservation_detail', kwargs={'pk': self.object.pk})


class ContactInquiryListView(ViewerAllowedMixin, ListView):
    model = Contact
    template_name = 'backoffice/inquiry_list.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    
    def get_queryset(self):
        return Contact.objects.all().order_by('-created_at')


class ContactInquiryDetailView(ViewerAllowedMixin, DetailView):
    model = Contact
    template_name = 'backoffice/inquiry_detail.html'
    context_object_name = 'inquiry'
    
    def get_object(self):
        obj = super().get_object()
        # Mark as read when viewed (only if not a POST request)
        if not obj.is_read and self.request.method == 'GET':
            obj.is_read = True
            obj.save()
        return obj
    
    def post(self, request, *args, **kwargs):
        inquiry = self.get_object()
        
        # Handle mark as read action
        if 'mark_read' in request.POST:
            inquiry.is_read = True
            inquiry.save()
            messages.success(request, f'Inquiry from {inquiry.name} marked as read.')
            return redirect('backoffice:inquiry_detail', pk=inquiry.pk)
        
        # Handle delete action
        elif 'delete_inquiry' in request.POST:
            inquiry_name = inquiry.name
            inquiry_subject = inquiry.subject
            inquiry.delete()
            messages.success(request, f'Inquiry "{inquiry_subject}" from {inquiry_name} has been deleted.')
            return redirect('backoffice:inquiry_list')
        
        return self.get(request, *args, **kwargs)


class ConvertInquiryView(AgentRequiredMixin, TemplateView):
    template_name = 'backoffice/convert_inquiry.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry'] = get_object_or_404(Contact, pk=kwargs['pk'])
        
        # If this is a GET request or form has errors, show the form
        if not hasattr(self, 'form'):
            context['form'] = ReservationForm(initial={
                'guest_full_name': context['inquiry'].name,
                'contact_number': context['inquiry'].phone,
                'booked_by': self.request.user.get_full_name() or self.request.user.username,
                'arrival_date': getattr(context['inquiry'], 'preferred_checkin', None),
                'departure_date': getattr(context['inquiry'], 'preferred_checkout', None),
            }, user=self.request.user)
        else:
            context['form'] = self.form
            
        return context
    
    def post(self, request, *args, **kwargs):
        inquiry = get_object_or_404(Contact, pk=kwargs['pk'])
        form = ReservationForm(request.POST, user=request.user)
        
        if form.is_valid():
            # Create the reservation
            reservation = form.save(commit=False)
            reservation.created_by = request.user
            reservation.source_contact = inquiry  # Link to original inquiry
            reservation.save()
            
            # Create audit log
            ReservationAuditLog.objects.create(
                reservation=reservation,
                user=request.user,
                action='created',
                changes={
                    'status': 'Created from inquiry conversion',
                    'source_inquiry_id': inquiry.id,
                    'source_inquiry_subject': inquiry.subject
                }
            )
            
            # Mark inquiry as read since it's been processed
            if not inquiry.is_read:
                inquiry.is_read = True
                inquiry.save()
            
            # Send confirmation email to guest
            try:
                email_sent = BanbasEmailService.send_reservation_confirmation(reservation)
                if email_sent:
                    messages.success(
                        request, 
                        f'Successfully created reservation for {reservation.guest_full_name} from inquiry "{inquiry.subject}". Confirmation email sent.'
                    )
                else:
                    messages.warning(
                        request, 
                        f'Successfully created reservation for {reservation.guest_full_name} from inquiry "{inquiry.subject}". However, confirmation email could not be sent.'
                    )
            except Exception as e:
                messages.warning(
                    request, 
                    f'Successfully created reservation for {reservation.guest_full_name} from inquiry "{inquiry.subject}". However, confirmation email could not be sent: {str(e)}'
                )
            
            return redirect('backoffice:reservation_detail', pk=reservation.pk)
        
        else:
            # Form has errors, store it to display in context
            self.form = form
            messages.error(request, 'Please fix the errors below and try again.')
            return self.get(request, *args, **kwargs)


class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'backoffice/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user profile for permissions
        try:
            profile = self.request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
        
        # Date range from request
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if not date_from:
            date_from = (timezone.now() - timedelta(days=30)).date()
        else:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        
        if not date_to:
            date_to = timezone.now().date()
        else:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        # Filter reservations by date range
        reservations = Reservation.objects.filter(
            arrival_date__gte=date_from,
            departure_date__lte=date_to
        )
        
        # Basic analytics
        total_reservations = reservations.count()
        context.update({
            'date_from': date_from,
            'date_to': date_to,
            'total_reservations': total_reservations,
            'total_guests': reservations.aggregate(
                adults=Sum('total_adults'),
                children=Sum('total_children')
            ),
            'occupancy_data': reservations.aggregate(
                total_rooms=Sum('number_of_rooms')
            ),
            'inquiries_count': Contact.objects.filter(
                created_at__date__gte=date_from,
                created_at__date__lte=date_to
            ).count(),
        })
        
        # Revenue data (admin only) with currency conversion
        if profile and profile.can_view_revenue():
            allowed_currencies = ['NRS', 'USD', 'INR', 'EUR']
            selected_currency = self.request.GET.get('currency')
            if selected_currency not in allowed_currencies:
                existing = list(
                    reservations.values_list('payment_currency', flat=True).distinct()
                )
                selected_currency = existing[0] if existing else 'USD'
            context['selected_currency'] = selected_currency
            context['available_currencies'] = allowed_currencies
            
            rates = {code: Decimal(str(rate)) for code, rate in EXCHANGE_RATES.items()}
            
            def convert_amount(amount_dec: Decimal, from_cur: str, to_cur: str) -> Decimal:
                if not amount_dec:
                    return Decimal('0')
                if from_cur == to_cur:
                    return amount_dec
                amount_in_nrs = amount_dec / rates[from_cur]
                return (amount_in_nrs * rates[to_cur]).quantize(Decimal('0.01'))
            
            total_revenue_converted = Decimal('0')
            for amount, cur in reservations.values_list('total_price', 'payment_currency'):
                total_revenue_converted += convert_amount(amount, cur, selected_currency)
            
            avg_per_res = (
                (total_revenue_converted / total_reservations).quantize(Decimal('0.01'))
                if total_reservations > 0 else Decimal('0.00')
            )
            
            context['revenue_data'] = {
                'total_revenue': total_revenue_converted,
                'avg_per_reservation': avg_per_res,
            }
        
        return context


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'backoffice/user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.select_related('userprofile').filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = context['users']
        # Safe DB counts instead of template loop counters
        context.update({
            'total_users': qs.count(),
            'admin_count': qs.filter(userprofile__role='admin').count(),
            'agent_count': qs.filter(userprofile__role='agent').count(),
            'viewer_count': qs.filter(userprofile__role='viewer').count(),
        })
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Additional security check - ensure user has admin role
        try:
            profile = request.user.userprofile
            if profile.role != 'admin':
                messages.error(request, 'Access denied: Only administrators can manage users.')
                return redirect('backoffice:dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No role assigned.')
            return redirect('backoffice:dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(AdminRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'backoffice/user_form.html'
    success_url = reverse_lazy('backoffice:user_list')
    
    def dispatch(self, request, *args, **kwargs):
        # Additional security check - ensure user has admin role
        try:
            profile = request.user.userprofile
            if profile.role != 'admin':
                messages.error(request, 'Access denied: Only administrators can create users.')
                return redirect('backoffice:dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No role assigned.')
            return redirect('backoffice:dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username', 'Unknown')
        messages.success(self.request, f'User {username} created successfully!')
        return response


class UserEditView(AdminRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'backoffice/user_form.html'
    success_url = reverse_lazy('backoffice:user_list')
    
    def dispatch(self, request, *args, **kwargs):
        # Additional security check - ensure user has admin role
        try:
            profile = request.user.userprofile
            if profile.role != 'admin':
                messages.error(request, 'Access denied: Only administrators can edit users.')
                return redirect('backoffice:dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Access denied: No role assigned.')
            return redirect('backoffice:dashboard')
        
        # Check if the target user exists before proceeding
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
            if not hasattr(user, 'userprofile'):
                messages.error(request, f'User profile not found for user {user.username}.')
                return redirect('backoffice:user_list')
        except User.DoesNotExist:
            messages.error(request, f'User with ID {user_id} not found.')
            return redirect('backoffice:user_list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        # Get UserProfile object based on User ID from URL
        user_id = self.kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
            return user.userprofile
        except User.DoesNotExist:
            from django.http import Http404
            raise Http404("User not found.")
        except UserProfile.DoesNotExist:
            from django.http import Http404
            raise Http404("User profile not found.")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username', 'Unknown')
        messages.success(self.request, f'User {username} updated successfully!')
        return response


class ReservationDeleteView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'backoffice/reservation_confirm_delete.html'
    context_object_name = 'reservation'
    
    def post(self, request, *args, **kwargs):
        reservation = self.get_object()
        
        # Create comprehensive audit log before deletion
        deletion_data = {
            'reservation_id': reservation.id,
            'guest_full_name': reservation.guest_full_name,
            'company_name': reservation.company_name,
            'arrival_date': reservation.arrival_date.isoformat(),
            'departure_date': reservation.departure_date.isoformat(),
            'nationality': reservation.nationality,
            'room_category': reservation.room_category,
            'number_of_rooms': reservation.number_of_rooms,
            'room_types': reservation.room_types,
            'meal_plan': reservation.meal_plan,
            'total_adults': reservation.total_adults,
            'total_children': reservation.total_children,
            'booked_by': reservation.booked_by,
            'contact_number': reservation.contact_number,
            'payment_method': reservation.payment_method,
            'payment_currency': reservation.payment_currency,
            'total_price': str(reservation.total_price),
            'created_by': reservation.created_by.username,
            'created_at': reservation.created_at.isoformat(),
            'updated_at': reservation.updated_at.isoformat(),
            'updated_by': reservation.updated_by.username if reservation.updated_by else None,
            'deleted_by': request.user.username,
            'deletion_timestamp': timezone.now().isoformat(),
            'nights': reservation.nights,
            'total_guests': reservation.total_guests,
        }
        
        # Create audit log entry
        ReservationAuditLog.objects.create(
            reservation=reservation,
            user=request.user,
            action='deleted',
            original_reservation_id=reservation.id,
            guest_name=reservation.guest_full_name,
            changes={
                'status': 'Reservation permanently deleted',
                'deletion_reason': 'Manual deletion via admin interface',
                'original_data': deletion_data
            }
        )
        
        # Store guest name for success message
        guest_name = reservation.guest_full_name
        
        # Delete the reservation
        reservation.delete()
        
        # Success message
        messages.success(
            request, 
            f'Reservation for {guest_name} has been successfully deleted. Deletion logged for audit purposes.'
        )
        
        return redirect('backoffice:reservation_list')
