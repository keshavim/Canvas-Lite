# forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect

from webapp.models import User, UserNotification

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


class UpdateProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=False, label="Updated Phone Number")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}) ,max_length=150, required=False, label="Updated Information")
    class Meta:
        model = User
        fields = ['phone_number', 'description']

class SendMessageForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True,
        label= 'Recipients',
        help_text= 'Hold Ctrl (Windows) or Cmd (Mac) to select multiple users.',
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=True
    )

    all_users = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Send to all users"
        )

@login_required
def toggle_notification_read(request, pk):
    notification = get_object_or_404(UserNotification, pk=pk, user=request.user)
    if notification.read:
        notification.mark_as_unread()
    else:
        notification.mark_as_read()
    # Redirect back to the page you came from or a default page
    return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))