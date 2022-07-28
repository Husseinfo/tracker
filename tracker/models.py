from datetime import date

from django.db import models
from django.forms import ModelForm


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    e_mail = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    image = models.ImageField(upload_to='static/profile/', name="Image")
    address = models.CharField(max_length=128)
    birth_date = models.DateField("Date", default=date.today)


class Image(models.Model):
    id = models.IntegerField(name='ID', unique=True, primary_key=True, editable=False)
    image = models.ImageField(name='Image')
    user = models.ForeignKey('User', on_delete=models.CASCADE)


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


class Attendance(models.Model):
    id = models.AutoField(name='id', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("date")
    inout = models.BooleanField("inout", null=True)


class Task(models.Model):
    id = models.AutoField(name='id', primary_key=True)
    name = models.CharField(max_length=32)


class UserTask(models.Model):
    id = models.AutoField(name='id', primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("task", "user"),)
