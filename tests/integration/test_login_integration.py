from django.test import TestCase
from webapp.models import User
from skeletons.login import login, logout

class LoginIntegrationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.user3 = User.objects.create_user(username="user3", password="password3")
        self.current_users = [self.user1, self.user2]
        self.users = [self.user1, self.user2, self.user3]

    def test_login_no_users(self):
        empty_current_users = []
        empty_users = []
        result = login("username", "password", empty_current_users, empty_users)
        self.assertFalse(result)
        self.assertEqual(len(empty_current_users), 0)

    def test_login_nonexistent_user(self):
        result = login("fake", "password3", self.current_users, self.users)
        self.assertFalse(result)
        self.assertEqual(len(self.current_users), 2)

    def test_login_current_user(self):
        result = login("user1", "password1", self.current_users, self.users)
        self.assertFalse(result)
        self.assertEqual(len(self.current_users), 2)

    def test_login_bad_password(self):
        result = login("user3", "password1", self.current_users, self.users)
        self.assertFalse(result)
        self.assertEqual(len(self.current_users), 2)

    def test_login_good_password(self):
        result = login("user3", "password3", self.current_users, self.users)
        self.assertTrue(result)
        self.assertEqual(len(self.current_users), 3)
        self.assertIn(self.user3, self.current_users)

class LogoutIntegrationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.user3 = User.objects.create_user(username="user3", password="password3")
        self.current_users = [self.user1, self.user2]

    def test_logout_no_current_users(self):
        result = logout("user1", [])
        self.assertFalse(result)

    def test_logout_not_current_user(self):
        result = logout("user3", self.current_users)
        self.assertFalse(result)
        self.assertEqual(len(self.current_users), 2)

    def test_logout_current_user(self):
        result = logout("user1", self.current_users)
        self.assertTrue(result)
        self.assertEqual(len(self.current_users), 1)
        self.assertNotIn(self.user1, self.current_users)
