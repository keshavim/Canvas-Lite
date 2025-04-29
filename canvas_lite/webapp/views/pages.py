from django.shortcuts import render
from django.shortcuts import redirect


# views for non-admin users

def user_calendar(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/calendar.html")
    else:
        return redirect("/login")

def user_courses(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/course_view.html")
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