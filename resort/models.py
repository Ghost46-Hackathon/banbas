from django.db import models
from django.urls import reverse


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.IntegerField()
    size_sqm = models.IntegerField(help_text="Size in square meters")
    amenities = models.TextField(help_text="Comma-separated amenities")
    image_placeholder = models.CharField(max_length=200, default="https://via.placeholder.com/400x300/0066cc/ffffff?text=Room+Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['base_price']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resort:room_detail', kwargs={'pk': self.pk})


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    image_placeholder = models.CharField(max_length=200, default="https://via.placeholder.com/300x200/28a745/ffffff?text=Amenity")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name


class Gallery(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image_placeholder = models.CharField(max_length=200, default="https://via.placeholder.com/600x400/17a2b8/ffffff?text=Gallery+Image")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Upload video file (MP4 recommended)")
    video_thumbnail = models.CharField(max_length=200, blank=True, help_text="Thumbnail image URL for video")
    category = models.CharField(max_length=50, choices=[
        ('rooms', 'Rooms'),
        ('amenities', 'Amenities'),
        ('dining', 'Dining'),
        ('exterior', 'Exterior'),
        ('activities', 'Activities'),
    ], default='exterior')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Gallery"
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Booking(models.Model):
    """Model to store booking requests"""
    ROOM_TYPE_CHOICES = [
        ('', 'No Preference'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('oceanview', 'Ocean View'),
        ('presidential', 'Presidential Suite'),
    ]
    
    BED_PREFERENCE_CHOICES = [
        ('', 'No Preference'),
        ('king', 'King Bed'),
        ('queen', 'Queen Bed'),
        ('twin', 'Twin Beds'),
    ]
    
    OCCASION_CHOICES = [
        ('', 'Select Occasion'),
        ('honeymoon', 'Honeymoon'),
        ('anniversary', 'Anniversary'),
        ('birthday', 'Birthday'),
        ('business', 'Business Travel'),
        ('vacation', 'Vacation'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Guest Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    # Stay Details
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField(default=0)
    rooms = models.IntegerField()
    
    # Room Preferences
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, blank=True)
    bed_preference = models.CharField(max_length=10, choices=BED_PREFERENCE_CHOICES, blank=True)
    preferences = models.JSONField(default=list, blank=True)  # Store multiple preferences
    
    # Special Requests
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, blank=True)
    arrival_time = models.TimeField(blank=True, null=True)
    services = models.JSONField(default=list, blank=True)  # Store multiple services
    special_requests = models.TextField(blank=True)
    
    # Booking Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.checkin_date} to {self.checkout_date}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_guests(self):
        return self.adults + self.children
    
    @property
    def nights(self):
        return (self.checkout_date - self.checkin_date).days


class Resort(models.Model):
    """Single instance model for resort information"""
    name = models.CharField(max_length=100, default="Banbas Resort")
    tagline = models.CharField(max_length=200, default="Your Paradise Awaits")
    description = models.TextField(default="Experience luxury and comfort at Banbas Resort")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    hero_image_placeholder = models.CharField(
        max_length=200, 
        default="https://via.placeholder.com/1200x600/0066cc/ffffff?text=Banbas+Resort"
    )
    hero_video = models.FileField(
        upload_to='videos/', 
        blank=True, 
        null=True, 
        help_text="Hero background video (MP4 recommended, under 10MB)"
    )
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and Resort.objects.exists():
            # If this isn't the first instance and there's already one, update the existing one
            existing = Resort.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
