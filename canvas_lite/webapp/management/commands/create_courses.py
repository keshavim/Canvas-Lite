from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from webapp.models import Course, Section


class Command(BaseCommand):
    help = 'Creates default courses and sections'

    def handle(self, *args, **options):
        # Remove instructor creation code since we don't need it

        # Default courses
        courses_data = [
            {
                'name': 'Introduction to Python',
                'description': 'Fundamentals of Python programming'
            },
            {
                'name': 'Web Development',
                'description': 'Building modern web applications'
            },
            {
                'name': 'Database Systems',
                'description': 'Relational databases and SQL'
            }
        ]

        # Default sections with null schedule and no instructor
        sections_data = [
            {
                'course_name': 'Introduction to Python',
                'sections': [
                    {
                        'name': 'LEC-01',
                        "schedule": {
                            "days": ["Monday", "Wednesday"],
                            "start_time": "09:00",
                            "end_time": "11:30",
                            "semester": "Fall",
                            "year": 2023
                        },
                        'section_type': 'LEC'
                    },
                    {
                        'name': 'LAB-01',
                        "schedule": {
                            "days": ["Friday"],
                            "start_time": "09:00",
                            "end_time": "11:30",
                            "semester": "Fall",
                            "year": 2023
                        },
                        'section_type': 'LAB',
                        'main_section': 'LEC-01'
                    }
                ]
            },
            {
                'course_name': 'Web Development',
                'sections': [
                    {
                        'name': 'LEC-01',
                        "schedule": {
                            "days": ["Tuesday", "Wednesday"],
                            "start_time": "09:00",
                            "end_time": "11:30",
                            "semester": "Fall",
                            "year": 2023
                        },
                        'section_type': 'LEC'
                    },
                    {
                        'name': 'DIS-01',
                        "schedule": {
                            "days": ["Monday", "Wednesday"],
                            "start_time": "09:00",
                            "end_time": "11:30",
                            "semester": "Fall",
                            "year": 2023
                        },
                        'section_type': 'DIS',
                        'main_section': 'LEC-01'
                    }
                ]
            }
        ]

        # Create courses
        created_courses = {}
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_data['name'],
                defaults=course_data
            )
            created_courses[course.name] = course
            self.stdout.write(f"Created course: {course.name}")

        # Create sections
        for course_sections in sections_data:
            course = created_courses.get(course_sections['course_name'])

            if not course:
                self.stderr.write(f"Course not found: {course_sections['course_name']}")
                continue

            for section_data in course_sections['sections']:
                try:
                    main_section_obj = None
                    if section_data.get('main_section'):
                        main_section_obj = Section.objects.get(
                            course=course,
                            name=section_data['main_section']
                        )

                    section, created = Section.objects.get_or_create(
                        course=course,
                        name=section_data['name'],
                        defaults={
                            'schedule': section_data['schedule'],
                            'section_type': section_data['section_type'],
                            'instructor': None,  # Explicitly set to None
                            'main_section': main_section_obj
                        }
                    )

                    if created:
                        self.stdout.write(f"Created section: {course.name} - {section.name}")
                    else:
                        self.stdout.write(f"Section exists: {course.name} - {section.name}")

                except Section.DoesNotExist:
                    self.stderr.write(
                        f"Main section not found: {course.name} - {section_data.get('main_section')}. "
                        f"Skipping {section_data['name']}"
                    )
                except Exception as e:
                    self.stderr.write(
                        f"Error creating section {course.name} - {section_data['name']}: {str(e)}"
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created default data'))
