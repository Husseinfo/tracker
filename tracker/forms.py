#!/usr/bin/env python3

from django import forms

from tracker import settings
from tracker.models import User


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    mail = forms.CharField(max_length=32)
    phone = forms.CharField(max_length=32)
    image = forms.ImageField(max_length=128)
    address = forms.CharField(max_length=128)
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

