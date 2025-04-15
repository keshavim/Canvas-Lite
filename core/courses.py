class Course(object):
    """
        Manages course creation and instructor assignment.
        Parameters:
        course_id (int) - course's id, must be present
        title (String) - course title, must be present
        semester (String) - semester, the semester of the course (Fall, Spring)- defaults to Fall
        instructor_id (int) - instructor id, the instructor of the course- defaults to 0
        Preconditions: all input is properly formatted.
        Postconditions: a course is created.
    """


    def __init__(self, course_id, title, semester="Fall", instructor_id=0):
        self.course_id = course_id
        self.title = title
        self.semester = semester
        self.instructor_id = instructor_id


    """ 
        Displays the course as a string. Format: [course_id] [title] [semester] [instructor_id]
        Parameters: none
        Preconditions: the course exists.
        Postconditions: none.
    """


    def __str__(self):
        pass


    """
        Delete a course.
        Parameters: none.
        Preconditions: course must exist.
        Postconditions: the course is deleted successfully (everything set to none).
    """


    def delete_course(self):
        pass


    """
            Update a course's id.
            Parameters: new_id (int): The new course ID.
            Preconditions: course has not been deleted, new_id is an integer
            Postconditions: course is updated successfully.
    """


    def update_id(self, new_id):
        pass


    """
            Update a course's title.
            Parameters: new_title (String): The new course title.
            Preconditions: course has not been deleted, new_title is a String.
            Postconditions: course is updated successfully.
    """


    def update_title(self, new_title):
        pass


    """
        Update the semester of a coures.
        Parameters: new_semester (String): The new course semester.
        Preconditions: course has not been deleted, new_semester is a String, properly formatted as Fall/Spring.
        Postconditions: course is updated successfully.
    """


    def update_semester(self, new_semester):
        pass


    """
        Update a course's instrucor.
        Parameters: new_instructor (int): The new instructor's ID.
        Preconditions: course has not been deleted, new_instructor is an integer.
        Postconditions: course is updated successfully.
    """


    def update_instructor(self, new_instructor):
        pass

class Course:
    def __init__(self):
        self.course_id = None
        self.course_code = None
        self.title = None
        self.semester = None
        self.instructor_id = None

    # Add methods as needed
    pass


class LabSection:
    def __init__(self):
        self.lab_id = None
        self.section_number = None
        self.course_id = None
        self.assigned_ta_id = None

    # Add methods as needed
    pass


class Assignment:
    def __init__(self):
        self.assignment_id = None
        self.ta_id = None
        self.course_id = None
        self.type = None
        self.num_labs = None

    # Add methods as needed
    pass


class Notification:
    def __init__(self):
        self.notification_id = None
        self.sender_id = None
        self.recipient_id = None
        self.message = None
        self.timestamp = None

    # Add methods as needed
    pass

