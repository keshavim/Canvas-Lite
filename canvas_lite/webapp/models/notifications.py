from typing import Any

from django.conf import settings
from django.db import models
from django.utils import timezone


"""
This class creates notifications and sends them to users
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
        """
        Creates a notification and associates it with one or more users.
        Args:
            recipients: A user instance or an iterable of users.
            subject: The notification subject.
            message: The notification message.
            sender: The user sending the notification (optional).
        Returns:
            Notification: The created notification instance.
        """
        notif = cls.objects.create(subject=subject, message=message, sender=sender)


        if recipients is None:
            return notif
        if subject is None and message is None:
            return notif
        # Normalize recipients to a list
        if not isinstance(recipients, (list, tuple, set)):
            recipients = [recipients]

        # Remove duplicates and None values
        recipients = [user for user in set(recipients) if user is not None]

        # Bulk create UserNotification links
        user_notifications = [
            UserNotification(user=user, notification=notif)
            for user in recipients
        ]
        UserNotification.objects.bulk_create(user_notifications)

        return notif

    def mark_as_read(self, user):
        """
           Marks this notification as read for the specified user.
           Args:
               user (User): The user for whom the notification should be marked as read.
           Side Effects:
               Updates the corresponding UserNotification entry to set 'read' to True
               and records the current timestamp in 'read_at'.
           """
        link = UserNotification.objects.get(user=user, notification=self)
        link.read = True
        link.read_at = timezone.now()
        link.save()

    def mark_as_unread(self, user):
        """
           Marks this notification as unread for the specified user.
           Args:
               user (User): The user for whom the notification should be marked as unread.
           Side Effects:
               Updates the corresponding UserNotification entry to set 'read' to False
               and clears the 'read_at' timestamp.
           """
        link = UserNotification.objects.get(user=user, notification=self)
        link.read = False
        link.read_at = None
        link.save()

    def is_read_by(self, user):
        """
            Checks if this notification has been read by the specified user.
            Args:
                user (User): The user to check read status for.
            Returns:
                bool: True if the notification is marked as read for the user, False otherwise.
            """
        return UserNotification.objects.filter(user=user, notification=self, read=True).exists()

    def __str__(self):
        return f"To {self.subject or self.message[:30]}"

"""
this class is used to make unique links between users and notifications.
"""
class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'notification')