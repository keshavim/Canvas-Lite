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
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'group_name', 'is_active' ]