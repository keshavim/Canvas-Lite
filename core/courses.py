class CourseManager:
    """
    Manages course creation and instructor assignment.
    """

def __init__(self, course_id, course_code, title, semester, instructor_id):
    self.title = title
    self.course_id = course_id
    self.semester = semester
    self.instructor_id = instructor_id

def __str__(self):
    pass


"""
    Creates a new course.
    Parameters: course_data (dict): Dictionary of course fields
    Preconditions: course_data must contain course fields, course does
    not already exist.
    Postconditions: course is created successfully.
"""

def create_course(self, course_data):
    pass


"""
    Delete a course.
    Parameters: course_id (int): The course ID of the course to be deleted.
    Preconditions: course must exist.
    Postconditions: the course is deleted successfully (everything set to none).
"""


def delete_course(self, course_id):
    pass


"""
    Update a course's title.
    Parameters: new_title (String): The new course title.
    Preconditions: new_title is a String, does not conflict with existing course title.
    Postconditions: course is updated successfully.
"""


def update_title(self, new_id):
    pass


"""
    Return a particular course.
    Parameters: course_id (int): The course ID.
    Preconditions: course must exist.
    Postconditions: none.
"""


def get_course(self, course_id):
    pass


"""
    Update a course's id.
    Parameters: new_id (int): The new course ID.
    Preconditions: new_id is an integer, does not conflict with existing course ID.
    Postconditions: course is updated successfully.
"""


def update_id(self, new_title):
    pass


"""
    Update the semester of a coures.
    Parameters: new_semester (String): The new course semester.
    Preconditions: new_semester is a String, properly formatted as Fall/Spring, followed by a year.
    Postconditions: course is updated successfully.
"""


def update_semester(self, new_semester):
    pass


"""
    Update a course's instrucor.
    Parameters: new_instructor (int): The new instructor's ID.
    Preconditions: new_instructor is an integer, does not conflict with existing instructor.
    Postconditions: course is updated successfully.
"""


def update_instructor(self, new_instructor):
    pass
