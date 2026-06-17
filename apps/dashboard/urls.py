from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/customers/', views.admin_customers, name='admin_customers'),
    path('admin/drivers/', views.admin_drivers, name='admin_drivers'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    path('orders/assign-driver/', views.assign_driver, name='assign_driver'),
    path('admin/update-profile/', views.admin_update_profile, name='admin_update_profile'),
    path('admin/save-settings/', views.admin_save_settings, name='admin_save_settings'),
    path('admin/save-pricing/', views.admin_save_pricing, name='admin_save_pricing'),
    path("drivers/add/", views.add_driver, name="add_driver"),
    
    
    
]


