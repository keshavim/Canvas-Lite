from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


"""
This class creates notifications and sends them to users
Uses UserNotification class to mark as read

Variables:
sender: link to the user that sent/will send the notification
recipients: list of links to the users that received/will receive the notification
the link is made through the UserNotification class

subject: small field for quick information
message: Big text field that contains full message
"""
class Notification(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notification'
    )
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserNotification',
        through_fields=('notification', 'user'),  # Explicitly define fields
        related_name='received_notifications'
    )
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_and_send(cls, recipients, subject=None, message=None, sender=None):
        notif = cls.objects.create(subject=subject, message=message, sender=sender)

        # Handle both QuerySet and individual instances
        if recipients is None:
            return notif

        # Convert single user to list
        if not isinstance(recipients, (list, tuple, set, QuerySet)):
            recipients = [recipients]

        # Handle QuerySet specifically
        if isinstance(recipients, QuerySet):
            recipients = list(recipients)

        # Remove duplicates and None values
        recipients = [user for user in set(recipients) if user is not None]

        user_notifications = [
            UserNotification(user=user, notification=notif)
            for user in recipients
        ]
        UserNotification.objects.bulk_create(user_notifications)

        return notif

    def get_user_notification(self, user):
        """
        Returns the UserNotification instance for this notification and user.
        """
        return UserNotification.objects.get(user=user, notification=self)

    def mark_as_read(self, user):
        """
        Marks this notification as read for the specified user.
        """
        self.get_user_notification(user).mark_as_read()

    def mark_as_unread(self, user):
        """
        Marks this notification as unread for the specified user.
        """
        self.get_user_notification(user).mark_as_unread()

    def is_read_by(self, user):
        """
        Checks if this notification has been read by the specified user.
        """
        return self.get_user_notification(user).is_read()

    def __str__(self):
        return f"{self.subject or self.message[:30]}"

"""
this class is used to make unique links between users and notifications.
It handles marking notifications as read

user: link to the user receiving the notification
notification: link to the notification
"""
class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'notification')

    def mark_as_read(self):
        """
        Marks this user-notification link as read and sets the read timestamp.
        """
        self.read = True
        self.read_at = timezone.now()
        self.save()

    def mark_as_unread(self):
        """
        Marks this user-notification link as unread and clears the read timestamp.
        """
        self.read = False
        self.read_at = None
        self.save()

    def is_read(self):
        """
        Returns True if this notification is marked as read for the user.
        """
        return self.read