"""
WSGI config for car_dealership project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_dealership.settings")
application = get_wsgi_application()
