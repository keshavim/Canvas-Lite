
class UserManager:
    """
    Manages user creation, update, and deletion.
    """

    def register(self, user_data):
        """
        Creates a new user.

        Parameters:
            user_data (dict): A dictionary of user fields
        """
        pass

    def update(self, user_id, updates):
        """
        Updates an existing user's information.

        Parameters:
            user_id (int): The ID of the user to update
            updates (dict): Dictionary of fields to update
        """
        pass

    def delete(self, user_id):
        """
        Deletes a user from the system.

        Parameters:
            user_id (int): The ID of the user to delete
        """
        pass

class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.firstname = ""
        self.lastname = ""
        self.email = ""
        self.phone_number = 0

        self.courses = []
        self.labsections = []
        self.notifications = []

class TA(User):
    def __init__(self):
        super().__init__()
    def send_notification(self):
        pass


class Instructor(User):
    def __init__(self):
        super().__init__()
    def assign_course_to_ta(self, course):
        pass
    def assign_labsection_to_ta(self, labsection):
        pass


class Admin(User):
    def __init__(self):
        super().__init__()

    def create_course(self):
        pass
    def create_labsection(self):
        pass
    def delete_user(self):
        pass
    def delete_labsection(self):
        pass
    def delete_course(self):
        pass
    def assign_course_to_instructor(self, course):
        pass
    def assign_labsection_to_instructor(self, labsection):
        pass
