from django.core.management.base import BaseCommand
from django.contrib.auth import urls

class Command(BaseCommand):
    help = "Prints all authentication URLs provided by django.contrib.auth.urls"

    def handle(self, *args, **kwargs):
        self.stdout.write("Authentication URLs:")
        for pattern in urls.urlpatterns:
            try:
                self.stdout.write(f"Path: {pattern.pattern}, Name: {pattern.name}")
            except AttributeError:
                self.stdout.write("Unnamed URL pattern")