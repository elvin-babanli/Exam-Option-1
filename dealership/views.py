from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Employee, Car, Sale
from .forms import EmployeeForm, CarForm, SaleForm
from .services import SaleQueryService, ReportService, ExportService


class EmployeeListView(ListView):
    model = Employee
    template_name = "dealership/employee_list.html"


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "dealership/employee_form.html"
    success_url = reverse_lazy("dealership:employee_list")


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "dealership/employee_form.html"
    success_url = reverse_lazy("dealership:employee_list")


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = "dealership/employee_confirm_delete.html"
    success_url = reverse_lazy("dealership:employee_list")


class CarListView(ListView):
    model = Car
    template_name = "dealership/car_list.html"


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = "dealership/car_form.html"
    success_url = reverse_lazy("dealership:car_list")


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = "dealership/car_form.html"
    success_url = reverse_lazy("dealership:car_list")


class CarDeleteView(DeleteView):
    model = Car
    template_name = "dealership/car_confirm_delete.html"
    success_url = reverse_lazy("dealership:car_list")


class SaleListView(ListView):
    model = Sale
    template_name = "dealership/sale_list.html"


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "dealership/sale_form.html"
    success_url = reverse_lazy("dealership:sale_list")


class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = "dealership/sale_form.html"
    success_url = reverse_lazy("dealership:sale_list")


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = "dealership/sale_confirm_delete.html"
    success_url = reverse_lazy("dealership:sale_list")


def _parse_date(value: str):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()  

class ReportsView(View):
    template_name = "dealership/reports.html"

    def get(self, request):
        exact = _parse_date(request.GET.get("date", ""))
        start = _parse_date(request.GET.get("start", ""))
        end = _parse_date(request.GET.get("end", ""))
        employee_id = request.GET.get("employee_id") or None
        export = request.GET.get("export")

        sales_qs = SaleQueryService.filter_sales(
            exact=exact,
            start=start,
            end=end,
            employee_id=int(employee_id) if employee_id else None,
        )

        if export == "csv":
            csv_text = ExportService.export_sales_csv(sales_qs)
            resp = HttpResponse(csv_text, content_type="text/csv")
            resp["Content-Disposition"] = 'attachment; filename="sales_report.csv"'
            return resp

        context = {
            "employees": Employee.objects.all(),
            "sales": sales_qs,
            "total_profit": ReportService.total_profit(sales_qs),
            "best_car": ReportService.best_selling_car_name(sales_qs),
            "top_emp": ReportService.top_salesperson(sales_qs),
        }
        return render(request, self.template_name, context)
