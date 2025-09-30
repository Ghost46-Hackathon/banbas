#!/usr/bin/env python
"""
Script to populate sample activities for Banbas Resort.
Run with: python manage.py shell < populate_activities.py
"""

from resort.models import Activity

# Sample activities data
activities_data = [
    {
        'name': 'Safari Game Drive',
        'short_description': 'Explore wildlife in their natural habitat with our expert guides.',
        'full_description': 'Embark on an unforgettable safari adventure through the wilderness. Our experienced guides will take you on a journey to spot the Big Five and other incredible wildlife species. Perfect for nature lovers and photography enthusiasts.',
        'category': 'adventure',
        'difficulty': 'moderate',
        'duration': '4-6 hours',
        'max_participants': 8,
        'min_age': 12,
        'price': 120.00,
        'icon_class': 'fas fa-binoculars',
        'image_placeholder': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'background_color': '#8B4513',
        'is_featured': True,
        'requires_booking': True,
        'includes_equipment': True,
        'includes_guide': True,
        'includes_transport': True,
        'location': 'Game Reserve',
        'what_to_bring': 'Sunscreen, Hat, Camera, Comfortable shoes',
        'included_items': 'Binoculars, Refreshments, Transport, Professional guide'
    },
    {
        'name': 'Ocean Kayaking',
        'short_description': 'Paddle through crystal clear waters and explore hidden coves.',
        'full_description': 'Discover the stunning coastline from a unique perspective. Glide through pristine waters, explore secluded beaches, and enjoy the tranquility of the ocean. Suitable for beginners and experienced paddlers alike.',
        'category': 'water_sports',
        'difficulty': 'easy',
        'duration': '2-3 hours',
        'max_participants': 12,
        'min_age': 8,
        'price': 75.00,
        'icon_class': 'fas fa-swimmer',
        'image_placeholder': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'background_color': '#20B2AA',
        'is_featured': True,
        'requires_booking': True,
        'includes_equipment': True,
        'includes_guide': True,
        'includes_transport': False,
        'location': 'Resort Beach',
        'what_to_bring': 'Swimwear, Sunscreen, Towel, Water bottle',
        'included_items': 'Kayak, Paddle, Life jacket, Safety briefing'
    },
    {
        'name': 'Sunset Yoga',
        'short_description': 'Find inner peace with yoga sessions at sunset on the beach.',
        'full_description': 'Unwind and connect with nature during our peaceful sunset yoga sessions. Practice gentle flows and meditation techniques while enjoying breathtaking ocean views and the golden hour ambiance.',
        'category': 'wellness',
        'difficulty': 'easy',
        'duration': '1 hour',
        'max_participants': 20,
        'min_age': 14,
        'price': 35.00,
        'icon_class': 'fas fa-spa',
        'image_placeholder': 'https://images.unsplash.com/photo-1506629905496-37ca7ca52160?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'background_color': '#9370DB',
        'is_featured': True,
        'requires_booking': True,
        'includes_equipment': True,
        'includes_guide': True,
        'includes_transport': False,
        'location': 'Beach Pavilion',
        'what_to_bring': 'Comfortable clothing, Water bottle',
        'included_items': 'Yoga mat, Meditation cushions, Herbal tea'
    },
    {
        'name': 'Gourmet Cooking Class',
        'short_description': 'Learn to prepare local delicacies with our professional chefs.',
        'full_description': 'Dive into the culinary traditions of the region with hands-on cooking classes. Learn to prepare authentic local dishes using fresh, organic ingredients sourced from local markets and our own gardens.',
        'category': 'dining',
        'difficulty': 'easy',
        'duration': '3 hours',
        'max_participants': 10,
        'min_age': 16,
        'price': 95.00,
        'icon_class': 'fas fa-utensils',
        'image_placeholder': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'background_color': '#FF6347',
        'is_featured': True,
        'requires_booking': True,
        'includes_equipment': True,
        'includes_guide': True,
        'includes_transport': False,
        'location': 'Resort Kitchen',
        'what_to_bring': 'Appetite for learning, Comfortable clothes',
        'included_items': 'All ingredients, Cooking equipment, Recipe cards, Lunch'
    },
    {
        'name': 'Live Music Evening',
        'short_description': 'Enjoy live performances by local musicians under the stars.',
        'full_description': 'Experience the vibrant local music scene with intimate performances by talented regional artists. Enjoy traditional and contemporary music in a beautiful outdoor setting with premium drinks and light snacks.',
        'category': 'entertainment',
        'difficulty': 'easy',
        'duration': '2-3 hours',
        'max_participants': 50,
        'min_age': 0,
        'price': 45.00,
        'icon_class': 'fas fa-music',
        'image_placeholder': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'background_color': '#FFD700',
        'is_featured': True,
        'requires_booking': True,
        'includes_equipment': False,
        'includes_guide': False,
        'includes_transport': False,
        'location': 'Garden Amphitheater',
        'what_to_bring': 'Just yourself and good vibes',
        'included_items': 'Welcome drink, Light snacks, Premium seating'
    },
    {
        'name': 'Cultural Village Tour',
        'short_description': 'Immerse yourself in local culture and traditional crafts.',
        'full_description': 'Discover the rich cultural heritage of the region with guided visits to traditional villages. Meet local artisans, learn about ancient crafts, and participate in cultural ceremonies and dances.',
        'category': 'cultural',
        'difficulty': 'easy',
        'duration': 'Half day',
        'max_participants': 15,
        'min_age': 8,
        'price': 85.00,
        'icon_class': 'fas fa-home',
        'image_placeholder': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'background_color': '#CD853F',
        'is_featured': True,
        'requires_booking': True,
        'includes_equipment': False,
        'includes_guide': True,
        'includes_transport': True,
        'location': 'Local Villages',
        'what_to_bring': 'Comfortable walking shoes, Camera, Respectful attitude',
        'included_items': 'Cultural guide, Transport, Traditional lunch, Craft demonstration'
    },
]

print("Populating activities...")

for activity_data in activities_data:
    activity, created = Activity.objects.get_or_create(
        name=activity_data['name'],
        defaults=activity_data
    )
    if created:
        print(f"Created: {activity.name}")
    else:
        print(f"Already exists: {activity.name}")

print(f"Total activities in database: {Activity.objects.count()}")
print(f"Featured activities: {Activity.objects.filter(is_featured=True).count()}")
print("Done!")