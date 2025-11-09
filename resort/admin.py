from django.contrib import admin
from .models import (
    RoomType,
    Amenity,
    Gallery,
    GalleryCategory,
    Contact,
    Resort,
    Activity,
    RoomGallery,
    Blog,
    AboutPage,
    NavigationSettings,
)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    fieldsets = (
        ('Page Content', {
            'fields': ('title', 'subtitle', 'main_image', 'secondary_image')
        }),
        ('Founder\'s Narrative', {
            'fields': ('founders_narrative_title', 'founders_narrative_content', 'founders_narrative_image')
        }),
        ('Management Partnership', {
            'fields': ('management_partnership_title', 'management_partnership_content', 'management_partnership_image')
        }),
        ('Vision and Design', {
            'fields': ('vision_and_design_title', 'vision_and_design_content', 'vision_and_design_image')
        }),
    )


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
    list_display = ['name', 'max_occupancy', 'size_sqm', 'room_count', 'is_available', 'is_featured', 'show_price_publicly', 'created_at']
    list_filter = ['max_occupancy', 'is_available', 'is_featured', 'show_price_publicly', 'has_ocean_view', 'has_balcony', 'is_suite']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_featured', 'show_price_publicly']
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
            'fields': ('base_price', 'show_price_publicly', 'is_available', 'is_featured'),
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


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'display_order']
    list_editable = ['is_active', 'display_order']
    search_fields = ['name', 'slug']
    ordering = ['display_order', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'featured_categories', 'is_featured', 'created_at']
    list_filter = ['media_type', 'is_featured', 'created_at', 'categories']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'media_type']
    ordering = ['-is_featured', '-created_at']
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'categories', 'is_featured')
        }),
        ('Media Content', {
            'fields': ('media_type', 'image_placeholder', 'video_file', 'video_thumbnail')
        })
    )
    
    def featured_categories(self, obj):
        return ", ".join(obj.categories.values_list('name', flat=True)) or "Uncategorized"
    featured_categories.short_description = "Categories"


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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'published_date', 'created_at']
    list_filter = ['category', 'is_published', 'is_featured', 'published_date', 'created_at']
    search_fields = ['title', 'content', 'author', 'excerpt']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_date', '-created_at']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'excerpt'),
            'description': 'Use the rich text editor to format your blog post. Excerpt is auto-generated if left empty.'
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_date'),
            'description': 'Published date is automatically set when first published.'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(NavigationSettings)
class NavigationSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Primary Links', {
            'fields': ('show_home', 'show_about', 'show_rooms', 'show_amenities', 'show_gallery', 'show_activities', 'show_blog', 'show_contact')
        }),
        ('Booking Button', {
            'fields': ('show_book_button', 'book_button_label', 'book_button_url')
        }),
    )
    list_display = ['__str__', 'updated_at', 'show_book_button']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        if NavigationSettings.objects.exists():
            return False
        return super().has_add_permission(request)


admin.site.site_header = "Banbas Resort Backoffice"
admin.site.site_title = "Banbas Admin"
admin.site.index_title = "Resort Operations Dashboard"
admin.site.site_url = "/"
