

from django.test import TestCase
from webapp.models import Course, Section, User, Notification, UserNotification
from django.utils import timezone


class UserSectionMethodTests(TestCase):
    def setUp(self):
        # Create users
        self.instructor1 = User.objects.create_user(username='instructor1', password='test')
        self.instructor2 = User.objects.create_user(username='instructor2', password='test')

        # Create courses
        self.course1 = Course.objects.create(name='Math 101')
        self.course2 = Course.objects.create(name='Biology 102')

        # Create sections
        self.section1 = Section.objects.create(
            course=self.course1,
            name='Math 101 - Section A',
            instructor=self.instructor1,
            schedule={'day': 'Monday'}
        )
        self.section2 = Section.objects.create(
            course=self.course1,
            name='Math 101 - Section B',
            instructor=self.instructor2,
            schedule={'day': 'Wednesday'}
        )
        self.section3 = Section.objects.create(
            course=self.course2,
            name='Biology 102 - Section A',
            instructor=self.instructor1,
            schedule={'day': 'Friday'}
        )

    def test_get_assigned_sections(self):
        sections = self.instructor1.get_assigned_sections()
        self.assertEqual(sections.count(), 2)
        self.assertIn(self.section1, sections)
        self.assertIn(self.section3, sections)

        sections2 = self.instructor2.get_assigned_sections()
        self.assertEqual(sections2.count(), 1)
        self.assertIn(self.section2, sections2)

    def test_get_assigned_courses(self):
        courses = self.instructor1.get_assigned_courses()
        # instructor1 teaches sections in course1 and course2
        self.assertEqual(set(courses), {self.course1, self.course2})

        courses2 = self.instructor2.get_assigned_courses()
        self.assertEqual(list(courses2), [self.course1])

    def test_is_in_course(self):
        self.assertTrue(self.instructor1.is_in_course(self.course1.id))
        self.assertTrue(self.instructor1.is_in_course(self.course2.id))
        self.assertFalse(self.instructor2.is_in_course(self.course2.id))

    def test_is_in_section(self):
        self.assertTrue(self.instructor1.is_in_section(self.section1.id))
        self.assertTrue(self.instructor1.is_in_section(self.section3.id))
        self.assertFalse(self.instructor1.is_in_section(self.section2.id))



class NotificationMethodTests(TestCase):
    def setUp(self):
        # Create users
        self.sender = User.objects.create_user(username='sender', password='test')
        self.recipient1 = User.objects.create_user(username='recipient1', password='test')
        self.recipient2 = User.objects.create_user(username='recipient2', password='test')

        # Create notifications
        self.n1 = Notification.objects.create(sender=self.sender)
        self.n2 = Notification.objects.create(sender=self.sender)
        self.n3 = Notification.objects.create(sender=self.recipient1)

        # Link notifications to recipients
        # n1 to recipient1 (unread), recipient2 (read)
        UserNotification.objects.create(user=self.recipient1, notification=self.n1, read=False)
        UserNotification.objects.create(user=self.recipient2, notification=self.n1, read=True, read_at=timezone.now())
        # n2 to recipient1 (read)
        UserNotification.objects.create(user=self.recipient1, notification=self.n2, read=True, read_at=timezone.now())
        # n3 to recipient2 (unread)
        UserNotification.objects.create(user=self.recipient2, notification=self.n3, read=False)

    def test_get_notifications(self):
        # recipient1 should have 2 UserNotification objects (n1, n2)
        notes = self.recipient1.get_notifications()
        self.assertEqual(notes.count(), 2)
        self.assertSetEqual(set(n.notification for n in notes), {self.n1, self.n2})

        # recipient2 should have 2 UserNotification objects (n1, n3)
        notes2 = self.recipient2.get_notifications()
        self.assertEqual(notes2.count(), 2)
        self.assertSetEqual(set(n.notification for n in notes2), {self.n1, self.n3})

    def test_get_sent_notifications(self):
        # sender sent n1 and n2
        sent = self.sender.get_sent_notifications()
        self.assertSetEqual(set(sent), {self.n1, self.n2})
        # recipient1 sent n3
        sent2 = self.recipient1.get_sent_notifications()
        self.assertSetEqual(set(sent2), {self.n3})

    def test_get_read_notifications(self):
        # recipient1 has n2 (read), not n1
        reads = self.recipient1.get_read_notifications()
        self.assertEqual(reads.count(), 1)
        self.assertEqual(reads[0].notification, self.n2)

        # recipient2 has only n1 (read)
        reads2 = self.recipient2.get_read_notifications()
        self.assertEqual(reads2.count(), 1)
        self.assertEqual(reads2[0].notification, self.n1)

    def test_get_unread_notifications(self):
        # recipient1 has n1 (unread)
        unreads = self.recipient1.get_unread_notifications()
        self.assertEqual(unreads.count(), 1)
        self.assertEqual(unreads[0].notification, self.n1)

        # recipient2 has n3 (unread)
        unreads2 = self.recipient2.get_unread_notifications()
        self.assertEqual(unreads2.count(), 1)
        self.assertEqual(unreads2[0].notification, self.n3)
