import time

from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())
    rendered_at = forms.IntegerField(required=False, widget=forms.HiddenInput())
    turnstile_token = forms.CharField(required=False, widget=forms.HiddenInput())

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
        self.enable_turnstile = kwargs.pop('enable_turnstile', False)
        self.min_submit_seconds = kwargs.pop('min_submit_seconds', 3)
        super().__init__(*args, **kwargs)

        self.fields['phone'].required = False
        self.fields['turnstile_token'].widget.attrs['id'] = 'id_turnstile_token'

        if not self.initial.get('rendered_at'):
            self.initial['rendered_at'] = int(time.time())

    def clean_honeypot(self):
        honeypot = self.cleaned_data.get('honeypot', '')
        if honeypot:
            raise forms.ValidationError('Bot submission blocked.')
        return honeypot

    def clean(self):
        cleaned_data = super().clean()

        rendered_at = cleaned_data.get('rendered_at')
        now = int(time.time())
        if not isinstance(rendered_at, int):
            raise forms.ValidationError('Invalid submission payload.')

        if now - rendered_at < self.min_submit_seconds:
            raise forms.ValidationError('Form submitted too quickly. Please try again.')

        if self.enable_turnstile and not cleaned_data.get('turnstile_token'):
            raise forms.ValidationError('Please complete the bot verification challenge.')

        return cleaned_data
