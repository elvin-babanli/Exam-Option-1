from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

from .models import Employee, Car, Sale
from .services import ReportService, SaleQueryService


class DealershipTests(TestCase):
    def setUp(self):
        self.emp = Employee.objects.create(
            full_name="John Doe",
            position="Manager",
            phone="+48123456789",
            email="john@example.com",
        )
        self.car = Car.objects.create(
            manufacturer="Toyota",
            year=2020,
            model="Corolla",
            cost_price=Decimal("10000.00"),
            potential_sale_price=Decimal("13000.00"),
        )
        self.sale = Sale.objects.create(
            employee=self.emp,
            car=self.car,
            sale_date=timezone.localdate(),
            actual_sale_price=Decimal("12500.00"),
        )

    def test_profit_property(self):
        self.assertEqual(self.sale.profit, Decimal("2500.00"))

    def test_report_total_profit(self):
        qs = SaleQueryService.filter_sales()
        total = ReportService.total_profit(qs)
        self.assertEqual(total, Decimal("2500.00"))

    def test_employee_list_view(self):
        url = reverse("dealership:employee_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "John Doe")
