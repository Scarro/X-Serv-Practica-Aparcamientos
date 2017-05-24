# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegistroUserForm(forms.Form):
    username = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=5, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#    photo = forms.ImageField(required=False)

    def clean_username(self):
        #Comprueba que no exista un username igual en la db
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError("Nombre de usuario ya registrado.")
        return username

    def clean_email(self):
        #Comprueba que no exista un email nuevo en la db
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError("Ya existe un email igual.")
        return email

    def clean_password2(self):
        #Comprueba que password y password2 sean iguales.
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Las password introducidas no coinciden")
        return password2

class EditarEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super(EditarEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Comprobar si ha cambiado el email
        actual_email = self.request.user.email
        username = self.request.user.username
        if email != actual_email:
            # Si lo ha cambiado, comprobar que no exista en la db.
            # Exluye el usuario actual.
            existe = User.objects.filter(email=email).exclude(username=username)
            if existe:
                raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

class EditarColorForm(forms.Form):
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super(EditarColorForm, self).__init__(*args, **kwargs)

class EditarSizeForm(forms.Form):
    size = forms.IntegerField(max_value=30, min_value=1,label='Tamaño',widget=forms.NumberInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super(EditarSizeForm, self).__init__(*args, **kwargs)

class EditarTituloForm(forms.Form):
    titulo = forms.CharField(min_length=1, widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super(EditarTituloForm, self).__init__(*args, **kwargs)