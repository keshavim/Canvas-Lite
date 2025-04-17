from django.conf import settings
from django.db import models

from webapp.models.courses import Course
from webapp.models.users import User


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sections_taught'
    )
    assistants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='sections_ta_for'
    )
    schedule = models.CharField(max_length=200, blank=True)
    # other section-specific fields

    def __str__(self):
        return f"{self.course.name} - {self.name}"