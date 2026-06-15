from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('orders/', views.orders, name='orders'),
    path('new-order/', views.new_order, name='new_order'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('place-order/', views.place_order, name='place_order'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    path('driver/profile/', views.driver_profile, name='driver_profile'),
    path('driver/deliveries/', views.my_deliveries, name='my_deliveries'),
    path('driver/available/', views.available_orders, name='available_orders'),
    
    path('driver/delivery/<int:id>/', views.delivery_detail, name='delivery_detail'),
    path('driver/update/<int:id>/', views.update_status, name='update_status'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile', views.profile, name='profile'),
    
]