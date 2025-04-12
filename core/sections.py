
from BMIApp.models import LabSection
from django.core.exceptions import ObjectDoesNotExist

class SectionManager:
    """
    Manages lab section creation and TA assignments.
    """

    def create_section(self, section_data):
        """
        Creates a new lab section.
        """
        return LabSection.objects.create(
            section_number=section_data.get("section_number"),
            course_id=section_data.get("course_id"),
            assigned_ta_id=section_data.get("assigned_ta_id", None)
        )

    def assign_ta(self, lab_id, ta_id):
        """
        Assigns a TA to an existing lab section.
        """
        try:
            section = LabSection.objects.get(id=lab_id)
            section.assigned_ta_id = ta_id
            section.save()
            return section
        except ObjectDoesNotExist:
            return None
