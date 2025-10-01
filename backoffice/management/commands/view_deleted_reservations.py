from django.core.management.base import BaseCommand
from django.utils import timezone
import json
from backoffice.models import ReservationAuditLog


class Command(BaseCommand):
    help = 'View audit log of deleted reservations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Show deletions from the last N days (default: 30)'
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed reservation data for each deletion'
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Filter by username who deleted the reservation'
        )

    def handle(self, *args, **options):
        days = options['days']
        detailed = options['detailed']
        username_filter = options['user']
        
        # Calculate date range
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=days)
        
        # Query deleted reservations
        deleted_reservations = ReservationAuditLog.objects.filter(
            action='deleted',
            timestamp__gte=start_date
        ).order_by('-timestamp')
        
        # Apply user filter if specified
        if username_filter:
            deleted_reservations = deleted_reservations.filter(
                user__username__icontains=username_filter
            )
        
        # Display results
        self.stdout.write(
            self.style.SUCCESS(f'Deleted Reservations (Last {days} days)')
        )
        self.stdout.write('=' * 60)
        
        if not deleted_reservations.exists():
            self.stdout.write(
                self.style.WARNING('No deleted reservations found in the specified period.')
            )
            return
        
        for log in deleted_reservations:
            self.display_deletion_log(log, detailed)
            self.stdout.write('')  # Empty line separator
        
        self.stdout.write('-' * 60)
        self.stdout.write(
            self.style.SUCCESS(f'Total deleted reservations: {deleted_reservations.count()}')
        )

    def display_deletion_log(self, log, detailed=False):
        """Display individual deletion log entry"""
        self.stdout.write(
            self.style.HTTP_INFO(f'Reservation ID: {log.original_reservation_id}')
        )
        self.stdout.write(f'Guest: {log.guest_name}')
        self.stdout.write(f'Deleted by: {log.user.get_full_name() or log.user.username}')
        self.stdout.write(f'Deleted at: {log.timestamp.strftime("%Y-%m-%d %H:%M:%S")}')
        
        if detailed and log.changes.get('original_data'):
            original_data = log.changes['original_data']
            self.stdout.write(self.style.WARNING('Reservation Details:'))
            
            # Display key information
            key_fields = [
                ('Arrival Date', 'arrival_date'),
                ('Departure Date', 'departure_date'),
                ('Nationality', 'nationality'),
                ('Number of Rooms', 'number_of_rooms'),
                ('Total Adults', 'total_adults'),
                ('Total Children', 'total_children'),
                ('Total Price', 'total_price'),
                ('Currency', 'payment_currency'),
                ('Created By', 'created_by'),
                ('Company', 'company_name'),
                ('Contact', 'contact_number'),
                ('Room Types', 'room_types'),
                ('Meal Plan', 'meal_plan'),
                ('Payment Method', 'payment_method'),
            ]
            
            for label, key in key_fields:
                value = original_data.get(key)
                if value:
                    if key == 'room_types':
                        # Format room types nicely
                        if isinstance(value, dict):
                            room_display = []
                            for room_type, count in value.items():
                                if count > 0:
                                    room_display.append(f"{count} {room_type}")
                            value = ", ".join(room_display) or "None"
                    
                    self.stdout.write(f'  {label}: {value}')
            
            # Show deletion reason
            deletion_reason = log.changes.get('deletion_reason', 'Not specified')
            self.stdout.write(f'Deletion Reason: {deletion_reason}')
    
    def handle_error(self, message):
        """Handle and display errors"""
        self.stdout.write(
            self.style.ERROR(f'Error: {message}')
        )