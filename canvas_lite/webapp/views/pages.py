from django.shortcuts import render
from django.shortcuts import redirect

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