from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'orders/home.html')

def orders(request):
    return render(request, 'dashboard/customerdashboard/orders.html')

def new_order(request):
    return render(request, 'dashboard/customerdashboard/new_order.html')

def notifications(request):
    return render(request, 'dashboard/customerdashboard/notifications.html')

def profile(request):
    return render(request, 'dashboard/customerdashboard/profile.html')

def place_order(request):
    return render(request, 'dashboard/customerdashboard/new_order.html')

def update_profile(request):
    return render(request, '')

def change_password(request):
    return render(request, '')

def delete_account(request):
    return render(request, '')

def driver_profile(request):
    return render(request, 'dashboard/driverdashboard/driver_profile.html')

def my_deliveries(request):
    return render(request, 'dashboard/driverdashboard/my_deliveries.html')

def available_orders(request):
    return render(request, 'dashboard/driverdashboard/available_orders.html')

def delivery_detail(request, id):
    return render(request, 'dashboard/driverdashboard/delivery_detail.html')

def update_status(request):
    return render(request, '')

def notifications(request):
    return render(request, '')

def profile(request):
    return render(request, '')

def delivery_history(request):
    context = {
        'history': []
    }
    return render(request, 'dashboard/driverdashboard/history.html', context)

