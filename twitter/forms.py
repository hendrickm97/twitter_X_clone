from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Digite o que você está pensando!",
            "class": "form-control",
        }
    ),
      label="",
    )
    class Meta:
        model = Tweet
        exclude = ("user", "likes")


class SingUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(label="", max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Sobrenome'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SingUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuário'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form text text muted"><small>Obrigatório, 150 caracteres ou menos. Somente letras, dígitos e @/./+/-.</small>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form text text muted small"><li> Sua senha não pode ser muito parecida com suas outras informações pessoais.</li><li>Sua senha não foi salva</li> </ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form text text muted small"> <small> Digite a mesma senha de antes, para validação </small> </span>'