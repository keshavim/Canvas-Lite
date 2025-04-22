from django.contrib import messages
from django.contrib.auth import authenticate, forms, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm




def user_home(request):
    return render(request, "dashboard.html")
def user_login(request):
    """
    Authenticates and logs in a webapp.
    Returns home page if login is successful,
    refresh page with an error message otherwise.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            # Form handles invalid username/password and adds errors
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # Check if a webapp with the provided username already exists
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            if user.exists():
                messages.info(request, "Username already taken!")
            else:
                user = form.create_user()
                user.save()
                login(request, user)
                messages.info(request, "Account created Successfully!")
                return redirect('/')

    form = UserRegistrationForm()
    return render(request, 'registration/register.html', {"form":form})

