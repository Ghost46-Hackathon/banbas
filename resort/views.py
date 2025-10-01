from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import RoomType, Amenity, Gallery, Contact, Resort, Activity
from .forms import ContactForm


def home(request):
    """Home page with hero section and featured content"""
    resort = Resort.objects.first()
    featured_rooms = RoomType.objects.filter(is_available=True, is_featured=True)[:3]
    if featured_rooms.count() < 3:
        # If not enough featured rooms, fill with available rooms
        additional_rooms = RoomType.objects.filter(is_available=True).exclude(
            pk__in=featured_rooms.values_list('pk', flat=True)
        )[:3-featured_rooms.count()]
        featured_rooms = list(featured_rooms) + list(additional_rooms)
    
    featured_amenities = Amenity.objects.filter(is_featured=True)[:6]
    featured_gallery = Gallery.objects.filter(is_featured=True)[:6]
    featured_activities = Activity.objects.filter(is_featured=True, is_available=True)[:6]
    
    context = {
        'resort': resort,
        'featured_rooms': featured_rooms,
        'featured_amenities': featured_amenities,
        'featured_gallery': featured_gallery,
        'featured_activities': featured_activities,
    }
    return render(request, 'resort/home.html', context)


def rooms(request):
    """Rooms listing page"""
    rooms = RoomType.objects.filter(is_available=True)
    paginator = Paginator(rooms, 6)  # Show 6 rooms per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'rooms': page_obj,
    }
    return render(request, 'resort/rooms.html', context)


def room_detail(request, pk):
    """Individual room detail page"""
    room = get_object_or_404(RoomType, pk=pk, is_available=True)
    gallery_items = room.gallery_items.all()
    gallery_images = gallery_items.filter(media_type='image')
    gallery_videos = gallery_items.filter(media_type='video')
    related_rooms = RoomType.objects.filter(is_available=True).exclude(pk=pk)[:3]
    resort = Resort.objects.first()
    
    context = {
        'room': room,
        'gallery_images': gallery_images,
        'gallery_videos': gallery_videos,
        'related_rooms': related_rooms,
        'resort': resort,
    }
    return render(request, 'resort/room_detail.html', context)


def amenities(request):
    """Amenities page"""
    amenities = Amenity.objects.all()
    featured_amenities = amenities.filter(is_featured=True)
    regular_amenities = amenities.filter(is_featured=False)
    
    context = {
        'featured_amenities': featured_amenities,
        'regular_amenities': regular_amenities,
        'all_amenities': amenities,
    }
    return render(request, 'resort/amenities.html', context)


def gallery(request):
    """Gallery page with filtering"""
    category = request.GET.get('category', 'all')
    
    if category == 'all':
        gallery_items = Gallery.objects.all()
    else:
        gallery_items = Gallery.objects.filter(category=category)
    
    # Get all categories for filter buttons
    categories = Gallery.objects.values_list('category', flat=True).distinct()
    
    paginator = Paginator(gallery_items, 12)  # Show 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'gallery_items': page_obj,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'resort/gallery.html', context)


def contact(request):
    """Contact page with form"""
    resort = Resort.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Conditional server-side validation: require check-in date for booking inquiries
        if request.POST.get('inquiry_type') == 'booking' and not request.POST.get('preferred_checkin'):
            form.add_error('preferred_checkin', 'Please select a check-in date for booking inquiries.')
        if form.is_valid():
            contact_entry = form.save()
            # Send automated acknowledgment email to guest
            try:
                guest_name = form.cleaned_data.get('name', '').strip() or 'Guest'
                guest_email = form.cleaned_data.get('email')
                subject = f"Thanks, {guest_name}! We've received your inquiry"
                message = render_to_string('email/auto_reply.txt', {
                    'name': guest_name,
                })
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[guest_email],
                    fail_silently=True,
                )
            except Exception:
                # Avoid breaking UX if email fails
                pass
            messages.success(request, 'Thank you for your message! We will get back to you shortly.')
            return redirect('resort:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'resort': resort,
    }
    return render(request, 'resort/contact.html', context)


def about(request):
    """About page"""
    resort = Resort.objects.first()
    amenities = Amenity.objects.filter(is_featured=True)[:4]
    
    context = {
        'resort': resort,
        'amenities': amenities,
    }
    return render(request, 'resort/about.html', context)


def activity_detail(request, pk):
    """Individual activity detail page"""
    activity = get_object_or_404(Activity, pk=pk, is_available=True)
    related_activities = Activity.objects.filter(is_available=True).exclude(pk=pk)[:3]
    resort = Resort.objects.first()
    
    context = {
        'activity': activity,
        'related_activities': related_activities,
        'resort': resort,
    }
    return render(request, 'resort/activity_detail.html', context)
