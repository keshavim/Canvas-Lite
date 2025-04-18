from typing import Any

from django.conf import settings
from django.db import models

"""
This class creates notifications and sends them to users
Uses UserNotification class to mark as read
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
        pass

    def get_user_notification(self, user):
        pass

    def mark_as_read(self, user):
        pass

    def mark_as_unread(self, user):
        pass

    def is_read_by(self, user):
        pass

"""
this class is used to make unique links between users and notifications.
It handles marking notifications as read
"""
class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'notification')

    def mark_as_read(self):
        pass

    def mark_as_unread(self):
        pass

    def is_read(self):
        pass