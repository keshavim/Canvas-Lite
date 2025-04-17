from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):
    sections = models.ManyToManyField('Section', blank=True)
    notifications = models.ManyToManyField('Notification', blank=True)

    def get_sections_assigned(self):
        """
                Returns all sections assigned to this user.
                """
        return self.sections.all()

    def get_courses_assigned(self):
        """
        Returns a queryset of distinct courses that the user is assigned to via their sections.

        Returns:
            QuerySet: All unique Course objects related to the user's sections.
        """
        from .courses import Course
        return Course.objects.filter(sections__in=self.sections.all()).distinct()

    def is_in_course(self, course):
        """
        Returns True if the user is enrolled in any section of the given course.
        """
        return self.sections.filter(course=course).exists()

    def get_sections_for_course(self, course):
        """
        Returns a queryset of sections for the given course that the user is enrolled in.
        """
        return self.sections.filter(course=course)

    def send_notification(self, subject, message):
        """
                Sends an email notification to the user.

                Args:
                    subject (str): The subject of the email.
                    message (str): The body of the email.
                """
        send_mail(subject, message, 'from@example.com', [self.email])

    def add_notification(self, subject, message):
        from .notifications import Notification
        self.notifications.add(Notification(subject=subject, message=message, user=self))

    def see_all_notifications(self):
        return self.notifications.all()

    def __str__(self):
        return self.username

    class Meta:
        permissions = (
            ("can_assign_courses_l1", "Can assign courses level 1"),
            ("can_assign_courses_l2", "Can assign courses level 2"),
        )
