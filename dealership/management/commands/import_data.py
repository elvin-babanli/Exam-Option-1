import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction


class Command(BaseCommand):
    help = "Import employees, cars, sales from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, default="export.json")

    @transaction.atomic
    def handle(self, *args, **options):
        path = options["path"]

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        objects = list(serializers.deserialize("json", json.dumps(data)))
        for obj in objects:
            obj.save()

        self.stdout.write(self.style.SUCCESS(f"Imported from {path}"))
