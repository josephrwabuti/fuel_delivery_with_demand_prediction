from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Profile
from django.contrib.auth.models import User


@staff_member_required
def assign_driver(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        driver = User.objects.get(id=request.POST.get("driver_id"))
        order.diver = driver
        order.status = "Driver Assigned"
        order.save()

    return redirect("admin_orders")


@login_required
def driver_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != "driver":
        return redirect("home")
    
    total_orders = Order.objects.filter(driver=request.user).count()
    active_orders = Order.objects.filter(driver=request.user, 
                status__in=["Driver Assigned", "En Route"]
                ).count()
    completed_orders = Order.objects.filter(
        driver=request.user,
        status="Delivered"
    ).count()
    
    context = {
        "orders": Order.objects.filter(driver=request.user).order_by("-created_at"),
        "total_orders": total_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders
    }

    

    return render(request, "dashboard/driverdashboard/dashboard.html", {
        "orders": orders
    })
    
    
@login_required
def my_deliveries(request):
    orders = Order.objects.filter(
        driver=request.user,
        status__in=["Driver Assigned", "En Route"]
    )

    return render(request, "dashboard/driverdashboard/my_deliveries.html", {
        "orders": orders
    })
    
@login_required
def update_delivery_status(request, id):
    order = Order.objects.get(id=id, driver=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()

    return redirect("my_deliveries")



@login_required
def place_order(request):
    if request.method == "POST":
        Order.objects.create(
            user=request.user,
            fuel_type=request.POST.get("fuel_type"),
            quantity=request.POST.get("quantity"),
            delivery_address=request.POST.get("delivery_address"),
            delivery_date=request.POST.get("delivery_date"),
            time_slot=request.POST.get("time_slot"),
            instructions=request.POST.get("instructions"),
            status="Pending"
        )

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
    
@login_required
def delivery_history(request):
    orders = Order.objects.filter(
        driver=request.user,
        status="Delivered"
    ).order_by("-created_at")
    
    return render(request, 'dashboard/driverdashboard/history.html', {
        "orders": orders
    })
    
    
@login_required
def available_orders(request):
    orders = Order.objects.filter(
        status="Confirmed",
        driver__isnull=True
    )
    
    return render(request, 'dashboard/driverdashboard/available_orders.html', {
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


def delivery_detail(request, id):
    return render(request, 'dashboard/driverdashboard/delivery_detail.html')


def update_driver_profile(request):
    if request.method == "POST":
        #saving logic later
        return redirect("driver_profile")
    return redirect("driver_profile")


