from django import forms
from .models import Comentario

class ComentarioCreateForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('titulo', 'cuerpo')
        labels = {
            'titulo': 'Titulo',
            'cuerpo': 'Texto'
            }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-control'})
            }