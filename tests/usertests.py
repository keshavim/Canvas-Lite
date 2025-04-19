from unittest.mock import MagicMock

from django.contrib.auth.models import Group
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
    def test_get_section_by_id(self):
        section_id = self.section2.id
        section = self.instructor2.get_assigned_section_id(section_id)
        self.assertEqual(section, self.section2)

        section_id = self.section1.id
        section = self.instructor2.get_assigned_section_id(section_id)
        self.assertNotEqual(section, self.section2)

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


class UserGroupFuncTests(TestCase):
    def setUp(self):
        # Create groups
        self.admin_group = Group.objects.create(name='Admin')
        self.instructor_group = Group.objects.create(name='Instructor')
        self.ta_group = Group.objects.create(name='TA')

        # Create users
        self.admin = User.objects.create(username='admin')
        self.instructor = User.objects.create(username='instructor')
        self.ta = User.objects.create(username='ta')

        # Assign groups
        self.admin.groups.add(self.admin_group)
        self.instructor.groups.add(self.instructor_group)
        self.ta.groups.add(self.ta_group)

        # Create a section and relate it to instructor
        self.course = Course.objects.create(name='Test Course')

        self.section = Section.objects.create(name='Section 1', course=self.course)
        if hasattr(self.instructor, 'sections_taught'):
            self.instructor.sections_taught.add(self.section)

    def test_get_user_group(self):
        self.assertEqual(self.admin.get_user_group(), 'Admin')
        self.assertEqual(self.instructor.get_user_group(), 'Instructor')
        self.assertEqual(self.ta.get_user_group(), 'TA')

    def test_set_user_group_assigns_correct_group(self):
        self.admin.set_user_group('TA')
        self.assertEqual(self.admin.get_user_group(), 'TA')
        self.admin.set_user_group('Instructor')
        self.assertEqual(self.admin.get_user_group(), 'Instructor')
        self.admin.set_user_group('Admin')
        self.assertEqual(self.admin.get_user_group(), 'Admin')

    def test_set_user_group_removes_other_groups(self):
        self.ta.set_user_group('Instructor')
        self.assertEqual(self.ta.get_user_group(), 'Instructor')
        self.assertFalse(self.ta.groups.filter(name='TA').exists())
        self.ta.set_user_group('Admin')
        self.assertEqual(self.ta.get_user_group(), 'Admin')
        self.assertFalse(self.ta.groups.filter(name='Instructor').exists())

    def test_set_user_group_invalid_group(self):
        with self.assertRaises(ValueError):
            self.instructor.set_user_group('NotAGroup')

    def test_ta_cannot_assign_user(self):
        result = self.ta.assign_user_to_section(self.instructor, self.section.id)
        self.assertIsInstance(result, PermissionError)
        self.assertEqual(str(result), "TA can not assign Users to section")

    def test_instructor_cannot_assign_admin(self):
        result = self.instructor.assign_user_to_section(self.admin, self.section.id)
        self.assertIsInstance(result, PermissionError)
        self.assertEqual(str(result), "Instructor can not assign this user to section")

    def test_instructor_cannot_assign_instructor(self):
        result = self.instructor.assign_user_to_section(self.instructor, self.section.id)
        self.assertIsInstance(result, PermissionError)
        self.assertEqual(str(result), "Instructor can not assign this user to section")

    # If you have a way for instructor to assign TA, and instructor is in the section:
    def test_instructor_can_assign_ta(self):
        # Make sure instructor is in the section
        if hasattr(self.instructor, 'is_in_section'):
            self.assertTrue(self.instructor.is_in_section(self.section.id))
        result = self.instructor.assign_user_to_section(self.ta, self.section.id)
        self.assertIsNone(result)  # Should succeed if logic allows
