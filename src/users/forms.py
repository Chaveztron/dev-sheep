from django import forms
from django.contrib.auth.models import User
from posts.models import Author, Idioma
from django.forms.widgets import CheckboxSelectMultiple

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    idiomas = forms.ModelMultipleChoiceField(queryset=Idioma.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    class Meta:
        model = Author
        fields = ['profile_picture', 'cv', 'telefono','idiomas']


class ValidAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = []

