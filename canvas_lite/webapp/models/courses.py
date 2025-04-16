from typing import Any

from django.db import models


class Course(models.Model):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.id = models.IntegerField(primary_key=True)
        self.name = models.CharField(max_length=30)