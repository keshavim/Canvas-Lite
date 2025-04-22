from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from canvas_lite.models import Course

User = get_user_model()

class CreateSectionAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.faculty = User.objects.create_user(
            username='facultyuser',
            password='facultypass123',
            email='faculty@example.com'
        )
        self.client.login(username='facultyuser', password='facultypass123')

        self.course = Course.objects.create(
            name='COMPSCI 361',
            description='Software engineering'
        )

    def test_access_section_creation_page(self):
        response = self.client.get('/section/create/')  # Adjust if needed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_create_section_successfully(self):
        response = self.client.post('/section/create/', {
            'name': 'Section A',
            'course': self.course.id,
            'schedule': '{}',  # or any required fields
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        from canvas_lite.models import Section
        self.assertTrue(Section.objects.filter(name='Section A').exists())

    def test_create_section_with_missing_name_fails(self):
        response = self.client.post('/section/create/', {
            'name': '',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
