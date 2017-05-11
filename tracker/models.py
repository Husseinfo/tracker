#!/usr/bin/env python3

from django.db import models
from django.forms import ModelForm


class User(models.Model):
    id = models.IntegerField(name='ID', primary_key=True, unique=True, auto_created=True, editable=False)
    first_name = models.CharField(name='First Name', max_length=32)
    last_name = models.CharField(name='Last Name', max_length=32)
    mail = models.CharField(name='E-mail', max_length=32)
    phone = models.IntegerField(name='Phone number')
    image = models.ImageField(name='Image')
    address = models.CharField(name='Address', max_length=128)
    birth_date = models.DateField(name='Birth date')


class Image(models.Model):
    id = models.IntegerField(name='ID', unique=True, primary_key=True, editable=False)
    image = models.ImageField(name='Image')
    user = models.ForeignKey('User')


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id']

    def is_valid(self):
        return True


class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['id']

