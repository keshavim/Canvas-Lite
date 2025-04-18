from collections.abc import Iterable

from django.conf import settings
from django.db import models

from webapp.models.users import User

"""
Model is a section of the Course Model. 
It contains the instructor (User of either ta group or instructor group) and schedule.
It also controls the assignment of these variables
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
        Instructor can be None.
        if user is invalid return false.
        """
        if user is not None and not isinstance(user, User):
            return False
        self.instructor = user
        self.save(update_fields=['instructor'])
        return True

    def set_schedule(self, schedule_dict):
        """
        Set the schedule for this section.
        schedule_dict should be a dictionary.
        if schedule_dict not a dict return False
        """
        if not isinstance(schedule_dict, dict):
            return False
        self.schedule = schedule_dict
        self.save(update_fields=['schedule'])
        return True
    # other section-specific fields
    def __str__(self):
        return f"{self.course.name} - {self.name}"

    class Meta:
        unique_together = ('course', 'name')