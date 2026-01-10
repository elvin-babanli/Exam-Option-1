import json
from django.core.management.base import BaseCommand
from django.core import serializers

from dealership.models import Employee, Car, Sale


class Command(BaseCommand):
    help = "Export employees, cars, sales to a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, default="export.json")

    def handle(self, *args, **options):
        path = options["path"]

        data = []
        data.extend(json.loads(serializers.serialize("json", Employee.objects.all())))
        data.extend(json.loads(serializers.serialize("json", Car.objects.all())))
        data.extend(json.loads(serializers.serialize("json", Sale.objects.all())))

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Exported to {path}"))
