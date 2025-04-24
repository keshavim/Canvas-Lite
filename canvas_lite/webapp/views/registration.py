from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from webapp.forms import UserRegistrationForm, UserAuthenticationForm


def user_home(request):
    """shows instructor and ta dashboard. shows signup page if not logged in"""
    return render(request, "dashboard.html")

def user_login(request):
    """
    Authenticates and logs in a webapp.
    Returns home page if login is successful,
    refresh page with an error message otherwise.
    """
    if request.method == "POST":
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.groups.filter(name='Admin').exists():
                return redirect("/sudo/")
            return redirect('/')
        else:
            # Form handles invalid username/password and adds errors
            messages.error(request, "Invalid username or password.")
    else:
        form = UserAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    """
    creates a user with the information given
    logs in user and redirects to dashboard if sucessful.
    refreshes page with error message otherwise.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Username uniqueness and password safety are checked in the form
            user = form.create_user()
            login(request, user)
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect('/')
        else:
            # Form errors (including username taken, weak password, etc.) will be displayed
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {"form": form})
