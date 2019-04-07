from django import forms
from django.contrib.auth.models import User
from posts.models import Author


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['profile_picture']
