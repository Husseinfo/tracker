#!/usr/bin/env python3

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    mail = forms.CharField(max_length=32, widget=forms.EmailInput)
    phone = forms.IntegerField('Phone number')
    image = forms.ImageField('Image')
    address = forms.CharField(max_length=128)
    birth_date = forms.DateField(widget=forms.DateInput)
