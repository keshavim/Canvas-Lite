from django.conf import settings
from django.db import models


class Section(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='sections')
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
    schedule = models.JSONField(default=dict)

    def assign_instructor(self, user):
        pass

    def assign_assistants(self, assistants):
        pass

    def set_schedule(self, schedule_dict):
        pass
