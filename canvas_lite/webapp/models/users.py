from django.contrib.auth.models import AbstractUser, Group
from django.db import models

"""enum type of user groups"""
class UserType(models.TextChoices):
    TA = "T", "TA"
    INSTRUCTOR = "I", "Instructor"
    ADMIN = "A", "ADMIN"


"""
class that can be of the group TA, Instructor, or Admin
TA and instructor are assigned to courses
All can get and receive notifications/emails

--planned--
Instructor can assign TA to sections
Admin can add and remove courses
Admin can assign instructor to sections
"""
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='phone_number', null=True)
    description = models.TextField(blank=True, null=True, verbose_name='description')

    group_name = models.CharField(
        max_length=1,
        choices=UserType,
        default=UserType.TA,
    )

    def assign_user_to_section(self, other, section_id):
        if self.get_user_group() == UserType.TA:
            return PermissionError("TA can not assign Users to section")
        elif self.get_user_group() == UserType.INSTRUCTOR:
            if other.get_user_group() != UserType.TA:
                return PermissionError("Instructor can not assign this user to section")
            elif not self.is_in_section(section_id):
                return PermissionError("Instructor can not assign this user to section")
        section = self.get_assigned_section_id(section_id)
        section.assign_instructor(other)

    def get_user_group(self):
        
        return self.groups.filter(name__exact=self.group_name)

    def set_user_group(self, group_name = UserType.TA):
        if group_name not in UserType:
          raise ValueError("Group must be of enum UserType")

        # Remove user from all allowed groups
        self.groups.clear()

        # Add user to the selected group
        group = Group.objects.get(name=group_name)
        self.groups.add(group)
        
    def get_sections(self):
        """
        gets the sections this user teaches
        """
        return self.sections_taught.all()

    def get_main_sections(self):
        return self.get_sections().filter(is_main_section=True)

    def get_assigned_section_id(self, section_id):
        """
        gets the sections this user teaches from the id given. return none if not found
        """
        if not self.is_in_section(section_id):
            return None
        return self.sections_taught.filter(id=section_id).first()

    def get_assigned_courses(self):
        """
        gets the courses assigned to this user from the sections assigned
        """
        from . import Course
        return (Course.objects
                .filter(sections__in=self.get_sections())
                .distinct())

    def is_in_course(self, course_id):
        """
        Checks if user is instructor of any section in the course
        """
        return self.sections_taught.filter(course_id=course_id).exists()

    def is_in_section(self, section_id):
        """
         Checks if user is instructor of the given section
        """
        return self.sections_taught.filter(id=section_id).exists()

    def get_schedules(self):
        """
        Gets all schedules from sections taught by this user.
        Returns a list of schedule dicts or an empty list if none exist.
        """
        return [section.schedule for section in self.get_sections()]
    def get_notifications(self):
        """
            Returns all notifications (UserNotification objects) for this user.
        """
        return self.usernotification_set.select_related('notification')

    def get_sent_notifications(self):
        """
            Returns all notifications this user has sent.
        """
        return self.sent_notification.all()

    def get_read_notifications(self):
        """
            Returns all notifications (UserNotification objects) for this user that are marked as read.
        """
        return self.usernotification_set.filter(read=True).select_related('notification')

    def get_unread_notifications(self):
        """
            Returns all notifications (UserNotification objects) for this user that are unread.
        """
        return self.usernotification_set.filter(read=False).select_related('notification')

    def send_notifications(self, recipients, subject=None, message=None):
        from . import Notification
        Notification.create_and_send(recipients, subject, message, self)

    def __str__(self):
        return self.username

    class Meta:
        permissions = (
            ("can_assign_l1", "Can assign to courses/sections: instructor"),
            ("can_assign_l2", "Can assign to courses/sections: admin"),
        )



