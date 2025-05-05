from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

from webapp.forms import UserForm, UpdateProfileForm
from webapp.models import *

# views for non-admin users

def user_calendar(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/calendar.html")
    else:
        return redirect("/login")

def user_courses(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        courses = current_user.get_assigned_courses()
        return render(request, "standard_pages/course_view.html", {"courses": courses})
    else:
        return redirect("/login")

def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/user_profile.html")
    else:
        return redirect("/login")

def user_inbox(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/inbox.html")
    else:
        return redirect("/login")

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect("/profile")
            else:
                 messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'standard_pages/change_password.html', {'form': form})
    else:
        return redirect("/login")

def update_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("/profile") # Redirect to a success page
        else:
            form = UpdateProfileForm(instance=request.user)
        return render(request, 'standard_pages/update_user_description.html', {'form': form})
    else:
        return redirect("/login")

