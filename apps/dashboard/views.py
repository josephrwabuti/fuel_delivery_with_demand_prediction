from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from apps.accounts.models import Profile
from django.utils import timezone

@login_required
def dashboard_home(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, "dashboard/customerdashboard/dashboard.html", {
        "orders": orders,
        "total_orders": orders.count(),
        "pending_orders": orders.filter(status="Pending").count(),
        "delivered_orders": orders.filter(status="Delivered").count(),
    })
    
    
@login_required
def dashboard(request):
    orders = Order.objects.all()

    total_orders = orders.count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    enroute_orders = orders.filter(status__in=["Fuel Loaded", "En Route", "Arrived"]).count()
    cancelled_orders = orders.filter(status="Cancelled").count()

    total_customers = User.objects.filter(profile__role="customer").count()
    total_drivers = User.objects.filter(profile__role="driver").count()
    recent_orders = orders.order_by("-created_at")[:5]

    top_drivers_qs = User.objects.filter(profile__role="driver").annotate(
        delivered_count=Count("order", filter=Q(order__status="Delivered"))
    ).order_by("-delivered_count")[:4]

    top_drivers = []
    for driver in top_drivers_qs:
        name = driver.get_full_name() or driver.username
        initials = "".join([part[0] for part in name.split()][:2]).upper()
        top_drivers.append({
            "name": name,
            "deliveries": driver.delivered_count,
            "on_time_rate": 100,
            "initials": initials,
        })

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "enroute_orders": enroute_orders,
        "cancelled_orders": cancelled_orders,
        "total_customers": total_customers,
        "total_drivers": total_drivers,
        "recent_orders": recent_orders,
        "top_drivers": top_drivers,
    }

    return render(request, "dashboard/admindashboard/dashboard.html", context)

@login_required
def admin_orders(request):
    orders = Order.objects.select_related("user", "driver").order_by("-created_at")

    context = {
        "orders": orders,
        "total_orders": orders.count(),
        "pending_orders": orders.filter(status="Pending").count(),
        "delivered_orders": orders.filter(status="Delivered").count(),
        "cancelled_orders": orders.filter(status="Cancelled").count(),
        "available_drivers": User.objects.filter(profile__role="driver"),
    }

    return render(request, 'dashboard/admindashboard/orders.html', context)

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
        "drivers": User.objects.filter(profile__role="driver")
    })

@login_required
def admin_reports(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    total_litres = orders.aggregate(total=Sum("quantity"))["total"] or 0
    total_revenue = orders.aggregate(total=Sum("amount"))["total"] or 0

    current_year = timezone.now().year
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_data = []
    for month_index, label in enumerate(month_labels, start=1):
        month_count = orders.filter(created_at__year=current_year, created_at__month=month_index).count()
        monthly_data.append({
            "label": label,
            "count": month_count,
            "pct": round((month_count / total_orders) * 100) if total_orders else 0
        })

    status_breakdown = []
    status_groups = [
        ("Delivered", delivered_orders, "var(--success)"),
        ("Pending", pending_orders, "var(--warning)"),
        ("En Route", orders.filter(status="En Route").count(), "var(--primary)"),
        ("Processing", orders.filter(status="Confirmed").count(), "var(--info)"),
        ("Cancelled", orders.filter(status="Cancelled").count(), "var(--danger)"),
    ]
    for label, count, color in status_groups:
        status_breakdown.append({
            "label": label,
            "count": count,
            "pct": round((count / total_orders) * 100) if total_orders else 0,
            "color": color,
        })

    top_customers_qs = User.objects.filter(order__isnull=False).annotate(
        orders=Count("order", distinct=True),
        litres=Sum("order__quantity"),
        spent=Sum("order__amount"),
    ).order_by("-orders")[:4]

    top_customers = []
    for customer in top_customers_qs:
        name = customer.get_full_name() or customer.username
        initials = "".join([part[0] for part in name.split()][:2]).upper()
        top_customers.append({
            "initials": initials,
            "name": name,
            "orders": customer.orders or 0,
            "litres": customer.litres or 0,
            "spent": customer.spent or 0,
        })

    driver_performance_qs = User.objects.filter(profile__role="driver").annotate(
        delivery_count=Count("deliveries"),
        litres=Sum("deliveries__quantity"),
    ).order_by("-delivery_count")[:4]

    driver_performance = []
    for driver in driver_performance_qs:
        name = driver.get_full_name() or driver.username
        initials = "".join([part[0] for part in name.split()][:2]).upper()
        driver_performance.append({
            "initials": initials,
            "name": name,
            "deliveries": driver.deliveries or 0,
            "on_time": 95,
            "litres": driver.litres or 0,
        })

    return render(request, 'dashboard/admindashboard/reports.html', {
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "pending_orders": pending_orders,
        "total_litres": total_litres,
        "total_revenue": total_revenue,
        "current_year": current_year,
        "monthly_data": monthly_data,
        "status_breakdown": status_breakdown,
        "top_customers": top_customers,
        "driver_performance": driver_performance,
    })


@login_required
def assign_driver(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        driver_id = request.POST.get("driver_id")
        
        try:
            # Get the order and driver from database
            order = Order.objects.get(id=order_id)
            driver = User.objects.get(id=driver_id)
            
            # Update the order with driver and new status
            order.driver = driver
            order.status = "Driver Assigned"  # Change from Pending to Fuel Loaded
            order.save()  # Save to database
            
        except (Order.DoesNotExist, User.DoesNotExist):
            # If order or driver doesn't exist, just pass (do nothing)
            pass
        
    return redirect('admin_orders')

@login_required
def delete_driver(request, id):
    if request.method == "POST":
        try:
            driver = User.objects.get(id=id)
            driver.delete()
        except User.DoesNotExist:
            pass
    return redirect('admin_drivers')


@login_required
def delete_order(request, id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=id)
            order.delete()
        except Order.DoesNotExist:
            pass
    return redirect('admin_orders')

@login_required
def delete_customer(request, id):
    if request.method == "POST":
        try:
            customer = User.objects.get(id=id)
            customer.delete()
        except User.DoesNotExist:
            pass
    return redirect('admin_customers')


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






