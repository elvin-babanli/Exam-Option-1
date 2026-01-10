import csv
import io
from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper, Value
from django.db.models.functions import Coalesce

from .models import Employee, Car, Sale


class SaleQueryService:
    """
    Single responsibility: build filtered queryset for sales.
    """
    @staticmethod
    def filter_sales(
        start: Optional[date] = None,
        end: Optional[date] = None,
        exact: Optional[date] = None,
        employee_id: Optional[int] = None,
    ):
        qs = Sale.objects.select_related("employee", "car").all()

        if exact:
            qs = qs.filter(sale_date=exact)
        if start:
            qs = qs.filter(sale_date__gte=start)
        if end:
            qs = qs.filter(sale_date__lte=end)
        if employee_id:
            qs = qs.filter(employee_id=employee_id)

        return qs


class ReportService:
    """
    Single responsibility: compute report metrics.
    """
    @staticmethod
    def total_profit(qs):
        profit_expr = ExpressionWrapper(
            F("actual_sale_price") - F("car__cost_price"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )

        total_expr = Coalesce(
            Sum(profit_expr),
            Value(Decimal("0.00")),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )

        data = qs.aggregate(total=total_expr)
        return data["total"]

    @staticmethod
    def best_selling_car_name(qs) -> Optional[str]:
        row = (
            qs.values("car__manufacturer", "car__model")
            .annotate(cnt=Count("id"))
            .order_by("-cnt")
            .first()
        )
        if not row:
            return None
        return f'{row["car__manufacturer"]} {row["car__model"]}'

    @staticmethod
    def top_salesperson(qs) -> Optional[Tuple[str, int]]:
        row = (
            qs.values("employee__full_name")
            .annotate(cnt=Count("id"))
            .order_by("-cnt")
            .first()
        )
        if not row:
            return None
        return (row["employee__full_name"], row["cnt"])


class ExportService:
    """
    Single responsibility: export querysets to CSV.
    """
    @staticmethod
    def export_sales_csv(qs) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "sale_date", "employee", "car", "actual_sale_price", "cost_price", "profit"])

        for s in qs:
            writer.writerow([
                s.id,
                s.sale_date.isoformat(),
                s.employee.full_name,
                f"{s.car.manufacturer} {s.car.model} ({s.car.year})",
                str(s.actual_sale_price),
                str(s.car.cost_price),
                str(s.profit),
            ])

        return buf.getvalue()

    @staticmethod
    def export_employees_csv(qs) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "full_name", "position", "phone", "email"])
        for e in qs:
            writer.writerow([e.id, e.full_name, e.position, e.phone, e.email])
        return buf.getvalue()

    @staticmethod
    def export_cars_csv(qs) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "manufacturer", "year", "model", "cost_price", "potential_sale_price"])
        for c in qs:
            writer.writerow([c.id, c.manufacturer, c.year, c.model, str(c.cost_price), str(c.potential_sale_price)])
        return buf.getvalue()
