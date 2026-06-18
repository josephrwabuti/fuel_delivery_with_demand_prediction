from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required



@login_required
def place_order(request):
    if request.method == "POST":
        
        Order.objects.create(
            user = request.user,
            fuel_type = fuel_type,
            quantity = quantity, 
            delivery_address = delivery_address,
            delivery_date = delivery_date,
            time_slot = time_slot,
            instructions = instructions
        )
        
        fuel_type = request.POST.get("fuel_type")
        quantity = request.POST.get("quantity")
        delivery_address = request.POST.get("delivery_address")
        delivery_date = request.POST.get("delivery_date")
        time_slot = request.POST.get("time_slot")
        instructions = request.POST.get("instructions")
        
        
        return redirect("customer_orders")
      
    return render(request, "dashboard/customerdashboard/new_order.html")

@login_required
def track_order(request, id):
    order = get_object_or_404(Order, id = id,
        user = request.user )
    
    return render(request, "dashboard/customerdashboard/track_order.html", {
        "order": order
    })
    
    
@login_required
def customer_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    
    print("USER:", request.user)
    print("ORDERS FOUND", orders)
    
    
    return render(request, "dashboard/customerdashboard/orders.html", {
        "orders": orders
    })

def home(request):
    return render(request, 'orders/home.html')

def orders(request):
    return render(request, 'dashboard/customerdashboard/orders.html')

def new_order(request):
    return render(request, 'dashboard/customerdashboard/new_order.html')

def notifications(request):
    return render(request, 'dashboard/customerdashboard/notifications.html')

def customer_profile(request):
    return render(request, 'dashboard/customerdashboard/profile.html')


def update_profile(request):
    return redirect('customer_profile')

def change_password(request):
    return redirect('customer_profile')

def delete_account(request):
    return redirect('home')

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


def delivery_history(request):
    context = {
        
    }
    return render(request, 'dashboard/driverdashboard/history.html', context)

def update_driver_profile(request):
    if request.method == "POST":
        #saving logic later
        return redirect("driver_profile")
    return redirect("driver_profile")


