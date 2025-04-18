from django.test import TestCase
from webapp.models import Notification, UserNotification
from webapp.models import User


class NotificationModelTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='pass')

    def test_create_and_send_single_user(self):
        notif = Notification.create_and_send(self.user1, "Subject 1", "Message 1")
        self.assertEqual(notif.subject, "Subject 1")
        self.assertEqual(notif.message, "Message 1")
        self.assertIn(self.user1, notif.recipients.all())
        self.assertEqual(UserNotification.objects.filter(user=self.user1, notification=notif).count(), 1)

    def test_create_and_send_multiple_users(self):
        notif = Notification.create_and_send([self.user1, self.user2], "Subject 2", "Message 2")
        self.assertIn(self.user1, notif.recipients.all())
        self.assertIn(self.user2, notif.recipients.all())
        self.assertEqual(UserNotification.objects.filter(notification=notif).count(), 2)

    def test_create_and_send_none(self):
        notif = Notification.create_and_send(None, "Subject 3", "Message 3")
        self.assertEqual(notif.recipients.count(), 0)
        self.assertEqual(UserNotification.objects.filter(notification=notif).count(), 0)

    def test_create_and_send_with_sender(self):
        notif = Notification.create_and_send(self.user1, "Subject Sender", "Message Sender", self.user2)
        self.assertEqual(notif.sender, self.user2)
        self.assertIn(self.user1, notif.recipients.all())
        self.assertEqual(UserNotification.objects.filter(user=self.user1, notification=notif).count(), 1)

    def test_create_and_send_without_sender(self):
        notif = Notification.create_and_send(self.user1, "Subject No Sender", "Message No Sender")
        self.assertIsNone(notif.sender)
        self.assertIn(self.user1, notif.recipients.all())

    def test_no_duplicate_user_links(self):
        notif = Notification.create_and_send([self.user1, self.user1], "Subject 4", "Message 4")
        self.assertEqual(UserNotification.objects.filter(user=self.user1, notification=notif).count(), 1)

    def test_str_method(self):
        notif = Notification.create_and_send(self.user1, "Subject 5", "Message 5")
        self.assertIn("Subject 5", str(notif))

    def test_mark_as_read_and_unread(self):
        notif = Notification.create_and_send(self.user1, "Subject 6", "Message 6")
        # Initially unread
        link = UserNotification.objects.get(user=self.user1, notification=notif)
        self.assertFalse(link.read)

        # Mark as read
        notif.mark_as_read(self.user1)
        link.refresh_from_db()
        self.assertTrue(link.read)
        self.assertIsNotNone(link.read_at)
        self.assertTrue(notif.is_read_by(self.user1))

        # Mark as unread
        notif.mark_as_unread(self.user1)
        link.refresh_from_db()
        self.assertFalse(link.read)
        self.assertIsNone(link.read_at)
        self.assertFalse(notif.is_read_by(self.user1))

    def test_is_read_by_multiple_users(self):
        notif = Notification.create_and_send([self.user1, self.user2], "Subject 7", "Message 7")
        notif.mark_as_read(self.user1)
        self.assertTrue(notif.is_read_by(self.user1))
        self.assertFalse(notif.is_read_by(self.user2))
