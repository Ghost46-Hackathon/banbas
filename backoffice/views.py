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

from .models import Reservation, UserProfile, ReservationAuditLog
from .forms import ReservationForm, UserProfileForm
from resort.models import Contact


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


class AdminRequiredMixin(RoleRequiredMixin):
    required_role = 'admin'


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
        
        # Revenue data (admin only)
        if profile and profile.can_view_revenue():
            context['stats']['total_revenue'] = Reservation.objects.aggregate(
                revenue=Sum('total_price'))['revenue'] or 0
            context['stats']['monthly_revenue'] = Reservation.objects.filter(
                created_at__date__gte=last_30_days
            ).aggregate(revenue=Sum('total_price'))['revenue'] or 0
        
        # Recent activity
        context['recent_reservations'] = Reservation.objects.select_related('created_by')[:5]
        context['recent_inquiries'] = Contact.objects.filter(is_read=False)[:5]
        
        return context


class ReservationListView(LoginRequiredMixin, ListView):
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


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'backoffice/reservation_detail.html'
    context_object_name = 'reservation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audit_logs'] = self.object.audit_logs.select_related('user')[:10]
        
        # Check if user can edit
        try:
            profile = self.request.user.userprofile
            context['can_edit'] = profile.can_edit_reservations()
        except UserProfile.DoesNotExist:
            context['can_edit'] = False
        
        return context


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'backoffice/reservation_form.html'
    success_url = reverse_lazy('backoffice:reservation_list')
    
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
        
        messages.success(self.request, f'Reservation for {self.object.guest_full_name} created successfully!')
        return response


class ReservationEditView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'backoffice/reservation_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user can edit reservations
        try:
            profile = request.user.userprofile
            if not profile.can_edit_reservations():
                messages.error(request, 'Only administrators can edit reservations.')
                return redirect('backoffice:reservation_detail', pk=kwargs['pk'])
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("Access denied")
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Track changes for audit log
        old_values = {}
        new_values = {}
        
        for field in form.changed_data:
            old_values[field] = getattr(self.object, field)
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
                    'old_values': old_values,
                    'new_values': {k: str(v) for k, v in new_values.items()}
                }
            )
        
        messages.success(self.request, f'Reservation for {self.object.guest_full_name} updated successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('backoffice:reservation_detail', kwargs={'pk': self.object.pk})


class ContactInquiryListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'backoffice/inquiry_list.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    
    def get_queryset(self):
        return Contact.objects.all().order_by('-created_at')


class ContactInquiryDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'backoffice/inquiry_detail.html'
    context_object_name = 'inquiry'
    
    def get_object(self):
        obj = super().get_object()
        # Mark as read when viewed
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj


class ConvertInquiryView(LoginRequiredMixin, TemplateView):
    template_name = 'backoffice/convert_inquiry.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry'] = get_object_or_404(Contact, pk=kwargs['pk'])
        context['form'] = ReservationForm(initial={
            'guest_full_name': context['inquiry'].name,
            'contact_number': context['inquiry'].phone,
        })
        return context


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
        context.update({
            'date_from': date_from,
            'date_to': date_to,
            'total_reservations': reservations.count(),
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
        
        # Revenue data (admin only)
        if profile and profile.can_view_revenue():
            context['revenue_data'] = reservations.aggregate(
                total_revenue=Sum('total_price')
            )
        
        return context


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'backoffice/user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.select_related('userprofile').filter(is_active=True)


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserProfileForm
    template_name = 'backoffice/user_form.html'
    success_url = reverse_lazy('backoffice:user_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {self.object.username} created successfully!')
        return response


class UserEditView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'backoffice/user_form.html'
    success_url = reverse_lazy('backoffice:user_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {self.object.username} updated successfully!')
        return response
