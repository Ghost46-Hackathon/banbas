from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import admin_required

app_name = 'backoffice'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='backoffice/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/_internal/login/'), name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Reservations
    path('reservations/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservations/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/<int:pk>/edit/', views.ReservationEditView.as_view(), name='reservation_edit'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    
    # Contact Inquiries
    path('inquiries/', views.ContactInquiryListView.as_view(), name='inquiry_list'),
    path('inquiries/<int:pk>/', views.ContactInquiryDetailView.as_view(), name='inquiry_detail'),
    path('inquiries/<int:pk>/convert/', views.ConvertInquiryView.as_view(), name='convert_inquiry'),
    
    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    
    # User Management (Admin only) - Double protected with AdminRequiredMixin + decorator
    path('users/', admin_required(views.UserListView.as_view()), name='user_list'),
    path('users/create/', admin_required(views.UserCreateView.as_view()), name='user_create'),
    path('users/<int:pk>/edit/', admin_required(views.UserEditView.as_view()), name='user_edit'),
]