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

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if len(title) > 100:
            raise forms.ValidationError("Tu titulo no debe de exceder 100 letras")
        elif len(title) < 10:
            raise forms.ValidationError("Tu titulo es demasiado corto, escriba más de 10 letras")
        else:
            return title

    def clean_overview(self, *args, **kwargs):
        overview = self.cleaned_data.get("overview")
        if len(overview) > 220:
            raise forms.ValidationError("Tu descripción no debe de exceder 220 letras")
        elif len(overview) < 20:
            raise forms.ValidationError("Tu descripción es demasiado corto, escriba más de 20 letras")
        else:
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
