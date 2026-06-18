from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    FUEL_TYPES = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Kerosene", "Kerosene"),
        ("Bio-fuel", "Bio-fuel"),
    ]
    
    STATUS = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Drive Assigned", "Driver Assigned"),
        ("En Route", "En Route"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    quantity = models.IntegerField()
    delivery_address = models.TextField()
    delivery_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.user.username} - {self.fuel_type}"
    
    
driver = models.ForeignKey(
    "auth.User",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="deliveries"
)
    
