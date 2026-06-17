from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order

@login_required
def dashboard_home(request):
    orders = Order.objects.filter(user=request.user)
    
    total_orders = orders.count()
    pending_orders =  orders.filter(status="Pending").count()
    delivered_orders = orders.filter(status="Delivered").count()
    
    return render(request, 'dashboard/customerdashboard/dashboard.html', {
        "orders": orders,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders
    })

def dashboard(request):
    return render(request, "dashboard/admindashboard/dashboard.html")

@login_required
def admin_orders(request):
    return render(request, 'dashboard/admindashboard/orders.html')

@login_required
def admin_customers(request):
    customers = User.objects.filter(order__isnull=False).distinct()
    
    data = []
    for c in customers:
        data.append({
            "user": c,
            "orders_count": c.order_set.count(),
            "last_order": c.order_set.last()
        })
    return render(request, 'dashboard/admindashboard/customers.html', {
        "customers": data
    })

@login_required
def admin_drivers(request):
    demo_drivers = range(6)
    
    return render(request, 'dashboard/admindashboard/drivers.html', {
        "demo_drivers": demo_drivers,
    })

@login_required
def admin_reports(request):
    return render(request, 'dashboard/admindashboard/reports.html')


def assign_driver(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        driver_id = request.POST.get("driver_id")
        
        print(order_id, driver_id)
        
    return redirect('orders')


def add_driver(request):
    if request.method == "POST":
        # code to save drivers 
        pass
    
    return redirect("admin_drivers")

def admin_update_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        
        return redirect('admin_settings')
    
    return redirect('admin_settings')

def admin_save_settings(request):
    if request.method == "POST":
        
        return redirect("admin_settings")
    
def admin_settings(request):
    SYSTEM_TOGGLES = [
        ("Online Ordering", "Allow customers to place new orders", 1),
        ("AI Auto-Scheduling", "Let AI auto-assign drivers", 1),
        ("Driver Self-Assignment", "Allow drivers to accept order themselves", 1),
        ("Customers Registration", "Allow new signups", 1),
        ("Maintenance Mode", "Disable system", 0),
    ]
    
    
    
    NOTIFICATIONS = [
        ("New order placed", "Get notified when a customer places an order", 1),
        ("Order delivered", "Confirm when delivery is completed", 1),
        ("Driver goes offline", "Allert when driver is offline", 0),
        ("New customer signup", "Notify when new customer registers", 1),
        ("Order Cancelled", "Allert when order is cancelled", 1),
        ("Low driver availabilty", "Warn when drivers are few", 1),
    ]
    
    
    
    SECURITY = [
        ("Two-factor Auntentication", "Require 2FA for admin logins", 0),
        ("Session Timeout", "Auto logout after inactivity", 1),
        ("Driver goes offline", "Allert when driver is offline", 0),
        ("Login Alerts", "Email alert on new login", 1),
        ("Force Password Reset", "Require password reset", 0),
    ]
    
    
    
    PRICING = [
        ("Petrol", "fire-flame-curved", 1.42),
        ("Diesel", "oil-can", 1.38),
        ("Kerosene", "flask", 1.15),
        ("Bio-fuel", "leaf", 1.55),
    ]
    
    return render(request, "dashboard/admindashboard/settings.html", {
        "system_toggles": SYSTEM_TOGGLES,
        "notifications": NOTIFICATIONS,
        "security_settings": SECURITY,
        "pricing": PRICING,
    })
    
    

def admin_save_pricing(request):
    if request.method == "POST":
        petrol = request.POST.get("price_petrol")
        diesel = request.POST.get("price_diesel")
        kerosene = request.POST.get("price_kerosene")
        bio_fuel = request.POST.get("price_bio-fuel")
        
        return redirect("admin_settings")
    
    return redirect("admin_settings")






