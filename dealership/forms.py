from django import forms
from .models import Employee, Car, Sale


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["full_name", "position", "phone", "email"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["manufacturer", "year", "model", "cost_price", "potential_sale_price"]


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["employee", "car", "sale_date", "actual_sale_price"]
