from django.test import TestCase, Client
from webapp.models import User


class UserCreationAcceptanceTest(TestCase):
    user_create_url = '/admin/webapp/user/add/' # Replace with actual URL if different
    def setUp(self):
        self.client = Client()

        # Create and login an admin user
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')

    def test_admin_can_access_user_creation_page(self):
        """
        Acceptance test: Admin should be able to access the user creation page
        """
        response = self.client.get(self.user_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")  # Assuming there's a form tag in the page

    def test_admin_can_create_new_user(self):
        """
        Acceptance test: Admin can create a new user using the form
        """
        new_user_data = {
            'username': 'newfaculty',
            'email': 'faculty@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(self.user_create_url, new_user_data, follow=True)  # Replace with actual URL
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newfaculty').exists())

    def test_user_creation_fails_with_mismatched_passwords(self):
        """
        Acceptance test: Creating a user with mismatched passwords should fail
        """
        invalid_data = {
            'username': 'baduser',
            'email': 'baduser@example.com',
            'password1': 'Pass123!',
            'password2': 'WrongPass!',
        }
        response = self.client.post(self.user_create_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())
        self.assertContains(response, "The two password fields didn’t match")  # Django default error