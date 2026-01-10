from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{7,15}$",
    message="Phone must be like +48123456789 or 123456789",
)


class Employee(TimeStampedModel):
    full_name = models.CharField(max_length=120)
    position = models.CharField(max_length=80)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.position})"


class Car(TimeStampedModel):
    manufacturer = models.CharField(max_length=80)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1886)])
    model = models.CharField(max_length=80)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    potential_sale_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ("manufacturer", "year", "model")

    def __str__(self) -> str:
        return f"{self.manufacturer} {self.model} ({self.year})"


class Sale(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="sales")
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="sales")
    sale_date = models.DateField(default=timezone.localdate)
    actual_sale_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["-sale_date", "-id"]

    def __str__(self) -> str:
        return f"Sale #{self.id} - {self.car} by {self.employee}"

    @property
    def profit(self):
        return self.actual_sale_price - self.car.cost_price
