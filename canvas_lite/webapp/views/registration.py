from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from webapp.forms import UserAuthenticationForm


def user_home(request):
    """shows instructor and ta dashboard. shows signup page if not logged in"""
    if request.user.groups.filter(name='Admin').exists():
        return redirect("admin_home")
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
                return redirect("admin_home")
            return redirect('home')
        else:
            # Form handles invalid username/password and adds errors
            messages.error(request, "Invalid username or password.")
    else:
        form = UserAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

