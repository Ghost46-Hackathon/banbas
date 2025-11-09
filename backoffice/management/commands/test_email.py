from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from backoffice.email_service import BanbasEmailService, send_test_email
from backoffice.models import Reservation
from resort.models import Contact
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Test email functionality for Banbas Resort'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['basic', 'reservation', 'inquiry', 'welcome'],
            default='basic',
            help='Type of email test to run'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        email_type = options['type']
        test_email = options.get('email', 'test@example.com')
        
        self.stdout.write(self.style.SUCCESS(f'Testing {email_type} email functionality...'))
        
        if email_type == 'basic':
            self.test_basic_email(test_email)
        elif email_type == 'reservation':
            self.test_reservation_email()
        elif email_type == 'inquiry':
            self.test_inquiry_email()
        elif email_type == 'welcome':
            self.test_welcome_email(test_email)
        
        self.stdout.write(self.style.SUCCESS('Email test completed!'))

    def test_basic_email(self, test_email):
        """Test basic Django email functionality"""
        try:
            send_mail(
                subject='Test Email from Banbas Resort',
                message='This is a test email to verify email configuration.',
                from_email='info@banbasresort.com',
                recipient_list=[test_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('✓ Basic email sent successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Basic email failed: {str(e)}'))

    def test_reservation_email(self):
        """Test reservation confirmation email"""
        try:
            # Get the first reservation or create a test one
            reservation = Reservation.objects.first()
            if not reservation:
                self.stdout.write(self.style.WARNING('No reservations found. Creating a test reservation...'))
                # Create a test reservation
                user = User.objects.first()
                if not user:
                    self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
                    return
                
                reservation = Reservation.objects.create(
                    guest_full_name='Test Guest',
                    arrival_date='2024-01-15',
                    departure_date='2024-01-18',
                    nationality='American',
                    room_category='pond_view',
                    number_of_rooms=1,
                    room_types={'double': 1},
                    meal_plan='bb',
                    total_adults=2,
                    total_children=0,
                    booked_by='Test Agent',
                    payment_method='cash',
                    payment_currency='USD',
                    total_price=450.00,
                    created_by=user
                )
            
            # Send reservation confirmation email
            email_sent = BanbasEmailService.send_reservation_confirmation(reservation)
            if email_sent:
                self.stdout.write(self.style.SUCCESS('✓ Reservation confirmation email sent successfully'))
            else:
                self.stdout.write(self.style.ERROR('✗ Reservation confirmation email failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Reservation email test failed: {str(e)}'))

    def test_inquiry_email(self):
        """Test inquiry notification email"""
        try:
            # Get the first contact or create a test one
            contact = Contact.objects.first()
            if not contact:
                self.stdout.write(self.style.WARNING('No contact inquiries found. Creating a test inquiry...'))
                contact = Contact.objects.create(
                    name='Test Customer',
                    email='test@example.com',
                    phone='+1 (555) 123-4567',
                    subject='Test Inquiry',
                    message='This is a test inquiry message.',
                    is_read=False
                )
            
            # Send inquiry notification email
            email_sent = BanbasEmailService.send_new_inquiry_notification(contact)
            if email_sent:
                self.stdout.write(self.style.SUCCESS('✓ Inquiry notification email sent successfully'))
            else:
                self.stdout.write(self.style.ERROR('✗ Inquiry notification email failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Inquiry email test failed: {str(e)}'))

    def test_welcome_email(self, test_email):
        """Test welcome email"""
        try:
            email_sent = BanbasEmailService.send_welcome_email(test_email, 'Test Guest')
            if email_sent:
                self.stdout.write(self.style.SUCCESS('✓ Welcome email sent successfully'))
            else:
                self.stdout.write(self.style.ERROR('✗ Welcome email failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Welcome email test failed: {str(e)}'))
