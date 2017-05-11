#!/usr/bin/env python3
import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from tracker import settings


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    mail = forms.CharField(max_length=32)
    phone = forms.CharField(max_length=32)
    image = forms.ImageField(max_length=128)
    address = forms.CharField(max_length=128)
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
