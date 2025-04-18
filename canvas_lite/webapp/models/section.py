from collections.abc import Iterable

from django.conf import settings
from django.db import models

from webapp.models.courses import Course
from webapp.models.users import User

"""
Model is a section of the Course Model. It contains the instructor (User of either ta group or instructor group)
and schedule. it also controls the assignment of these variables
Each Section is unique to to a course and cannot be copied to another course.
"""
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

    schedule = models.JSONField(default=dict)

    def assign_instructor(self, user):
        """
        Set the instructor for this section.
        """
        if user is not None and not isinstance(user, User):
            return None
        self.instructor = user
        self.save(update_fields=['instructor'])

    def set_schedule(self, schedule_dict):
        """
        Set the schedule for this section.
        schedule_dict should be a dictionary.
        """
        if not isinstance(schedule_dict, dict):
            return None
        self.schedule = schedule_dict
        self.save(update_fields=['schedule'])
    # other section-specific fields
    def __str__(self):
        return f"{self.course.name} - {self.name}"

    class Meta:
        unique_together = ('course', 'name')