from typing import Any

from django.db import models
from webapp.models.users import User

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.message}"
