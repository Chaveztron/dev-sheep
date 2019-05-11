from django import forms
from django.contrib.auth.models import User
from posts.models import Author, Idioma
from django.contrib import messages
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

    def clean_first_name(self, *args, **kwargs):
        first_name = self.cleaned_data.get("first_name")
        valid_characters = 'áabcdeéfghiíjklmnoópqrstuúvwxyznAÁBCDEÉFGHIJKLMNOÓPQRSTUÚVWXYZÑ '
        if first_name == "":
            raise forms.ValidationError("Escriba su nombre por favor")
        elif not all(char in valid_characters for char in first_name):
            raise forms.ValidationError("Solo caracteres, evite los signos y emojis en el nombre")
        else:
            return first_name

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data.get("last_name")
        valid_characters = 'áabcdeéfghiíjklmnoópqrstuúvwxyznAÁBCDEÉFGHIJKLMNOÓPQRSTUÚVWXYZÑ '
        if last_name == "":
            raise forms.ValidationError("Escriba sus apellidos por favor")
        elif not all(char in valid_characters for char in last_name):
            raise forms.ValidationError("Solo caracteres, evite los signos y emojis en los apellidos")
        else:
            return last_name

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError("Es importante que tenga un email, en caso de olvidar la contraseña lo necesitara")
        else:
            return email

class ProfileUpdateForm(forms.ModelForm):
    #albun = modelformset_factory(Author, fields=('albun',), extra=6)
    idiomas = forms.ModelMultipleChoiceField(queryset=Idioma.objects.all(), widget=forms.CheckboxSelectMultiple,
                                             required=True, label='Idiomas que domina')
    profile_picture = forms.ImageField(label=('Foto de Perfil'), required=False,
                                    error_messages={'invalid': ("Solo imagenes")}, widget=forms.FileInput)
    cv = forms.FileField(label=('Curriculum PDF'), required=False, widget=forms.FileInput(attrs={
        'class': 'form-control-file',
    }))

    telefono = forms.TextInput(attrs={'type':'tel', 'class': 'form-control',})
    class Meta:
        model = Author
        fields = ['profile_picture', 'cv', 'telefono','idiomas','portada','imagen1','imagen2','imagen3','imagen4','imagen5','imagen6']

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        tipo_archivo = str(cv)
        extension = tipo_archivo[-4:]

        if cv.size > 2621440:
            raise forms.ValidationError('Suba un archivo ".pdf" menor a 2.5 MB')
        elif extension == '.pdf' or extension == '.PDF':
            return cv
        else:
            raise forms.ValidationError('Suba un archivo y asegurese que el archivo sea "PDF"')
        # 2.5MB - 2621440
        # 5MB - 5242880
        # 10MB - 10485760
        # 20MB - 20971520
        # 50MB - 5242880
        # 100MB 104857600
        # 250MB - 214958080
        # 500MB - 429916160

    def clean_telefono(self, *args, **kwargs):
        telefono = self.cleaned_data.get("telefono")
        if telefono == "":
            raise forms.ValidationError("Escriba su numero de teléfono por favor")
        else:
            return telefono

    def clean_portada(self, *args, **kwargs):
        portada = self.cleaned_data.get("portada")
        if portada.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return portada

    def clean_imagen1(self, *args, **kwargs):
        imagen1 = self.cleaned_data.get("imagen1")
        if imagen1.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return imagen1

    def clean_imagen2(self, *args, **kwargs):
        imagen2 = self.cleaned_data.get("imagen2")
        if imagen2.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return imagen2

    def clean_imagen3(self, *args, **kwargs):
        imagen3 = self.cleaned_data.get("imagen3")
        if imagen3.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return imagen3

    def clean_imagen4(self, *args, **kwargs):
        imagen4 = self.cleaned_data.get("imagen4")
        if imagen4.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return imagen4

    def clean_imagen5(self, *args, **kwargs):
        imagen5 = self.cleaned_data.get("imagen5")
        if imagen5.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return imagen5

    def clean_imagen6(self, *args, **kwargs):
        imagen6 = self.cleaned_data.get("imagen6")
        if imagen6.size > 2621440:
            raise forms.ValidationError('Suba una imagen menor a 2.5 MB')
        else:
            return imagen6

class ValidAuthor(forms.ModelForm):
    idiomas = forms.ModelMultipleChoiceField(queryset=Idioma.objects.all(), widget=forms.CheckboxSelectMultiple,
                                             required=True, label='Idiomas que domina')
    telefono = forms.TextInput(attrs={'type': 'tel'})
    class Meta:
        model = Author
        fields = ['telefono', 'idiomas']

    def clean_telefono(self, *args, **kwargs):
        telefono = self.cleaned_data.get("telefono")
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
        valid_characters = 'áabcdeéfghiíjklmnoópqrstuúvwxyznAÁBCDEÉFGHIJKLMNOÓPQRSTUÚVWXYZÑ '
        if first_name == "":
            raise forms.ValidationError("Escriba su nombre por favor")
        elif not all(char in valid_characters for char in first_name):
            raise forms.ValidationError("Solo caracteres, evite los signos y emojis")
        else:
            return first_name

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data.get("last_name")
        valid_characters = 'áabcdeéfghiíjklmnoópqrstuúvwxyznAÁBCDEÉFGHIJKLMNOÓPQRSTUÚVWXYZÑ '
        if last_name == "":
            raise forms.ValidationError("Escriba sus apellidos por favor")
        elif not all(char in valid_characters for char in last_name):
            raise forms.ValidationError("Solo caracteres, evite los signos y emojis")
        else:
            return last_name

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError("Es importante que tenga un email, en caso de olvidar la contraseña lo necesitara")
        else:
            return email
