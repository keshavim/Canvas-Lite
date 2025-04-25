from django.shortcuts import render, get_object_or_404, redirect
from django import forms

from webapp.models import *


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'schedule', 'section_type', 'instructor']