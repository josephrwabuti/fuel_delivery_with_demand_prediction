from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages


@staff_member_required
def admin_orders(request):
    
    orders = Order.objects.select_related(
        "user",
        "driver"
    ).order_by("-created_at")
    
    available_drivers = User.objects.filter(
        profile__role="driver"
    )
    
    context = {
        "orders": orders,
        "available_drivers": available_drivers,
        
        "total_orders": orders.count(),
        
        "pending_orders": orders.filter(status="Pending").count(),
        
        "delivered_orders": orders.filter(status="Delivered").count(),
        
        "cancelled_orders": orders.filter(status="Cancelled").count(),
    }
    
    return render(
        request, "dashboard/admindashboard/orders.html", context
    )


@staff_member_required
def assign_driver(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    drivers = User.objects.filter(profile__role="driver")

    if request.method == "POST":
        
        driver_id = request.POST.get("driver_id")
        
        driver = get_object_or_404(User, id=driver_id)
        
        order.driver = driver
        order.status = "Driver Assigned"
        order.assigned_at = timezone.now()
        order.save()

        return redirect("admin_orders")
    
    return redirect("admin_orders")
    
    


@login_required
def driver_dashboard(request):
    
    user = request.user
    
    active_delivery = Order.objects.filter(
        driver=user,
        status__in=["Fuel Loaded", "En Route", "Arrived"]
    ).first()
    
    todays_assignments = Order.objects.filter(
        driver=user)
    
    available_count = Order.objects.filter(
        status="Pending",
        driver__isnull=True
    ).count()
    
    
    context = {
        "active_delivery": active_delivery,
        "todays_assignments": todays_assignments,
        "todays_deliveries": todays_assignments.count(),
        "todays_pending": todays_assignments.exclude(status="Delivered").count(),
        "totaL_completed": Order.objects.filter(driver=request.user, status="Delivered").count(),
        "total_litres": 0, #fix later
        "on_time_rate": 96,
        "available_count": Order.objects.filter(driver__isnull=True, status="Pending").count(),
        "week_total": todays_assignments.count(),
    }

    return render(request, "dashboard/driverdashboard/dashboard.html", context)
    
    
@login_required
def my_deliveries(request):
    
    orders = Order.objects.filter(driver=request.user)
    
    active_delivery = orders.filter(
        status__in=[
            "Driver Assigned",
            "Fuel Loaded", 
            "En Route", 
            "Arrived"
        ]
    ).first()
    
    

    return render(request, "dashboard/driverdashboard/my_deliveries.html", {
        "active_delivery": active_delivery,
        "my_deliveries": orders,
    })
    
    
@login_required
def delivery_history(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if profile.role != "driver":
        return redirect("home")
    
    
    history = Order.objects.filter(
        driver=request.user,
        status="Delivered"
    ).order_by("-created_at")
    
    return render(request, 'dashboard/driverdashboard/history.html', {
        "orders": history
    })
    
    
@login_required
def update_delivery_status(request, id):
    order = get_object_or_404(
        Order,
        id=id, 
        driver=request.user
    )

    if request.method == "POST":
        
        new_status = request.POST.get("status")
        
        if new_status in [
            "En Route",
            "Delivered"
        ]:
            order.status = new_status
            order.save()

        return redirect("my_deliveries")
    


@login_required
def delivery_detail(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        driver=request.user
    )
    return render(request, 'dashboard/driverdashboard/delivery_detail.html', {
        "order": order
    })
    

@login_required
def claim_order(request, order_id):
    
    if request.method == "POST":
        
        order = get_object_or_404(Order, id=order_id)
        
        if order.driver:
            messages.error(request, "This order has already been claimed!")
            
            return redirect("available_orders")
        
        active_order = Order.objects.filter(
            driver=request.user,
            status__in=[
                "Driver Assigned",
                "Fuel Loaded",
                "En Route",
                "Arrived"
            ]
        ).exists()
        
        if active_order:
            messages.error(
                request, "Complete your current delivery before claiming another order."
            )
            return redirect("available_orders")
        
        order.driver = request.user
        order.status = "Driver Assigned"
        order.save()
        
        messages.succes(request, "Order claimed successfully!")
    
    return redirect("my_deliveries")


@login_required
def available_orders(request):
    
    orders = Order.objects.filter(
        driver__isnull=True,
        status="Confirmed"
    )
    
    return render(
        request, "dashboard/driverdashboard/available_orders.html", {
            "available_orders": available_orders
        }
    )



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


