
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UserManager:
    """
    Handles user creation, update, and deletion.
    """

    def create_user(self, user_data):
        """
        Creates a new user using the built-in User model.
        """
        return User.objects.create_user(
            username=user_data.get("username"),
            email=user_data.get("email"),
            password=user_data.get("password"),
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", "")
        )

    def update_user(self, user_id, updates):
        """
        Updates existing user information.
        """
        try:
            user = User.objects.get(id=user_id)
            for key, value in updates.items():
                setattr(user, key, value)
            user.save()
            return user
        except ObjectDoesNotExist:
            return None

    def delete_user(self, user_id):
        """
        Deletes a user if found.
        """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False
