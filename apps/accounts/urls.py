from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),  
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  
    path('logout/', views.user_logout, name='logout'),
]