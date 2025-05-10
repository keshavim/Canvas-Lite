from django.contrib import messages
from django import forms

import json

from webapp.models import *
from webapp.models.section import SectionType
from webapp.widgets import ScheduleWidget, ScheduleField


# forms.py
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

    def save(self, request=None, commit=True):
        instance = super().save(commit=commit)
        if request and not self.instance.pk:  # Only for creation
            messages.success(request, 'Course added successfully!')
        return instance

class SectionForm(forms.ModelForm):
    schedule = ScheduleField(widget=ScheduleWidget(), required=False)

    class Meta:
        model = Section
        fields = ['name', 'schedule', 'section_type', 'instructor', 'main_section']

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)

        # Exclude Admins from instructors
        if 'instructor' in self.fields:
            self.fields['instructor'].queryset = self.fields['instructor'].queryset.exclude(
                groups__name='Admin'
            )
        self.fields['schedule'].required = False

        # Only show main sections as possible parents for subsections
        if 'main_section' in self.fields:
            self.fields['main_section'].queryset = Section.objects.filter(
                course=self.course, section_type=SectionType.LECTURE
            )

    def save(self, commit=True):
        # Extract cleaned data
        name = self.cleaned_data['name']
        instructor = self.cleaned_data.get('instructor')
        schedule = self.cleaned_data.get('schedule')
        section_type = self.cleaned_data['section_type']
        main_section = self.cleaned_data.get('main_section')

        # Main section creation
        if not main_section and section_type == SectionType.LECTURE:
            instance = Section.create_main_section(
                course=self.course,
                sec_name=name,
                instructor=instructor,
                schedule=schedule
            )
        # Subsection creation
        elif main_section and section_type in [SectionType.LAB, SectionType.DISCUSSION]:
            instance = main_section.create_subsection(
                name=name,
                sectype=section_type,
                instructor=instructor,
                schedule=schedule
            )
        else:
            raise forms.ValidationError(
                "Invalid section type or missing main section for subsection."
            )

        if commit:
            instance.save()
        return instance


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,  # Required on add, optional on edit
        help_text="Leave blank to keep the current password."
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'phone_number', 'group_name', 'is_active', "date_joined", "description" ]