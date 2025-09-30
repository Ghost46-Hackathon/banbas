from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from decimal import Decimal
import json


class UserProfile(models.Model):
    """Extended user profile with role-based permissions"""
    ROLE_CHOICES = [
        ('agent', 'Agent'),
        ('viewer', 'Viewer'), 
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='agent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    def can_edit_reservations(self):
        return self.role == 'admin'
    
    def can_view_revenue(self):
        return self.role == 'admin'


class Reservation(models.Model):
    """Comprehensive reservation model with all required fields"""
    
    # Room Category Choices
    ROOM_CATEGORY_CHOICES = [
        ('availability', 'Based on Availability'),
        ('pond_view', 'Pond View'),
        ('garden_view', 'Garden View'),
        ('long_house', 'Long House'),
    ]
    
    # Room Type Choices
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
    ]
    
    # Meal Plan Choices
    MEAL_PLAN_CHOICES = [
        ('ep', 'EP'),
        ('bb', 'B&B'),
        ('map', 'MAP'),
        ('ap', 'AP'),
        ('1n2d_jp', '1N/2D JP'),
        ('2n3d_jp', '2N/3D JP'),
        ('3n4d_jp', '3N/4D JP'),
    ]
    
    # Payment Method Choices
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('company', 'Company'),
        ('complementary', 'Complementary'),
    ]
    
    # Payment Currency Choices
    CURRENCY_CHOICES = [
        ('NRS', 'NRS'),
        ('INR', 'INR'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    
    # 1. Guest Full name (Mandatory)
    guest_full_name = models.CharField(max_length=200)
    
    # 2. Company Name (Optional)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    
    # 3. Arrival Date (Mandatory)
    arrival_date = models.DateField()
    
    # 4. Departure Date (Mandatory)
    departure_date = models.DateField()
    
    # 5. Nationality (Mandatory)
    nationality = models.CharField(max_length=100)
    
    # 6. Room Category (Mandatory)
    room_category = models.CharField(max_length=20, choices=ROOM_CATEGORY_CHOICES)
    
    # 7. Number of rooms (Mandatory)
    number_of_rooms = models.IntegerField()
    
    # 8. Room Type and quantities (Mandatory) - stored as JSON
    # Format: {'single': 2, 'double': 1, 'triple': 0}
    room_types = models.JSONField(default=dict, help_text="Room type quantities as JSON")
    
    # 9. Meal plan (Mandatory)
    meal_plan = models.CharField(max_length=20, choices=MEAL_PLAN_CHOICES)
    
    # 10. Total number of adults (Mandatory)
    total_adults = models.IntegerField()
    
    # 11. Total number of children (Mandatory)
    total_children = models.IntegerField(default=0)
    
    # 12. Booked By (Mandatory)
    booked_by = models.CharField(max_length=200)
    
    # 13. Contact number (Optional)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    
    # 14. Payment method and currency (Mandatory)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    
    # 15. Total price of package (Mandatory)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Additional metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_reservations', null=True, blank=True)
    
    # Source inquiry (if created from contact form)
    source_contact = models.ForeignKey('resort.Contact', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.guest_full_name} - {self.arrival_date} to {self.departure_date}"
    
    @property
    def total_guests(self):
        return self.total_adults + self.total_children
    
    @property
    def nights(self):
        return (self.departure_date - self.arrival_date).days
    
    @property
    def room_types_display(self):
        """Human readable room types"""
        room_types = self.room_types or {}
        display_parts = []
        for room_type, count in room_types.items():
            if count > 0:
                type_display = dict(self.ROOM_TYPE_CHOICES).get(room_type, room_type)
                display_parts.append(f"{count} {type_display}")
        return ", ".join(display_parts) if display_parts else "None specified"
    
    def save(self, *args, **kwargs):
        # Auto-calculate number of rooms from room_types if not set
        if not self.number_of_rooms and self.room_types:
            self.number_of_rooms = sum(self.room_types.values())
        super().save(*args, **kwargs)


class ReservationAuditLog(models.Model):
    """Audit trail for reservation changes"""
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, related_name='audit_logs', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # 'created', 'updated', 'deleted'
    changes = models.JSONField(default=dict)  # What changed
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional fields to preserve data when reservation is deleted
    original_reservation_id = models.IntegerField(null=True, blank=True)  # Original reservation ID
    guest_name = models.CharField(max_length=200, null=True, blank=True)  # Guest name for reference
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        if self.reservation:
            return f"{self.reservation} - {self.action} by {self.user.username}"
        else:
            return f"Reservation ID {self.original_reservation_id} ({self.guest_name}) - {self.action} by {self.user.username}"
