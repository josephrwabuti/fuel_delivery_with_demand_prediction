from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "fuel_type",
            "quantity",
            "delivery_address",
            "delivery_date",
            "time_slot",
            "instructions"
        ]