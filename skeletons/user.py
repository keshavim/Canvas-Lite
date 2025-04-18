from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def get_assigned_sections(self):
       pass

    def get_assigned_courses(self):
        pass

    def is_in_course(self, course_id):
        pass

    def is_in_section(self, section_id):
        pass

    def get_notifications(self):
        pass

    def get_sent_notifications(self):
        pass

    def get_read_notifications(self):
        pass

    def get_unread_notifications(self):
        pass

    def send_notifications(self, recipients, subject=None, message=None):
        pass

