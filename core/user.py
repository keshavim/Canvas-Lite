
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
        """
        Sends a notification to relevant users (e.g., instructors or students).
        """
        pass


class Instructor(User):
    def __init__(self):
        super().__init__()
    def assign_course_to_ta(self, course):
         """
        Assigns a TA to a course.

        Parameters:
            course: The course object to assign a TA to
        """
        pass
    def assign_labsection_to_ta(self, labsection):
        """
        Assigns a TA to a lab section.

        Parameters:
            labsection: The lab section object to assign a TA to
        """
        pass


class Admin(User):
    def __init__(self):
        super().__init__()

    def create_course(self):
        """
        Creates a new course in the system.
        """
        pass
    def create_labsection(self):
        """
        Creates a new lab section.
        """
        pass
    def delete_user(self):
        """
        Deletes a user from the system.
        """
        pass
    def delete_labsection(self):
        """
        Deletes a lab section from the system.
        """
        pass
    def delete_course(self):
        """
        Deletes a course from the system.
        """
        pass
    def assign_course_to_instructor(self, course):
        """
        Assigns an instructor to a course.

        Parameters:
            course: The course object to assign
        """
        pass
    def assign_labsection_to_instructor(self, labsection):
        """
        Assigns a lab section to an instructor.

        Parameters:
            labsection: The lab section object to assign
        """
        pass
