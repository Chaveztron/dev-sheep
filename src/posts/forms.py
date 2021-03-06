from django import forms
from tinymce import TinyMCE
from .models import Post, Comment, Category
from django.forms.widgets import CheckboxSelectMultiple


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, label='',
                            widget=forms.TextInput(attrs={"placeholder": "Escriba el titulo de la oferta de trabajo aqui (max 100 letras)", 'onkeyup' :"countChars(this);"}))
    overview = forms.CharField(
                        required=True, label='',
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Escriba un breve descripción de la oferta de trabajo, max(220 letras), min(21 letras)",
                                    "class": "new-class-name two",
                                    "id": "my-id-for-textarea",
                                    "rows": 2,
                                    'cols': 120,
                                    'onkeyup': "countChars2(this);",
                                }
                            )
                        )
    categories = forms.ModelMultipleChoiceField(label='Categoría de la oferta (seleccione al menos una para que se publique la oferta)', queryset=Category.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={
    }), required=True)
    content = forms.CharField(required=True, label='Escriba la información completa de la oferta aquí',
        widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 30, 'rows': 10}
        )
    )

    thumbnail = forms.ImageField(required=True, label='Imagen de previa vista (se mostrara como principal en las publicaciones)')

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail',
                  'categories',)

        def clean_thumbnail(self, *args, **kwargs):
            thumbnail = self.cleaned_data.get("thumbnail")
            tipo_archivo = str(thumbnail)
            extension = tipo_archivo[-4:]

            if thumbnail.size > 5242880:
                raise forms.ValidationError('Suba una imagen menor a 5 MB')
            elif extension == '.jpg' or extension == 'PEG' or extension == '.gif' or extension == '.PNG' or extension == '.png' or extension == '.BMP' or extension == '.bmp':
                return thumbnail
            else:
                raise forms.ValidationError('En la imagen de la miniatura, debe de ser JPG, GIF, PNG y BMP')

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        valid_characters = 'áabcdeéfghiíjklmnoópqrstuúvwxyznAÁBCDEÉFGHIJKLMNOÓPQRSTUÚVWXYZÑ 1234567890,.¿?¡!'
        if len(title) > 100:
            raise forms.ValidationError("Tu titulo no debe de exceder 100 letras")
        elif len(title) < 10:
            raise forms.ValidationError("Tu titulo es demasiado corto, escriba más de 10 letras")
        elif not all(char in valid_characters for char in title):
            raise forms.ValidationError("Solo caracteres, evite los signos y emojis")
        else:
            python = title
            dicPalabras = python.split(' ')
            dic = []
            count = 0
            for palabra in dicPalabras:
                if len(palabra) > 15:
                    word = []
                    for letra in palabra:
                        count = count + 1
                        if count % 15 == 0:
                            word.append('\n')
                            word.append(letra)
                        else:
                            word.append(letra)
                    palabra = ''.join(word)
                    dic.append(palabra)
                else:
                    dic.append(palabra)

            title = ' '.join(dic)

            return title

    def clean_overview(self, *args, **kwargs):
        overview = self.cleaned_data.get("overview")
        valid_characters = 'áabcdeéfghiíjklmnoópqrstuúvwxyznAÁBCDEÉFGHIJKLMNOÓPQRSTUÚVWXYZÑ 1234567890,.'
        if len(overview) > 220:
            raise forms.ValidationError("Tu descripción no debe de exceder 220 letras")
        elif len(overview) < 20:
            raise forms.ValidationError("Tu descripción es demasiado corto, escriba más de 20 letras")
        elif not all(char in valid_characters for char in overview):
            raise forms.ValidationError("Solo caracteres, evite los signos y emojis")
        else:
            python = overview
            dicPalabras = python.split(' ')
            dic = []
            count = 0
            for palabra in dicPalabras:
                if len(palabra) > 33:
                    word = []
                    for letra in palabra:
                        count = count + 1
                        if count % 33 == 0:
                            word.append('\n')
                            word.append(letra)
                        else:
                            word.append(letra)
                    palabra = ''.join(word)
                    dic.append(palabra)
                else:
                    dic.append(palabra)

            overview =' '.join(dic)

            return overview


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Escribe tu peticion',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content',)
