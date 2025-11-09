from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="Brief description for room cards")
    detailed_description = RichTextField(config_name='default', blank=True, help_text="Rich text content for room detail page")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price per night (for admin reference only)")
    show_price_publicly = models.BooleanField(default=False, help_text="Toggle to display the price badge on the public rooms page")
    max_occupancy = models.IntegerField()
    size_sqm = models.IntegerField(help_text="Size in square meters")
    room_count = models.IntegerField(default=1, help_text="Number of available rooms of this type")
    amenities = models.TextField(help_text="Comma-separated amenities")
    
    # Media
    main_image = models.CharField(max_length=300, default="https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", help_text="Main room image URL")
    
    # Features
    has_balcony = models.BooleanField(default=False)
    has_ocean_view = models.BooleanField(default=False)
    has_garden_view = models.BooleanField(default=False)
    has_kitchenette = models.BooleanField(default=False)
    has_jacuzzi = models.BooleanField(default=False)
    is_suite = models.BooleanField(default=False)
    
    # Availability
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured rooms section")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['base_price']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resort:room_detail', kwargs={'pk': self.pk})
    
    def get_amenities_list(self):
        """Return list of amenities"""
        return [amenity.strip() for amenity in self.amenities.split(',') if amenity.strip()]
    
    def get_features_list(self):
        """Return list of room features based on boolean fields"""
        features = []
        if self.has_balcony:
            features.append('Private Balcony')
        if self.has_ocean_view:
            features.append('Ocean View')
        if self.has_garden_view:
            features.append('Garden View')
        if self.has_kitchenette:
            features.append('Kitchenette')
        if self.has_jacuzzi:
            features.append('Private Jacuzzi')
        if self.is_suite:
            features.append('Suite Layout')
        return features


class RoomGallery(models.Model):
    """Room photo and video gallery"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='gallery_items')
    title = models.CharField(max_length=100, blank=True, help_text="Optional title for the media item")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image_url = models.CharField(max_length=300, blank=True, help_text="Image URL")
    video_url = models.CharField(max_length=300, blank=True, help_text="Video URL (YouTube, Vimeo, or direct)")
    video_thumbnail = models.CharField(max_length=300, blank=True, help_text="Video thumbnail image URL")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    is_featured = models.BooleanField(default=False, help_text="Feature this image in room cards")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Room Gallery"
    
    def __str__(self):
        return f"{self.room_type.name} - {self.get_media_type_display()} {self.id}"
    
    def get_display_url(self):
        """Return the appropriate URL for display"""
        if self.media_type == 'video':
            return self.video_thumbnail or self.video_url
        return self.image_url


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


class Activity(models.Model):
    """Resort Activities Model"""
    ACTIVITY_CATEGORIES = [
        ('adventure', 'Adventure'),
        ('water_sports', 'Water Sports'),
        ('wellness', 'Wellness & Spa'),
        ('dining', 'Dining'),
        ('entertainment', 'Entertainment'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('nature', 'Nature'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100, help_text="Activity name")
    short_description = models.CharField(max_length=200, help_text="Brief description for cards")
    full_description = models.TextField(help_text="Detailed activity description")
    detailed_content = RichTextField(config_name='activity_content', blank=True, help_text="Rich text content for activity detail page")
    category = models.CharField(max_length=20, choices=ACTIVITY_CATEGORIES, default='adventure')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_LEVELS, default='easy')
    duration = models.CharField(max_length=50, help_text="e.g., '2-3 hours', 'Full day', 'Half day'")
    max_participants = models.IntegerField(default=10, help_text="Maximum number of participants")
    min_age = models.IntegerField(default=0, help_text="Minimum age requirement (0 for no restriction)")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price per person")
    
    # Visual elements
    icon_class = models.CharField(max_length=50, default="fas fa-star", help_text="Font Awesome icon class (e.g., fas fa-swimming-pool)")
    image_placeholder = models.CharField(
        max_length=300, 
        default="https://images.unsplash.com/photo-1544197150-b99a580bb7a8?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        help_text="Activity image URL"
    )
    background_color = models.CharField(max_length=7, default="#134a39", help_text="Hex color for card background")
    
    # Availability and features
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured activities section")
    requires_booking = models.BooleanField(default=True)
    includes_equipment = models.BooleanField(default=False)
    includes_guide = models.BooleanField(default=False)
    includes_transport = models.BooleanField(default=False)
    
    # Scheduling
    available_days = models.CharField(
        max_length=100, 
        default="Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday",
        help_text="Comma-separated days of the week"
    )
    available_times = models.CharField(
        max_length=200,
        default="9:00 AM,2:00 PM",
        help_text="Comma-separated available start times"
    )
    
    # SEO and additional info
    location = models.CharField(max_length=100, blank=True, help_text="Activity location")
    what_to_bring = models.TextField(blank=True, help_text="What participants should bring")
    included_items = models.TextField(blank=True, help_text="What's included in the activity")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-is_featured', '-is_available', 'category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def get_absolute_url(self):
        return reverse('resort:activity_detail', kwargs={'pk': self.pk})
    
    def get_available_days_list(self):
        """Return list of available days"""
        return [day.strip() for day in self.available_days.split(',') if day.strip()]
    
    def get_available_times_list(self):
        """Return list of available times"""
        return [time.strip() for time in self.available_times.split(',') if time.strip()]
    
    def get_included_items_list(self):
        """Return list of included items"""
        return [item.strip() for item in self.included_items.split(',') if item.strip()]
    
    def get_what_to_bring_list(self):
        """Return list of items to bring"""
        return [item.strip() for item in self.what_to_bring.split(',') if item.strip()]


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"

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
    image_placeholder = models.CharField(max_length=200, default="https://via.placeholder.com/600x400/1e6b54/ffffff?text=Gallery+Image")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Upload video file (MP4 recommended)")
    video_thumbnail = models.CharField(max_length=200, blank=True, help_text="Thumbnail image URL for video")
    categories = models.ManyToManyField(GalleryCategory, blank=True, related_name='gallery_items', help_text="Select one or more categories for filtering on the gallery page.")
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


class Blog(models.Model):
    """Blog post model with rich text editor"""
    CATEGORY_CHOICES = [
        ('resort', 'Resort News'),
        ('travel', 'Travel Tips'),
        ('local', 'Local Attractions'),
        ('food', 'Food & Dining'),
        ('events', 'Events'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200, help_text="Blog post title")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly version of title")
    content = RichTextField(config_name='default', help_text="Blog post content with rich text formatting")
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short description for blog list (auto-generated if empty)")
    author = models.CharField(max_length=100, default="Banbas Resort", help_text="Author name")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    featured_image = models.CharField(
        max_length=300,
        default="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        help_text="Featured image URL for the blog post"
    )
    
    # Publishing
    is_published = models.BooleanField(default=False, help_text="Publish this blog post")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    published_date = models.DateTimeField(blank=True, null=True, help_text="Date to publish (leave blank for now)")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('resort:blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            from django.utils.html import strip_tags
            plain_content = strip_tags(self.content)
            self.excerpt = plain_content[:297] + '...' if len(plain_content) > 300 else plain_content
        
        # Set published_date if publishing for the first time
        if self.is_published and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)


class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="OUR STORY")
    subtitle = models.CharField(max_length=300, default="Story Behind Banbas | Sustainability | Chitwan National Park")
    founders_narrative_title = models.CharField(max_length=200, default="Bashu Dhungana's Life Work")
    founders_narrative_content = RichTextField(config_name='default', blank=True)
    founders_narrative_image = models.CharField(max_length=300, default="https://www.banbasresort.com/static/img/b.jpg")
    management_partnership_title = models.CharField(max_length=200, default="Management Partnership")
    management_partnership_content = RichTextField(config_name='default', blank=True)
    management_partnership_image = models.CharField(max_length=300, default="https://www.banbasresort.com/static/img/c.jpg")
    vision_and_design_title = models.CharField(max_length=200, default="Vision and Design")
    vision_and_design_content = RichTextField(config_name='default', blank=True)
    vision_and_design_image = models.CharField(max_length=300, default="https://www.banbasresort.com/static/img/a.jpg")
    main_image = models.CharField(max_length=300, default="https://images.unsplash.com/photo-1516426122078-c23e76319801?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80")
    secondary_image = models.CharField(max_length=300, default="https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About Page"


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
        default="https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1920&q=80"
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


class NavigationSettings(models.Model):
    """Control visibility of header navigation items and booking button."""
    show_home = models.BooleanField(default=True)
    show_about = models.BooleanField(default=True)
    show_rooms = models.BooleanField(default=True)
    show_amenities = models.BooleanField(default=True)
    show_gallery = models.BooleanField(default=True)
    show_blog = models.BooleanField(default=True)
    show_contact = models.BooleanField(default=True)
    show_activities = models.BooleanField(default=True)
    book_button_label = models.CharField(max_length=50, default="Book A Stay")
    book_button_url = models.CharField(max_length=200, default="/contact/")
    show_book_button = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Navigation Settings"
        verbose_name_plural = "Navigation Settings"

    def __str__(self):
        return "Site Navigation Configuration"
