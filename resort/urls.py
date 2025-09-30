from django.urls import path
from . import views

app_name = 'resort'

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('amenities/', views.amenities, name='amenities'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
]
