

from django.db import models

class Course(models.Model):
    name = models.CharField(default=None, max_length=50)
    description = models.TextField(blank=True)

    def get_sections(self):
        # Returns all sections for this course
        return self.sections.all()
    def get_section_with_id(self, section_id):
        return self.sections.get(id=section_id)

    def get_section_with_name(self, section_name):
        return self.sections.get(name__exact=section_name)

    def add_section(self, name, instructor=None, assistants=None, schedule=None):
        """
        Create and add a new section to this course.
        """
        from . import Section  # Avoid circular import
        section = Section.objects.create(
            course=self,
            name=name,
            instructor=instructor,
            schedule=schedule or {}
        )
        if assistants:
            section.assistants.set(assistants)
        return section

    def remove_section(self, section_id):
        """
        Remove a section from this course by ID.
        """
        section = self.sections.filter(id=section_id).first()
        if section:
            section.delete()
            return True
        return False

    def __str__(self):
        return self.name
