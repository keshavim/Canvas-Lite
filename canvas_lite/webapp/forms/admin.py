from django.contrib import messages
from django import forms

import json

from webapp.models import *
from webapp.widgets import ScheduleWidget


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


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
    class Meta:
        model = Section
        fields = ['name', 'schedule', 'section_type', 'instructor']
        widgets = {
            'schedule': ScheduleWidget(),
        }
    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)  # Remove course from kwargs
        super().__init__(*args, **kwargs)  # Now passes clean kwargs

        # Filter instructors excluding Admin group members
        if 'instructor' in self.fields:
            self.fields['instructor'].queryset = self.fields['instructor'].queryset.exclude(
                groups__name='Admin'
            )

        self.fields['schedule'].required = False  # Make entire JSON optional

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.course:
            instance.course = self.course
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