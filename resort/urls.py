from django.urls import path
from . import views

app_name = 'resort'

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('amenities/', views.amenities, name='amenities'),
    path('activities/', views.activities_list, name='activities_list'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
