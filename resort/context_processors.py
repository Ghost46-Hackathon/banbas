from .models import NavigationSettings, Resort


def navigation_settings(request):
    """Provide navigation configuration to all templates."""
    settings_obj, _ = NavigationSettings.objects.get_or_create(
        pk=1,
        defaults={
            'book_button_url': '/contact/',
        }
    )
    return {'nav_settings': settings_obj}


def site_resort_info(request):
    """Provide shared resort contact details (address/phone/email) to all templates."""
    return {'resort_info': Resort.objects.first()}
