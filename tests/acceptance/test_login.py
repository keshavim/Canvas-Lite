from django.test import TestCase
from django.urls import reverse

from webapp.models import User

class LoginAcceptanceTest(TestCase):
    def setUp(self):

        self.credentials = {
            'username': 'keshab',
            'password': 'keshab123'
        }
        User.objects.create_user(**self.credentials)
        self.login_url = reverse("login")


    def test_login_success(self):
        response = self.client.post(self.login_url, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_empty_fields(self):
        response = self.client.post(self.login_url, {'username': '', 'password': ''}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

class LogoutAcceptanceTest(TestCase):
    login_url = '/login/'
    logout_url = '/accounts/logout/'

    def setUp(self):
        self.credentials = {
            'username': 'keshab',
            'password': 'keshab123'
        }
        User.objects.create_user(**self.credentials)


    def test_logout_success(self):
        # First, log in the user
        self.client.post(self.login_url, self.credentials, follow=True)
        # Now, log out
        response = self.client.post(self.logout_url, follow=True)
        # Check if the user is logged out
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_without_login(self):
        # Try logging out without logging in
        response = self.client.get(self.logout_url, follow=True)
        # The user should still be anonymous
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_clears_session(self):
        self.client.post(self.login_url, self.credentials, follow=True)
        self.client.post(self.logout_url, follow=True)
        # Check session is empty
        session = self.client.session
        self.assertFalse('_auth_user_id' in session)
