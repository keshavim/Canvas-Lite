# forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm


from webapp.models import User

"""
form for athenticating the user
can take either email or username as an identifier

"""
class UserAuthenticationForm(forms.Form):
    identifier = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    #runs during init
    def clean(self):
        identifier = self.cleaned_data.get('identifier')
        password = self.cleaned_data.get('password')
        # Try to fetch user by username first, then by email
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email__iexact=identifier)
            except User.DoesNotExist:
                user = None

        if user is not None:
            self.user = authenticate(
                self.request,
                username=user.username,  # Always pass username to authenticate
                password=password
            )
        if self.user is None:
            raise forms.ValidationError("Invalid username/email or password.")
        return self.cleaned_data

    def get_user(self):
        return self.user

"""
creates a user with the information given
validates username and password
"""
class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    email = forms.EmailField(required=False, label="Email")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def create_user(self):
        # Create the user instance and save it to the database
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data.get('email', '')
        )
        return user

class UpdateProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=False, label="Updated Phone Number")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}) ,max_length=150, required=False, label="Updated Information")
    class Meta:
        model = User
        fields = ['phone_number', 'description']