from django.shortcuts import render

def user_calendar(request):
    return render(request, "standard_pages/calendar.html")

def user_courses(request):
    return render(request, "standard_pages/course_view.html")

def user_profile(request):
    return render(request, "standard_pages/user_profile.html")

def user_inbox(request):
    return render(request, "standard_pages/inbox.html")