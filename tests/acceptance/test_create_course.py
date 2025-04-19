from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class CreateCourseAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.client.login(username='admin', password='adminpass123')

    def test_access_course_creation_page(self):
        response = self.client.get('/course/create/')  # Adjust if different
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_create_course_successfully(self):
        response = self.client.post('/course/create/', {
            'name': 'COMPSCI 361',
            'description': 'Software engineering course'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        from canvas_lite.models import Course
        self.assertTrue(Course.objects.filter(name='COMPSCI 361').exists())

    def test_create_course_with_blank_name_fails(self):
        response = self.client.post('/course/create/', {
            'name': '',
            'description': 'This should fail'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")  # Adjust if using custom error