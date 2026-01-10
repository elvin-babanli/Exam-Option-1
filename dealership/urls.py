from django.urls import path
from . import views

app_name = "dealership"

urlpatterns = [
    path("employees/", views.EmployeeListView.as_view(), name="employee_list"),
    path("employees/add/", views.EmployeeCreateView.as_view(), name="employee_add"),
    path("employees/<int:pk>/edit/", views.EmployeeUpdateView.as_view(), name="employee_edit"),
    path("employees/<int:pk>/delete/", views.EmployeeDeleteView.as_view(), name="employee_delete"),

    path("cars/", views.CarListView.as_view(), name="car_list"),
    path("cars/add/", views.CarCreateView.as_view(), name="car_add"),
    path("cars/<int:pk>/edit/", views.CarUpdateView.as_view(), name="car_edit"),
    path("cars/<int:pk>/delete/", views.CarDeleteView.as_view(), name="car_delete"),

    path("sales/", views.SaleListView.as_view(), name="sale_list"),
    path("sales/add/", views.SaleCreateView.as_view(), name="sale_add"),
    path("sales/<int:pk>/edit/", views.SaleUpdateView.as_view(), name="sale_edit"),
    path("sales/<int:pk>/delete/", views.SaleDeleteView.as_view(), name="sale_delete"),

    path("reports/", views.ReportsView.as_view(), name="reports"),
]
