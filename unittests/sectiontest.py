import unittest

class Section:
    """
    Represents a lab section in the system.
    """
    def __init__(self, section_number, course_id, schedule="", assigned_ta_id=None):
        self.section_number = section_number
        self.course_id = course_id
        self.schedule = schedule
        self.assigned_ta_id = assigned_ta_id

class SectionManager:
    """
    Manages lab section creation, update, deletion, and TA assignments.
    """
    def __init__(self):
        self.sections = {}
        self.next_id = 1

    def create_section(self, section_data):
        section_id = self.next_id
        self.next_id += 1
        self.sections[section_id] = Section(**section_data)
        return section_id

    def update_section(self, section_id, updates):
        if section_id not in self.sections:
            raise ValueError("Section not found")
        section = self.sections[section_id]
        for key, value in updates.items():
            if hasattr(section, key):
                setattr(section, key, value)
            else:
                raise KeyError(f"Invalid field: {key}")

    def delete_section(self, section_id):
        if section_id not in self.sections:
            raise ValueError("Section not found")
        del self.sections[section_id]

    def assign_ta(self, section_id, ta_id):
        if section_id not in self.sections:
            raise ValueError("Section not found")
        self.sections[section_id].assigned_ta_id = ta_id


class TestSectionManager(unittest.TestCase):
    def setUp(self):
        self.manager = SectionManager()

    def test_create_section(self):
        section_data = {
            "section_number": "301",
            "course_id": 1,
            "schedule": "MWF 9-10"
        }
        section_id = self.manager.create_section(section_data)
        section = self.manager.sections[section_id]
        self.assertEqual(section.section_number, "301")
        self.assertEqual(section.course_id, 1)
        self.assertEqual(section.schedule, "MWF 9-10")
        self.assertIsNone(section.assigned_ta_id)

    def test_update_section(self):
        sid = self.manager.create_section({
            "section_number": "301",
            "course_id": 1,
            "schedule": "MWF 9-10"
        })
        self.manager.update_section(sid, {"schedule": "TTh 11-12"})
        self.assertEqual(self.manager.sections[sid].schedule, "TTh 11-12")

    def test_delete_section(self):
        sid = self.manager.create_section({
            "section_number": "302",
            "course_id": 1
        })
        self.manager.delete_section(sid)
        self.assertNotIn(sid, self.manager.sections)

    def test_assign_ta(self):
        sid = self.manager.create_section({
            "section_number": "303",
            "course_id": 2
        })
        self.manager.assign_ta(sid, 1001)
        self.assertEqual(self.manager.sections[sid].assigned_ta_id, 1001)


if __name__ == "__main__":
    unittest.main()
