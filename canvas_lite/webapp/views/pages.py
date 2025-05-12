
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.dateformat import format
import datetime

from webapp.forms import UpdateProfileForm



# views for non-admin users

def user_calendar(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/calendar.html")
    else:
        return redirect("/login")


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "standard_pages/user_profile.html")
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

@login_required
def calendar_events(request):
   # Example static events — replace with DB data later
   events = [
       {
           "title": "Advising Session",
           "start": str(datetime.date.today())
       },
       {
           "title": "Assignment Due",
           "start": str(datetime.date.today() + datetime.timedelta(days=2))
       },
   ]
   return JsonResponse(events, safe=False)
