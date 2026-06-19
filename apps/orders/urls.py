from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path("orders/", views.customer_orders, name="customer_orders"),
    path("new-order/", views.new_order, name="new_order"),
    path('place-order/', views.place_order, name="place_order"),
    
    path("orders/assign-driver/<int:order_id>/", views.assign_driver, name="assign_driver"),
    
    path("driver/dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path("driver/my-deliveries/", views.my_deliveries, name="my_deliveries"),
    path("driver/delivery/<int:id>/", views.delivery_detail, name="delivery_detail"),
    path("driver/update-status/<int:id>/", views.update_delivery_status, name="update_delivery_status"),
    path("driver/profile/", views.driver_profile, name="driver_profile"),
    path("driver/profile/update/", views.update_driver_profile, name="update_driver_profile"),
    path("driver/available-orders/", views.available_orders, name="available_orders"),
    path("driver/deliveryhistory/", views.delivery_history, name="delivery_history"),
    path("driver/claim-order/<int:order_id/", views.claim_order, name="claim_order"),
    
    
    
    
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.customer_profile, name="customer_profile"),
    
    path("track-order/<int:id>/", views.track_order, name="track_order"),
    
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    

   
    
    
    
    
    
]