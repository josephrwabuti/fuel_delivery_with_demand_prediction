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
from django.db import transaction
from django.db.models import Sum, Count


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
    
    driver = request.user
    
    
    orders = Order.objects.filter(driver=driver)
    
    today = timezone.now().date()
    
    todays_orders = orders.filter(delivery_date=today)
    
    completed = orders.filter(status="Delivered")
    
    total_litres = completed.aggregate(
        total=Sum("quantity")
    )["total"] or 0
    
    total_delivered = completed.count()
    total_orders = orders.count()
    
    on_time_rate = 0
    if total_orders > 0:
        on_time_rate = round((total_delivered / total_orders) * 100)
    
    
    context = {
        "todays_deliveries": todays_orders.count(),
        "todays_pending": todays_orders.exclude(status="Delivered").count(),
        "total_completed": total_delivered,
        "total_litres": total_litres,
        "on_time_rate": on_time_rate,
        "todays_assignments": todays_orders,
        "active_delivery": orders.filter(status__in=["Fuel Loaded", "En Route", "Arrived"]).first(),
        "available_count": Order.objects.filter(driver__isnull=True).count(),
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
    
    history = Order.objects.filter(
        driver=request.user,
        status="Delivered"
    ).order_by("-delivered_at")
    
    context = {
        "history": history,
        "total_delivered": history.count(),
    }
    
    
    return render(request, 'dashboard/driverdashboard/history.html', context )
    
    
@login_required
def update_delivery_status(request, id):
    
    order = get_object_or_404(
        Order,
        id=id, 
        driver=request.user
    )

    if request.method == "POST":
        
        allowed_flow = [
            "Driver Assigned",
            "Fuel Loaded",
            "En Route",
            "Arrived",
            "Delivered"
        ]
        
        new_status = request.POST.get("status")
        note = request.POST.get("note")
        
        if new_status in allowed_flow:
            
            order.status = new_status
            
            if note:
                order.driver_note = note
            
            if new_status == "Fuel Loaded" and not order.loaded_at:
                order.loaded_at = timezone.now()
                
            elif new_status == "En Route" and not order.en_route_at:
                order.en_route_at = timezone.now()
                
            elif new_status == "Arrived" and not order.arrived_at:
                order.arrived_at = timezone.now()
            
            elif new_status == "Delivered" and not order.delivered_at:
                order.delivered_at = timezone.now()
            
            order.save()

        return redirect("my_deliveries")
    
    return redirect("my_deliveries")
    


@login_required
def delivery_detail(request, id):
    delivery = get_object_or_404(
        Order,
        id=id,
        driver=request.user
    )
    
    status_order = {
        "Driver Assigned": 1,
        "Fuel Loaded": 2,
        "En Route": 3,
        "Arrived": 4,
        "Delivered": 5,
    }
    
    context = {
        "delivery": delivery,
        "status_order": status_order.get(delivery.status, 1),
    }
    
    return render(request, 'dashboard/driverdashboard/delivery_detail.html', context )
    

@login_required
def claim_order(request, order_id):
    
    if request.method != "POST":
        return redirect("available_orders")
        
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)
    
        if order.driver:
            messages.error(request, "This order has already been claimed!")
            
            return redirect("available_orders")
        
        active_order = Order.objects.filter(
            driver=request.user,
            status__in=["Driver Assigned", "Fuel Loaded", "En Route", "Arrived"]
        ).exists()
        
        
        if active_order:
            messages.error(
                request, "Complete your current delivery before claiming another order."
            )
            return redirect("available_orders")
        
        order.driver = request.user
        order.status = "Driver Assigned"
        order.assigned_at = timezone.now()
        order.save()
        
        
        
        messages.success(request, f"Order #{order_id} claimed successfully!")
        
        print("CLAIM ORDER:", order_id, order.driver)
        
        return redirect("my_deliveries")


@login_required
def available_orders(request):
    
    orders = Order.objects.filter(
        driver__isnull=True,
        status__in=["Pending", "Confirmed"]
    )
    
    return render(
        request, "dashboard/driverdashboard/available_orders.html", {
            "available_orders": orders
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


def update_driver_profile(request):
    if request.method == "POST":
        #saving logic later
        return redirect("driver_profile")
    return redirect("driver_profile")


