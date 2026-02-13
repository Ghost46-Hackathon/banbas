from .models import NavigationSettings, Resort

def navigation_settings(request):
    settings_obj = NavigationSettings.objects.first()
    return {
        'nav_settings': settings_obj
    }


def site_resort_info(request):
    return {
        'resort_info': Resort.objects.first()
    }
