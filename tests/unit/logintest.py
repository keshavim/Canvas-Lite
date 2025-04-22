import unittest
from unittest.mock import Mock

from skeletons.login import login, logout

# test login function
class TestLogin(unittest.TestCase):
    # set up list of users and current users
    def setUp(self):
        self.mock_user1 = Mock()
        self.mock_user2 = Mock()
        self.mock_user3 = Mock()

        self.mock_user1.username = "user1"
        self.mock_user1.password = "password1"
        self.mock_user2.username = "user2"
        self.mock_user2.password = "password2"
        self.mock_user3.username = "user3"
        self.mock_user3.password = "password3"

        self.current_users = [self.mock_user1, self.mock_user2]
        self.users = [self.mock_user1, self.mock_user2, self.mock_user3]

    # test login with no users, should return false, current_users should be empty
    def test_login_no_users(self):
        empty_current_users = []
        empty_users = []
        request = login("username", "password", empty_current_users, empty_users)
        self.assertEqual(request, False)
        self.assertEqual(len(empty_current_users), 0)

    # test with user that does not exist
    def test_login_nonexistant_user(self):
        request = login("fake", "password3", self.current_users, self.users)
        self.assertEqual(request, False)
        self.assertEqual(len(self.current_users), 2)

    # test with user already logged in
    def test_login_current_user(self):
        request = login("user1", "password1", self.current_users, self.users)
        self.assertEqual(request, False)
        self.assertEqual(len(self.current_users), 2)

    # test with bad password and existing user
    def test_login_bad_password(self):
        request = login("user3", "password1", self.current_users, self.users)
        self.assertEqual(request, False)
        self.assertEqual(len(self.current_users), 2)

    # test with good password and existing user
    def test_login_good_password(self):
        request = login("user3", "password3", self.current_users, self.users)
        self.assertEqual(request, True)
        self.assertEqual(len(self.current_users), 3)
        self.assertIn(self.mock_user3, self.current_users)

# test logout function
class TestLogout(unittest.TestCase):
    # set up list of current users
    def setUp(self):
        self.mock_user1 = Mock()
        self.mock_user2 = Mock()
        self.mock_user3 = Mock()

        self.mock_user1.username = "user1"
        self.mock_user2.username = "user2"
        self.mock_user3.username = "user3"

        self.current_users = [self.mock_user1, self.mock_user2]

    # test with no current users
    def test_logout_no_current_users(self):
        request = logout("user1", [])
        self.assertEqual(request, False)

    # test with user not logged in
    def test_logout_not_current_user(self):
        request = logout("user3", self.current_users)
        self.assertEqual(request, False)
        self.assertEqual(len(self.current_users), 2)

    # test with user logged in
    def test_logout_current_user(self):
        request = logout("user1", self.current_users)
        self.assertEqual(request, True)
        self.assertEqual(len(self.current_users), 1)
        self.assertNotIn(self.mock_user1, self.current_users)

if __name__ == '__main__':
    unittest.main()