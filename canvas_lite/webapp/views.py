from django.contrib import messages
from django.contrib.auth import authenticate, forms, login
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
        #can add email to this
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a webapp with the provided username exists
        #this part may change
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/webapp/login/')

        # Authenticate the webapp with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/webapp/login/')
        else:
            login(request, user)
            return redirect('/')
    return render(request, 'registration/login.html', {'form':forms.AuthenticationForm})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # Check if a webapp with the provided username already exists


        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            if user.exists():
                messages.info(request, "Username already taken!")
                return redirect('/webapp/register/')

            user = form.save()
            user.save()
            login(request, user)

        messages.info(request, "Account created Successfully!")
        return redirect('/')

    # Render the registration page template (GET request)
    return render(request, 'registration/register.html', {"form":UserRegistrationForm})

