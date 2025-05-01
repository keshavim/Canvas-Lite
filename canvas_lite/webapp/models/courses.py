

from django.db import models
from django.utils.text import normalize_newlines

"""
Class that contains basic information about a course.
It has links to a Section object.
Can create and remove sections.
"""
class Course(models.Model):
    name = models.CharField(default=None, max_length=50)
    description = models.TextField(blank=True)

    def get_sections(self):
        """
        returns all sections with a link to this course
        """
        return self.sections
    def get_section_with_id(self, section_id):
        """
        returns section with given id.
        raise doesNotExit if not found
        """
        return self.sections.get(id=section_id)

    def get_section_with_name(self, section_name):
        return self.sections.get(name__exact=section_name)

    def add_section(self, name, instructor=None, schedule=None):
        """
        Create and add a new section to this course.
        """
        from . import Section  # Avoid circular import
        return Section.create_main_section(self, name, instructor, schedule)

    def remove_section(self, section_id):
        """
        Remove a section from this course by ID.
        If found, return true and delete, else return false.
        """
        section = self.sections.filter(id=section_id).first()
        if section:
            section.delete()
            return True
        return False

    def __str__(self):
        return self.name
