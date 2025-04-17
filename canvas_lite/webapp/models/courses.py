from typing import Any

from django.db import models


class Course(models.Model):
    name = models.CharField(default=None, max_length=50)
    description = models.TextField(blank=True)

    def get_sections(self):
        # Returns all sections for this course
        return self.sections.all()

    def __str__(self):
        return self.name

