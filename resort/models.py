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
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_placeholder = models.CharField(max_length=200, default="https://via.placeholder.com/600x400/17a2b8/ffffff?text=Gallery+Image")
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
