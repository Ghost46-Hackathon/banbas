"""
Email service for Banbas Resort
Handles sending emails to guests and staff for various events
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class BanbasEmailService:
    """Email service for Banbas Resort communications"""
    
    # Default sender email
    DEFAULT_FROM_EMAIL = 'info@banbasresort.com'
    DEFAULT_FROM_NAME = 'Banbas Resort'
    
    # Staff notification emails
    STAFF_EMAILS = [
        'admin@banbasresort.com',
        'reservations@banbasresort.com',
    ]
    
    @classmethod
    def send_reservation_confirmation(cls, reservation, guest_email=None):
        """Send reservation confirmation email to guest"""
        try:
            # Get guest email from parameter, contact, or reservation field
            if not guest_email:
                if reservation.source_contact:
                    guest_email = reservation.source_contact.email
                elif hasattr(reservation, 'guest_email'):
                    guest_email = reservation.guest_email
            
            if not guest_email:
                logger.warning(f"No email found for reservation {reservation.id}")
                return False
            
            # Prepare email context
            context = {
                'reservation': reservation,
                'resort_name': 'Banbas Resort',
                'resort_phone': '+1 (555) 123-4567',
                'resort_email': 'info@banbasresort.com',
                'resort_website': 'https://www.banbasresort.com',
                'resort_address': '123 Paradise Beach Avenue, Tropical Island, TI 12345',
            }
            
            # Render HTML template
            html_content = render_to_string('emails/reservation_confirmation.html', context)
            text_content = strip_tags(html_content)
            
            # Create email
            subject = f'Reservation Confirmation - {reservation.guest_full_name}'
            from_email = f'{cls.DEFAULT_FROM_NAME} <{cls.DEFAULT_FROM_EMAIL}>'
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[guest_email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send email
            result = msg.send()
            
            if result:
                logger.info(f"Reservation confirmation sent to {guest_email} for reservation {reservation.id}")
                return True
            else:
                logger.error(f"Failed to send reservation confirmation to {guest_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending reservation confirmation: {str(e)}")
            return False
    
    @classmethod
    def send_reservation_update(cls, reservation, changes, updated_by):
        """Send reservation update notification to guest"""
        try:
            # Get guest email
            guest_email = None
            if reservation.source_contact:
                guest_email = reservation.source_contact.email
            elif hasattr(reservation, 'guest_email'):
                guest_email = reservation.guest_email
            
            if not guest_email:
                logger.warning(f"No email found for reservation update {reservation.id}")
                return False
            
            # Prepare email context
            context = {
                'reservation': reservation,
                'changes': changes,
                'updated_by': updated_by,
                'resort_name': 'Banbas Resort',
                'resort_phone': '+1 (555) 123-4567',
                'resort_email': 'info@banbasresort.com',
                'resort_website': 'https://www.banbasresort.com',
            }
            
            # Render HTML template
            html_content = render_to_string('emails/reservation_update.html', context)
            text_content = strip_tags(html_content)
            
            # Create email
            subject = f'Reservation Update - {reservation.guest_full_name}'
            from_email = f'{cls.DEFAULT_FROM_NAME} <{cls.DEFAULT_FROM_EMAIL}>'
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[guest_email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send email
            result = msg.send()
            
            if result:
                logger.info(f"Reservation update sent to {guest_email} for reservation {reservation.id}")
                return True
            else:
                logger.error(f"Failed to send reservation update to {guest_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending reservation update: {str(e)}")
            return False
    
    @classmethod
    def send_new_inquiry_notification(cls, contact):
        """Send notification to staff about new contact inquiry"""
        try:
            # Prepare email context
            context = {
                'contact': contact,
                'resort_name': 'Banbas Resort',
            }
            
            # Render HTML template
            html_content = render_to_string('emails/new_inquiry_notification.html', context)
            text_content = strip_tags(html_content)
            
            # Create email
            subject = f'New Contact Inquiry: {contact.subject}'
            from_email = f'{cls.DEFAULT_FROM_NAME} <{cls.DEFAULT_FROM_EMAIL}>'
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=cls.STAFF_EMAILS
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send email
            result = msg.send()
            
            if result:
                logger.info(f"New inquiry notification sent to staff for contact {contact.id}")
                return True
            else:
                logger.error(f"Failed to send new inquiry notification")
                return False
                
        except Exception as e:
            logger.error(f"Error sending new inquiry notification: {str(e)}")
            return False
    
    @classmethod
    def send_inquiry_response(cls, contact, response_message, responded_by):
        """Send response to guest inquiry"""
        try:
            # Prepare email context
            context = {
                'contact': contact,
                'response_message': response_message,
                'responded_by': responded_by,
                'resort_name': 'Banbas Resort',
                'resort_phone': '+1 (555) 123-4567',
                'resort_email': 'info@banbasresort.com',
                'resort_website': 'https://www.banbasresort.com',
            }
            
            # Render HTML template
            html_content = render_to_string('emails/inquiry_response.html', context)
            text_content = strip_tags(html_content)
            
            # Create email
            subject = f'Re: {contact.subject}'
            from_email = f'{cls.DEFAULT_FROM_NAME} <{cls.DEFAULT_FROM_EMAIL}>'
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[contact.email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send email
            result = msg.send()
            
            if result:
                logger.info(f"Inquiry response sent to {contact.email} for contact {contact.id}")
                return True
            else:
                logger.error(f"Failed to send inquiry response to {contact.email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending inquiry response: {str(e)}")
            return False
    
    @classmethod
    def send_welcome_email(cls, guest_email, guest_name):
        """Send welcome email to new guests"""
        try:
            # Prepare email context
            context = {
                'guest_name': guest_name,
                'resort_name': 'Banbas Resort',
                'resort_phone': '+1 (555) 123-4567',
                'resort_email': 'info@banbasresort.com',
                'resort_website': 'https://www.banbasresort.com',
                'resort_address': '123 Paradise Beach Avenue, Tropical Island, TI 12345',
            }
            
            # Render HTML template
            html_content = render_to_string('emails/welcome_email.html', context)
            text_content = strip_tags(html_content)
            
            # Create email
            subject = f'Welcome to Banbas Resort, {guest_name}!'
            from_email = f'{cls.DEFAULT_FROM_NAME} <{cls.DEFAULT_FROM_EMAIL}>'
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[guest_email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send email
            result = msg.send()
            
            if result:
                logger.info(f"Welcome email sent to {guest_email}")
                return True
            else:
                logger.error(f"Failed to send welcome email to {guest_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending welcome email: {str(e)}")
            return False


def send_test_email():
    """Send a test email to verify email configuration"""
    try:
        send_mail(
            subject='Test Email from Banbas Resort',
            message='This is a test email to verify email configuration.',
            from_email='info@banbasresort.com',
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Test email failed: {str(e)}")
        return False
