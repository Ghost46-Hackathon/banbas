from .models import NavigationSettings

def navigation_settings(request):
    settings_obj = NavigationSettings.objects.first()
    return {
        'nav_settings': settings_obj
    }
