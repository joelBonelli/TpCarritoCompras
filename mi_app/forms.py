from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Correo electrónico o contraseña incorrectos')
        return self.cleaned_data

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(required=True)
    apellido = forms.CharField(required=True)
    dni = forms.CharField(required=True)

    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'apellido', 'dni', 'password1', 'password2')