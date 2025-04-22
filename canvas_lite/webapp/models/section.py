from collections.abc import Iterable

from django.conf import settings
from django.db import models

from webapp.models.users import User




class SectionType(models.TextChoices):
    LECTURE = "LEC", "Lecture"
    LAB = "LAB", "Lab"
    DISCUSSION = "DIS", "Discussion"

"""
Model is a section of the Course Model. 
It contains the instructor (User of either ta group or instructor group) and schedule.
It also controls the assignment of these variables
Each Section is unique to to a course and cannot be copied to another course.
"""
class Section(models.Model):
    name = models.CharField(max_length=100)
    schedule = models.JSONField(default=dict)
    section_type = models.CharField(
        max_length=3,
        choices=SectionType,
        default=SectionType.LECTURE,
    )
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='sections')
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sections_taught'
    )
    # Only subsections will have this set
    main_section = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_sections'
    )

    class Meta:
        unique_together = (
            ('course', 'name'),
            ('main_section', 'name'),
        )

    def is_main_section(self):
        return self.section_type == SectionType.LECTURE and self.main_section is None

    def is_sub_section(self):
        return self.main_section is not None

    def get_subsections(self):
        """Return all subsections for this main section."""
        if self.is_main_section():
            return self.sub_sections.all()
        return Section.objects.none()

    @staticmethod
    def create_main_section(course, sec_name, instructor=None, schedule=None):
        return Section.objects.create(
            name=sec_name,
            course=course,
            instructor=instructor,
            schedule=schedule or {},
            main_section=None,
        )

    def create_subsection(self, name, sectype=SectionType.LAB, instructor=None, schedule=None):
        """Create a subsection under this main section."""
        if not self.is_main_section():
            return None
        if sectype == SectionType.LECTURE:
            return None  # Only LAB or DISCUSSION allowed as subsections
        return Section.objects.create(
            name=name,
            section_type=sectype,
            course=self.course,
            instructor=instructor,
            schedule=schedule or {},
            main_section=self,
        )

    def assign_instructor(self, user):
        """Assign an instructor to this section."""
        from . import User
        if user is not None and not isinstance(user, User):
            return False
        self.instructor = user
        self.save(update_fields=['instructor'])
        return True

    def set_schedule(self, schedule_dict):
        """Set the schedule for this section."""
        if not isinstance(schedule_dict, dict):
            return False
        self.schedule = schedule_dict
        self.save(update_fields=['schedule'])
        return True

    def __str__(self):
        if self.is_sub_section():
            return f"{self.course.name} - {self.main_section.name} - {self.name}"
        return f"{self.course.name} - {self.name}"
