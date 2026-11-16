"""WSGI entry point: this is what a production server (gunicorn) imports."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calcsite.settings")

application = get_wsgi_application()
