import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import RoomType, Amenity, Gallery, Contact, Resort, Activity, Blog, AboutPage
from .forms import ContactForm

logger = logging.getLogger(__name__)


def _client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        forwarded_ips = [ip.strip() for ip in forwarded_for.split(',') if ip.strip()]
        if forwarded_ips:
            # Use the right-most value to reduce spoofing risk when proxies append client IP.
            return forwarded_ips[-1]
    return request.META.get('REMOTE_ADDR', 'unknown')


def _contact_rate_limited(request):
    ip_address = _client_ip(request)
    key = f'contact-rate:{ip_address}'
    current_attempts = cache.get(key, 0)
    max_attempts = settings.CONTACT_RATE_LIMIT_MAX_ATTEMPTS
    window_seconds = settings.CONTACT_RATE_LIMIT_WINDOW_SECONDS

    if current_attempts >= max_attempts:
        return True

    cache.set(key, current_attempts + 1, timeout=window_seconds)
    return False


def _verify_turnstile_token(request, token):
    if not settings.TURNSTILE_ENABLED:
        return True, None

    if not settings.TURNSTILE_SECRET_KEY:
        logger.warning('TURNSTILE_ENABLED is true but TURNSTILE_SECRET_KEY is missing.')
        return False, 'Bot verification is temporarily unavailable.'

    if not token:
        return False, 'Please complete the bot verification challenge.'

    payload = urllib.parse.urlencode({
        'secret': settings.TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': _client_ip(request),
    }).encode('utf-8')

    try:
        req = urllib.request.Request(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data=payload,
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
    except Exception:
        logger.exception('Turnstile verification request failed.')
        return False, 'Could not verify bot challenge. Please try again.'

    if not result.get('success'):
        return False, 'Bot verification failed. Please try again.'

    expected_hostname = settings.TURNSTILE_EXPECTED_HOSTNAME
    response_hostname = result.get('hostname')
    if expected_hostname and response_hostname != expected_hostname:
        logger.warning(
            'Turnstile hostname mismatch. expected=%s got=%s',
            expected_hostname,
            response_hostname,
        )
        return False, 'Invalid verification response.'

    return True, None


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
    
    # Define categories with proper display names
    categories = [
        {'slug': 'rooms', 'name': 'Rooms'},
        {'slug': 'amenities', 'name': 'Amenities'},
        {'slug': 'dining', 'name': 'Dining'},
        {'slug': 'exterior', 'name': 'Exterior'},
        {'slug': 'activities', 'name': 'Activities'},
    ]
    
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
    form_kwargs = {
        'enable_turnstile': settings.TURNSTILE_ENABLED,
        'min_submit_seconds': settings.CONTACT_MIN_SUBMIT_SECONDS,
    }

    if request.method == 'POST':
        if _contact_rate_limited(request):
            messages.error(
                request,
                'Too many inquiry attempts. Please wait a few minutes before trying again.',
            )
            form = ContactForm(request.POST, **form_kwargs)
        else:
            form = ContactForm(request.POST, **form_kwargs)

            if form.is_valid():
                verified, error_message = _verify_turnstile_token(
                    request,
                    form.cleaned_data.get('turnstile_token'),
                )
                if not verified:
                    form.add_error(None, error_message)
                else:
                    form.save()
                    messages.success(request, 'Thank you for your message! We will get back to you soon.')
                    return redirect('resort:contact')
    else:
        form = ContactForm(**form_kwargs)
    
    context = {
        'form': form,
        'resort': resort,
        'turnstile_enabled': settings.TURNSTILE_ENABLED,
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY,
    }
    return render(request, 'resort/contact.html', context)


def about(request):
    """About page - Admin-managed content"""
    page = AboutPage.objects.first()
    resort = Resort.objects.first()
    
    # If no about page exists, create a default one
    if not page:
        page = AboutPage.objects.create()
    
    context = {
        'page': page,
        'resort': resort,
    }
    return render(request, 'resort/about_admin.html', context)


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


def blog_list(request):
    """Blog listing page"""
    category = request.GET.get('category', 'all')
    
    # Only show published blog posts
    if category == 'all':
        blog_posts = Blog.objects.filter(is_published=True)
    else:
        blog_posts = Blog.objects.filter(is_published=True, category=category)
    
    # Get all categories for filter buttons
    categories = Blog.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    
    paginator = Paginator(blog_posts, 9)  # Show 9 blog posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'blog_posts': page_obj,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'resort/blog_list.html', context)


def blog_detail(request, slug):
    """Individual blog post detail page"""
    blog_post = get_object_or_404(Blog, slug=slug, is_published=True)
    related_posts = Blog.objects.filter(is_published=True).exclude(slug=slug)[:3]
    resort = Resort.objects.first()
    
    context = {
        'blog_post': blog_post,
        'related_posts': related_posts,
        'resort': resort,
    }
    return render(request, 'resort/blog_detail.html', context)
