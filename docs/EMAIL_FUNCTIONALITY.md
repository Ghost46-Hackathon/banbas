# Email Functionality - Banbas Resort

## 📧 Overview

The Banbas Resort management system includes comprehensive email functionality to communicate with guests and staff. All emails are sent from `info@banbasresort.com` and include professional HTML templates.

## 🚀 Features

### Email Types

1. **Reservation Confirmation** - Sent to guests when a reservation is created
2. **Reservation Update** - Sent to guests when reservation details are modified
3. **New Inquiry Notification** - Sent to staff when a new contact inquiry is received
4. **Inquiry Response** - Sent to guests when staff responds to their inquiry
5. **Welcome Email** - Sent to new guests (optional)

### Email Templates

All emails use responsive HTML templates with:
- Professional Banbas Resort branding
- Mobile-friendly design
- Consistent color scheme (#134a39 green theme)
- Clear call-to-action buttons
- Contact information and resort details

## 🔧 Configuration

### Development Setup

By default, emails are sent to the console for development. To see emails in the console, run:

```bash
python manage.py runserver
```

### Production Setup

To configure for production, set these environment variables:

```bash
# SMTP Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com  # or your SMTP server
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@banbasresort.com
EMAIL_HOST_PASSWORD=your_app_password

# From Email
DEFAULT_FROM_EMAIL=Banbas Resort <info@banbasresort.com>
```

### Email Service Configuration

The email service is configured in `banbas_resort/settings.py`:

```python
BANBAS_EMAIL_CONFIG = {
    'FROM_EMAIL': 'info@banbasresort.com',
    'FROM_NAME': 'Banbas Resort',
    'STAFF_EMAILS': [
        'admin@banbasresort.com',
        'reservations@banbasresort.com',
    ],
    'RESORT_INFO': {
        'name': 'Banbas Resort',
        'phone': '+1 (555) 123-4567',
        'email': 'info@banbasresort.com',
        'website': 'https://www.banbasresort.com',
        'address': '123 Paradise Beach Avenue, Tropical Island, TI 12345',
    }
}
```

## 🧪 Testing

### Test Email Functionality

Use the management command to test different email types:

```bash
# Test basic email
python manage.py test_email --type=basic --email=test@example.com

# Test reservation confirmation
python manage.py test_email --type=reservation

# Test inquiry notification
python manage.py test_email --type=inquiry

# Test welcome email
python manage.py test_email --type=welcome --email=test@example.com
```

### Manual Testing

You can also test emails manually in the Django shell:

```python
from backoffice.email_service import BanbasEmailService
from backoffice.models import Reservation

# Test reservation confirmation
reservation = Reservation.objects.first()
BanbasEmailService.send_reservation_confirmation(reservation, 'test@example.com')
```

## 📱 Email Templates

### Template Files

All email templates are located in `templates/emails/`:

- `reservation_confirmation.html` - Reservation confirmation email
- `reservation_update.html` - Reservation update notification
- `new_inquiry_notification.html` - Staff notification for new inquiries
- `inquiry_response.html` - Response to guest inquiries
- `welcome_email.html` - Welcome email for new guests

### Template Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Professional Branding**: Consistent with resort theme
- **Clear Information**: All relevant details included
- **Call-to-Actions**: Buttons for important actions
- **Contact Information**: Resort details in footer

## 🔄 Integration Points

### Automatic Email Triggers

1. **Reservation Creation**: 
   - When a new reservation is created in the backoffice
   - When an inquiry is converted to a reservation

2. **Contact Form Submission**:
   - Staff notification when contact form is submitted

3. **Reservation Updates**:
   - Guest notification when reservation is modified (can be implemented)

### Manual Email Sending

Staff can manually send emails through the backoffice system (can be implemented as a feature).

## 🛠️ Customization

### Adding New Email Types

1. Create a new method in `BanbasEmailService`
2. Create a new HTML template in `templates/emails/`
3. Integrate the email sending into the appropriate view

### Modifying Templates

All templates use Django template syntax and can be customized:
- Change colors by modifying CSS variables
- Update content by editing HTML
- Add new sections as needed

### Email Content

Email content can be customized by:
- Modifying the `BANBAS_EMAIL_CONFIG` in settings
- Updating template context in email service methods
- Editing HTML templates directly

## 📊 Email Logging

All email sending is logged with:
- Success/failure status
- Recipient information
- Error messages (if any)
- Timestamp

Check Django logs for email-related messages.

## 🔒 Security Considerations

- Email addresses are validated before sending
- No sensitive information in email logs
- SMTP credentials should be stored securely
- Use environment variables for production credentials

## 🚨 Troubleshooting

### Common Issues

1. **Emails not sending**:
   - Check SMTP configuration
   - Verify email credentials
   - Check Django logs for errors

2. **Templates not rendering**:
   - Ensure templates are in correct directory
   - Check template syntax
   - Verify context variables

3. **Console emails not showing**:
   - Check `EMAIL_BACKEND` setting
   - Ensure `DEBUG=True` in development

### Debug Mode

To debug email issues:

```python
import logging
logging.getLogger('django.core.mail').setLevel(logging.DEBUG)
```

## 📈 Future Enhancements

Potential improvements:
- Email templates editor in admin
- Email scheduling
- Email analytics
- A/B testing for templates
- Multi-language support
- Email preferences for guests
