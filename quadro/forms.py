from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cartao, Coluna # Adicionar Coluna

class CartaoForm(forms.ModelForm):
    class Meta:
        model = Cartao
        fields = ['titulo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do cartão'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição...'}),
        }

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

# NOVO FORMULÁRIO PARA COLUNA
class ColunaForm(forms.ModelForm):
    class Meta:
        model = Coluna
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Título da nova coluna'
            }),
        }