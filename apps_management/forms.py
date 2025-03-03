from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Task, User


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = User
        fields = ["username", "avatar"]  # Do not include email (not editable)
        widgets = {
            "username": forms.TextInput(attrs={"class": "p-2 border rounded w-full"}),  # Custom styling for input field
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom form for changing the user password."""

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "p-2 border rounded w-full"}),  # Styled password input
        label="Old password",
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "p-2 border rounded w-full"}),  # Styled password input
        label="New password",
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "p-2 border rounded w-full"}),  # Styled password input
        label="Confirm new password",
    )
