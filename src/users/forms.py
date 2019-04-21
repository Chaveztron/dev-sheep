from django import forms
from django.contrib.auth.models import User
from posts.models import Author, Idioma
from django.forms.widgets import CheckboxSelectMultiple
#from django.forms import modelformset_factory

class UserUpdateForm(forms.ModelForm):


    class Meta:
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@domino.com'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo: user369, Jesus54...'}),
        }
        fields = ['username', 'email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    #albun = modelformset_factory(Author, fields=('albun',), extra=6)
    idiomas = forms.ModelMultipleChoiceField(queryset=Idioma.objects.all(), widget=forms.CheckboxSelectMultiple,
                                             required=True, label='Idiomas que domina')
    profile_picture = forms.ImageField(label=('Foto de Perfil'), required=False,
                                    error_messages={'invalid': ("Solo imagenes")}, widget=forms.FileInput)
    cv = forms.FileField(label=('Curriculum PDF'), required=False,
                                    error_messages={'invalid': ("Curriculum en pdf")}, widget=forms.FileInput)
    class Meta:
        model = Author
        fields = ['profile_picture', 'cv', 'telefono','idiomas','portada','imagen1','imagen2','imagen3','imagen4','imagen5','imagen6']


class ValidAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = []

