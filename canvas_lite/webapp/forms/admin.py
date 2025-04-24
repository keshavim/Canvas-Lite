from django.shortcuts import render, get_object_or_404, redirect
from django import forms

from webapp.models import User


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
