from django import forms
from django.contrib.auth.models import User
from posts.models import Author, Idioma
from django.forms.widgets import CheckboxSelectMultiple
#from django.forms import modelformset_factory
from phone_field import PhoneField


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
    idiomas = forms.ModelMultipleChoiceField(queryset=Idioma.objects.all(), widget=forms.CheckboxSelectMultiple,
                                             required=True, label='Idiomas que domina')
    class Meta:
        model = Author
        fields = ['telefono', 'idiomas']

    def clean_telefono(self, *args, **kwargs):
        telefono = self.cleaned_data.get("telefono")
        print(telefono)
        if telefono == "":
            raise forms.ValidationError("Escriba su numero de teléfono por favor")
        else:
            return telefono

class ValidUser(forms.ModelForm):
    email = forms.EmailInput(attrs={'placeholder': 'Correo electronico'})
    first_name = forms.TextInput(attrs={'placeholder': 'Nombre'})
    last_name = forms.TextInput(attrs={'placeholder': 'Apellidos'})
    username = forms.TextInput(attrs={'placeholder': 'username'})

    class Meta:
        model = User
        fields = ( 'username', 'email', 'first_name', 'last_name',)

    def clean_first_name(self, *args, **kwargs):
        first_name = self.cleaned_data.get("first_name")
        if first_name == "":
            raise forms.ValidationError("Escriba su nombre por favor")
        else:
            return first_name

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data.get("last_name")
        if last_name == "":
            raise forms.ValidationError("Escriba sus apellidos por favor")
        else:
            return last_name

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError("Es importante que tenga un email, en caso de olvidar la contraseña lo necesitara")
        else:
            return email
