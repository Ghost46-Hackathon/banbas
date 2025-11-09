from django.core.management.base import BaseCommand
from resort.models import Resort, RoomType, Amenity, Gallery, Contact


class Command(BaseCommand):
    help = 'Populate the database with sample data for Banbas Resort'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating sample data for Banbas Resort...'))

        # Create or update resort information
        resort, created = Resort.objects.get_or_create(
            defaults={
                'name': 'Banbas Resort',
                'tagline': 'Your Paradise Awaits',
                'description': 'Experience luxury and comfort at Banbas Resort, where every moment is designed to create unforgettable memories. Our world-class amenities and stunning oceanfront location provide the perfect escape from everyday life.',
                'address': '123 Paradise Beach Avenue\nTropical Island, TI 12345\nParadise Islands',
                'phone': '+1 (555) 123-4567',
                'email': 'info@banbasresort.com',
                'website': 'https://www.banbasresort.com',
                'hero_image_placeholder': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1920&q=80',
                'facebook_url': 'https://facebook.com/banbasresort',
                'instagram_url': 'https://instagram.com/banbasresort',
                'twitter_url': 'https://twitter.com/banbasresort',
            }
        )
        
        if created:
            self.stdout.write('[OK] Resort information created')
        else:
            self.stdout.write('[OK] Resort information already exists')

        # Create Room Types
        rooms_data = [
            {
                'name': 'Ocean View Suite',
                'description': 'Luxurious suite with breathtaking ocean views, featuring a spacious living area, private balcony, and premium amenities. Perfect for couples seeking romance and tranquility.',
                'base_price': 450.00,
                'max_occupancy': 2,
                'size_sqm': 65,
                'amenities': 'King bed, Ocean view, Private balcony, Mini bar, Room service, WiFi, Air conditioning, Safe',
                'image_placeholder': 'https://via.placeholder.com/400x300/134a39/ffffff?text=Ocean+View+Suite'
            },
            {
                'name': 'Deluxe Garden Room',
                'description': 'Elegant room overlooking our tropical gardens, offering comfort and serenity. Features modern furnishings and access to garden terraces.',
                'base_price': 280.00,
                'max_occupancy': 3,
                'size_sqm': 45,
                'amenities': 'Queen bed, Garden view, Terrace access, Mini fridge, WiFi, Air conditioning, Safe',
                'image_placeholder': 'https://via.placeholder.com/400x300/28a745/ffffff?text=Garden+Room'
            },
            {
                'name': 'Presidential Villa',
                'description': 'Our most exclusive accommodation featuring a private pool, personal butler service, and unparalleled luxury. The ultimate in resort living.',
                'base_price': 1200.00,
                'max_occupancy': 6,
                'size_sqm': 150,
                'amenities': 'Master bedroom, Private pool, Butler service, Kitchen, Living room, Multiple balconies, Premium bar, WiFi, Air conditioning',
                'image_placeholder': 'https://via.placeholder.com/400x300/dc3545/ffffff?text=Presidential+Villa'
            },
            {
                'name': 'Beach Cabana',
                'description': 'Charming beachfront accommodation with direct beach access. Wake up to the sound of waves and enjoy unobstructed sunrise views.',
                'base_price': 380.00,
                'max_occupancy': 4,
                'size_sqm': 55,
                'amenities': 'Beach access, Sunrise view, Outdoor shower, Hammock, Mini bar, WiFi, Air conditioning, Safe',
                'image_placeholder': 'https://via.placeholder.com/400x300/1e6b54/ffffff?text=Beach+Cabana'
            },
            {
                'name': 'Family Paradise Room',
                'description': 'Spacious accommodation perfect for families, featuring connecting rooms, child-friendly amenities, and easy access to family activities.',
                'base_price': 320.00,
                'max_occupancy': 5,
                'size_sqm': 70,
                'amenities': 'Two bedrooms, Connecting rooms, Kids amenities, Family balcony, Mini kitchen, WiFi, Air conditioning, Safe',
                'image_placeholder': 'https://via.placeholder.com/400x300/ffc107/ffffff?text=Family+Room'
            }
        ]

        for room_data in rooms_data:
            room, created = RoomType.objects.get_or_create(
                name=room_data['name'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f'[OK] Created room: {room.name}')

        # Create Amenities
        amenities_data = [
            {
                'name': 'Infinity Pool',
                'description': 'Our stunning infinity pool offers breathtaking ocean views and is perfect for relaxation and swimming. Open 24/7 with poolside service available.',
                'icon_class': 'fas fa-swimming-pool',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/300x200/134a39/ffffff?text=Infinity+Pool'
            },
            {
                'name': 'Luxury Spa',
                'description': 'Indulge in our world-class spa featuring massage therapy, facial treatments, and wellness programs designed to rejuvenate your body and mind.',
                'icon_class': 'fas fa-spa',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Luxury+Spa'
            },
            {
                'name': 'Gourmet Restaurant',
                'description': 'Experience fine dining with our award-winning chef\'s creative cuisine. Features fresh local ingredients and international flavors.',
                'icon_class': 'fas fa-utensils',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/300x200/dc3545/ffffff?text=Gourmet+Restaurant'
            },
            {
                'name': 'Fitness Center',
                'description': 'Stay active during your vacation with our modern fitness center, featuring state-of-the-art equipment and personal training services.',
                'icon_class': 'fas fa-dumbbell',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/300x200/1e6b54/ffffff?text=Fitness+Center'
            },
            {
                'name': 'Beach Bar',
                'description': 'Enjoy tropical cocktails and light snacks at our beachfront bar. Perfect for sunset drinks and casual dining with your toes in the sand.',
                'icon_class': 'fas fa-cocktail',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/300x200/ffc107/ffffff?text=Beach+Bar'
            },
            {
                'name': 'Water Sports',
                'description': 'Adventure awaits with our comprehensive water sports program including kayaking, snorkeling, jet skiing, and sailing.',
                'icon_class': 'fas fa-ship',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/300x200/6f42c1/ffffff?text=Water+Sports'
            },
            {
                'name': 'Kids Club',
                'description': 'Fun-filled activities and supervised programs for children aged 4-12. Games, crafts, and educational activities in a safe environment.',
                'icon_class': 'fas fa-child',
                'is_featured': False,
                'image_placeholder': 'https://via.placeholder.com/300x200/fd7e14/ffffff?text=Kids+Club'
            },
            {
                'name': 'Business Center',
                'description': 'Full-service business center with high-speed internet, printing facilities, and meeting rooms for business travelers.',
                'icon_class': 'fas fa-briefcase',
                'is_featured': False,
                'image_placeholder': 'https://via.placeholder.com/300x200/6c757d/ffffff?text=Business+Center'
            }
        ]

        for amenity_data in amenities_data:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_data['name'],
                defaults=amenity_data
            )
            if created:
                self.stdout.write(f'[OK] Created amenity: {amenity.name}')

        # Create Gallery Items
        gallery_data = [
            {
                'title': 'Resort Exterior',
                'description': 'Beautiful exterior view of our main resort building',
                'category': 'exterior',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/600x400/134a39/ffffff?text=Resort+Exterior'
            },
            {
                'title': 'Infinity Pool Paradise',
                'description': 'Our stunning infinity pool with ocean backdrop',
                'category': 'amenities',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/600x400/1e6b54/ffffff?text=Pool+Paradise'
            },
            {
                'title': 'Ocean View Suite Interior',
                'description': 'Luxurious interior of our Ocean View Suite',
                'category': 'rooms',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/600x400/28a745/ffffff?text=Suite+Interior'
            },
            {
                'title': 'Gourmet Dining Experience',
                'description': 'Fine dining at our award-winning restaurant',
                'category': 'dining',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/600x400/dc3545/ffffff?text=Fine+Dining'
            },
            {
                'title': 'Beach Activities',
                'description': 'Water sports and beach activities',
                'category': 'activities',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/600x400/ffc107/ffffff?text=Beach+Activities'
            },
            {
                'title': 'Spa Relaxation',
                'description': 'Peaceful spa treatment room',
                'category': 'amenities',
                'is_featured': True,
                'image_placeholder': 'https://via.placeholder.com/600x400/6f42c1/ffffff?text=Spa+Relaxation'
            },
            {
                'title': 'Sunset Beach View',
                'description': 'Breathtaking sunset from our private beach',
                'category': 'exterior',
                'is_featured': False,
                'image_placeholder': 'https://via.placeholder.com/600x400/fd7e14/ffffff?text=Sunset+Beach'
            },
            {
                'title': 'Presidential Villa Pool',
                'description': 'Private pool at the Presidential Villa',
                'category': 'rooms',
                'is_featured': False,
                'image_placeholder': 'https://via.placeholder.com/600x400/20c997/ffffff?text=Villa+Pool'
            }
        ]

        for gallery_item_data in gallery_data:
            gallery_item, created = Gallery.objects.get_or_create(
                title=gallery_item_data['title'],
                defaults=gallery_item_data
            )
            if created:
                self.stdout.write(f'[OK] Created gallery item: {gallery_item.title}')

        # Create some sample contact messages
        sample_contacts = [
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@email.com',
                'phone': '+1 (555) 987-6543',
                'subject': 'Wedding Venue Inquiry',
                'message': 'Hello! I\'m planning my wedding and would love to know more about your wedding packages and venues. Could someone please contact me with details about availability for next summer?',
                'is_read': False
            },
            {
                'name': 'Michael Chen',
                'email': 'michael.chen@business.com',
                'phone': '+1 (555) 456-7890',
                'subject': 'Corporate Retreat Booking',
                'message': 'We are looking for a location for our annual corporate retreat for 50 people. Please send information about group rates and meeting facilities.',
                'is_read': True
            }
        ]

        for contact_data in sample_contacts:
            contact, created = Contact.objects.get_or_create(
                email=contact_data['email'],
                subject=contact_data['subject'],
                defaults=contact_data
            )
            if created:
                self.stdout.write(f'[OK] Created contact message from: {contact.name}')

        self.stdout.write(self.style.SUCCESS('\nSample data population completed successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now access the website and admin panel.'))
        self.stdout.write(self.style.WARNING('Admin credentials: admin / admin'))