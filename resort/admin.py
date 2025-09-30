from django.contrib import admin
from .models import RoomType, Amenity, Gallery, Contact, Resort, Booking, Activity, RoomGallery


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


class RoomGalleryInline(admin.TabularInline):
    model = RoomGallery
    extra = 1
    fields = ['media_type', 'title', 'image_url', 'video_url', 'video_thumbnail', 'order', 'is_featured']
    ordering = ['order']


@admin.register(RoomGallery)
class RoomGalleryAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'media_type', 'title', 'order', 'is_featured', 'created_at']
    list_filter = ['media_type', 'is_featured', 'room_type']
    search_fields = ['title', 'room_type__name']
    ordering = ['room_type', 'order']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_occupancy', 'size_sqm', 'room_count', 'is_available', 'is_featured', 'created_at']
    list_filter = ['max_occupancy', 'is_available', 'is_featured', 'has_ocean_view', 'has_balcony', 'is_suite']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_featured']
    ordering = ['name']
    inlines = [RoomGalleryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'detailed_description')
        }),
        ('Room Details', {
            'fields': ('max_occupancy', 'size_sqm', 'room_count', 'amenities')
        }),
        ('Features', {
            'fields': ('has_balcony', 'has_ocean_view', 'has_garden_view', 'has_kitchenette', 'has_jacuzzi', 'is_suite')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Pricing & Availability', {
            'fields': ('base_price', 'is_available', 'is_featured'),
            'description': 'Base price is for admin reference only and not displayed to guests.'
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


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty', 'price', 'duration', 'is_featured', 'is_available', 'created_at']
    list_filter = ['category', 'difficulty', 'is_featured', 'is_available', 'requires_booking', 'includes_equipment', 'includes_guide', 'created_at']
    search_fields = ['name', 'short_description', 'full_description', 'location']
    list_editable = ['is_featured', 'is_available', 'price']
    ordering = ['-is_featured', '-is_available', 'category', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'short_description', 'full_description')
        }),
        ('Rich Content', {
            'fields': ('detailed_content',),
            'description': 'Use the rich text editor to add detailed content, images, and formatting for the activity detail page.'
        }),
        ('Activity Details', {
            'fields': ('difficulty', 'duration', 'max_participants', 'min_age', 'price', 'location')
        }),
        ('Visual Design', {
            'fields': ('icon_class', 'image_placeholder', 'background_color'),
            'description': 'Icon class examples: fas fa-swimming-pool, fas fa-mountain, fas fa-spa, fas fa-utensils'
        }),
        ('Availability & Features', {
            'fields': ('is_available', 'is_featured', 'requires_booking', 'includes_equipment', 'includes_guide', 'includes_transport')
        }),
        ('Scheduling', {
            'fields': ('available_days', 'available_times'),
            'description': 'Use comma-separated values. Days: Monday,Tuesday,etc. Times: 9:00 AM,2:00 PM,etc.'
        }),
        ('Additional Information', {
            'fields': ('what_to_bring', 'included_items'),
            'description': 'Use comma-separated values for lists'
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    class Media:
        css = {
            'all': ('admin/css/activity_admin.css',)
        }
        js = ('admin/js/activity_admin.js',)
