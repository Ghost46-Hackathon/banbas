from .models import NavigationSettings


def navigation_settings(request):
    """Provide navigation configuration to all templates."""
    settings_obj, _ = NavigationSettings.objects.get_or_create(
        pk=1,
        defaults={
            'book_button_url': '/contact/',
        }
    )
    return {'nav_settings': settings_obj}
