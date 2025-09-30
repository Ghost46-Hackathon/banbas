from django.contrib import admin
from .models import RoomType, Amenity, Gallery, Contact, Resort, Booking


@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline', 'phone', 'email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'description')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Media', {
            'fields': ('hero_image_placeholder', 'hero_video')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url')
        })
    )


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'max_occupancy', 'size_sqm', 'created_at']
    list_filter = ['max_occupancy', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['base_price']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Details', {
            'fields': ('base_price', 'max_occupancy', 'size_sqm', 'amenities')
        }),
        ('Media', {
            'fields': ('image_placeholder',)
        })
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_featured', 'icon_class', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_featured']
    ordering = ['-is_featured', 'name']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'is_featured', 'created_at']
    list_filter = ['media_type', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'category', 'media_type']
    ordering = ['-is_featured', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'is_featured')
        }),
        ('Media Content', {
            'fields': ('media_type', 'image_placeholder', 'video_file', 'video_thumbnail')
        })
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        })
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'checkin_date', 'checkout_date', 
        'total_guests', 'rooms', 'status', 'created_at'
    ]
    list_filter = ['status', 'room_type', 'checkin_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Stay Details', {
            'fields': ('checkin_date', 'checkout_date', 'adults', 'children', 'rooms')
        }),
        ('Room Preferences', {
            'fields': ('room_type', 'bed_preference', 'preferences'),
            'classes': ('collapse',)
        }),
        ('Special Requests', {
            'fields': ('occasion', 'arrival_time', 'services', 'special_requests'),
            'classes': ('collapse',)
        }),
        ('Booking Status', {
            'fields': ('status', 'created_at', 'updated_at')
        })
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def total_guests(self, obj):
        return obj.total_guests
    total_guests.short_description = 'Total Guests'
