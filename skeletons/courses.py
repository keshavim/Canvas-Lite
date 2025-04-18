from django.db import models


class Course(models.Model):
    name = models.CharField(default=None, max_length=50)
    description = models.TextField(blank=True)

    def get_sections(self):
        pass

    def get_section_with_id(self, section_id):
        pass

    def get_section_with_name(self, section_name):
        pass


    def add_section(self, name, instructor=None, assistants=None, schedule=None):
        pass

    def remove_section(self, section_id):
        pass

