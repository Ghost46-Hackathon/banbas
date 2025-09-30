from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Contact, Booking


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your inquiry'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about your inquiry or special requests...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make phone field not required
        self.fields['phone'].required = False


class BookingForm(forms.ModelForm):
    """Form for handling booking requests"""
    
    # Custom fields for handling multiple selections
    preferences_list = forms.MultipleChoiceField(
        choices=[
            ('ocean_view', 'Ocean View'),
            ('balcony', 'Balcony/Terrace'),
            ('high_floor', 'High Floor'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    services_list = forms.MultipleChoiceField(
        choices=[
            ('airport_transfer', 'Airport Transfer'),
            ('spa_package', 'Spa Package'),
            ('dining_package', 'Dining Package'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Booking
        exclude = ['preferences', 'services', 'status', 'created_at', 'updated_at']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Your address (optional)'
            }),
            'checkin_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'checkout_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'adults': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }, choices=[
                ('', 'Select Adults'),
                (1, '1 Adult'),
                (2, '2 Adults'),
                (3, '3 Adults'),
                (4, '4 Adults'),
                (5, '5+ Adults'),
            ]),
            'children': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                (0, 'No Children'),
                (1, '1 Child'),
                (2, '2 Children'),
                (3, '3 Children'),
                (4, '4+ Children'),
            ]),
            'rooms': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }, choices=[
                ('', 'Select Rooms'),
                (1, '1 Room'),
                (2, '2 Rooms'),
                (3, '3 Rooms'),
                (4, '4+ Rooms'),
            ]),
            'room_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bed_preference': forms.Select(attrs={
                'class': 'form-select'
            }),
            'occasion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'arrival_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please let us know if you have any special requests, dietary requirements, accessibility needs, or other preferences...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to today for date fields
        today = timezone.now().date().isoformat()
        self.fields['checkin_date'].widget.attrs['min'] = today
        self.fields['checkout_date'].widget.attrs['min'] = today
    
    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get('checkin_date')
        checkout_date = cleaned_data.get('checkout_date')
        
        # Validate dates
        if checkin_date and checkout_date:
            if checkin_date >= checkout_date:
                raise ValidationError('Check-out date must be after check-in date.')
            
            if checkin_date < timezone.now().date():
                raise ValidationError('Check-in date cannot be in the past.')
        
        return cleaned_data
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        
        # Save preferences and services as JSON
        booking.preferences = self.cleaned_data.get('preferences_list', [])
        booking.services = self.cleaned_data.get('services_list', [])
        
        if commit:
            booking.save()
        
        return booking
