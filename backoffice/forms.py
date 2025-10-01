from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Reservation, UserProfile


class ReservationForm(forms.ModelForm):
    """Comprehensive form for creating/editing reservations with all 15 required fields"""
    
    # Room type quantities (checkbox style with number inputs)
    single_rooms = forms.IntegerField(
        min_value=0, initial=0, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    double_rooms = forms.IntegerField(
        min_value=0, initial=0, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    triple_rooms = forms.IntegerField(
        min_value=0, initial=0, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    
    class Meta:
        model = Reservation
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by', 'room_types', 'source_contact']
        widgets = {
            'guest_full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter guest full name',
                'required': True
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name (optional)'
            }),
            'arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Guest nationality',
                'required': True
            }),
            'room_category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'number_of_rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'required': True
            }),
            'meal_plan': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'total_adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'required': True
            }),
            'total_children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'required': True
            }),
            'booked_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Agent/person who made the booking',
                'required': True
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+977 98XXXXXXXX'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'payment_currency': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        # Accept current user to control field-level permissions
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Set minimum dates
        today = timezone.now().date().isoformat()
        self.fields['arrival_date'].widget.attrs['min'] = today
        self.fields['departure_date'].widget.attrs['min'] = today
        
        # If editing existing reservation, populate room type quantities
        if self.instance and self.instance.pk and self.instance.room_types:
            room_types = self.instance.room_types
            self.fields['single_rooms'].initial = room_types.get('single', 0)
            self.fields['double_rooms'].initial = room_types.get('double', 0)
            self.fields['triple_rooms'].initial = room_types.get('triple', 0)
        
        # Make 'booked_by' read-only for non-admins and set sensible default
        if self.user:
            role = None
            try:
                role = self.user.userprofile.role
            except Exception:
                role = None
            if role != 'admin':
                self.fields['booked_by'].disabled = True
                if not self.instance or not self.instance.pk:
                    # On creation, default to current user's identity
                    self.fields['booked_by'].initial = self.user.get_full_name() or self.user.username
    
    def clean(self):
        cleaned_data = super().clean()
        arrival_date = cleaned_data.get('arrival_date')
        departure_date = cleaned_data.get('departure_date')
        
        # Validate dates
        if arrival_date and departure_date:
            if arrival_date >= departure_date:
                raise ValidationError('Departure date must be after arrival date.')
            
            if arrival_date < timezone.now().date():
                raise ValidationError('Arrival date cannot be in the past.')
        
        # Validate room quantities - handle None values
        try:
            single_rooms = int(cleaned_data.get('single_rooms') or 0)
            double_rooms = int(cleaned_data.get('double_rooms') or 0)
            triple_rooms = int(cleaned_data.get('triple_rooms') or 0)
        except (ValueError, TypeError):
            single_rooms = double_rooms = triple_rooms = 0
        
        total_room_quantity = single_rooms + double_rooms + triple_rooms
        number_of_rooms = cleaned_data.get('number_of_rooms', 0)
        
        if total_room_quantity == 0:
            raise ValidationError('At least one room type must be selected.')
        
        # Auto-update number_of_rooms if not matching
        if total_room_quantity != number_of_rooms:
            cleaned_data['number_of_rooms'] = total_room_quantity
        
        return cleaned_data
    
    def save(self, commit=True):
        reservation = super().save(commit=False)
        
        # Set room_types JSON from individual fields
        try:
            reservation.room_types = {
                'single': int(self.cleaned_data.get('single_rooms') or 0),
                'double': int(self.cleaned_data.get('double_rooms') or 0),
                'triple': int(self.cleaned_data.get('triple_rooms') or 0),
            }
        except (ValueError, TypeError):
            reservation.room_types = {
                'single': 0,
                'double': 0,
                'triple': 0,
            }
        
        if commit:
            reservation.save()
        
        return reservation


class UserProfileForm(forms.ModelForm):
    """Form for creating/editing users with profile information"""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Leave blank to keep existing password"
    )
    
    class Meta:
        model = UserProfile
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select', 'required': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing user, populate user fields
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            user = self.instance.user
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        # Check if username exists (exclude current user if editing)
        user_query = User.objects.filter(username=username)
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            user_query = user_query.exclude(pk=self.instance.user.pk)
        
        if user_query.exists():
            raise ValidationError('A user with this username already exists.')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Check if email exists (exclude current user if editing)
        user_query = User.objects.filter(email=email)
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            user_query = user_query.exclude(pk=self.instance.user.pk)
        
        if user_query.exists():
            raise ValidationError('A user with this email already exists.')
        
        return email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Create or update User instance
        if hasattr(profile, 'user') and profile.user:
            # Editing existing user
            user = profile.user
        else:
            # Creating new user
            user = User()
            
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        # Set password if provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        elif not user.pk:
            # New user without password - set a random one
            user.set_password(User.objects.make_random_password())
        
        if commit:
            user.save()
            profile.user = user
            profile.save()
        
        return profile