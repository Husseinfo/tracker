from datetime import date
from os.path import join

from django.db import models


def get_photo_upload_path(instance, filename):
    return join(f'static/photos/{instance.user.id}_{filename}')


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    e_mail = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    image = models.ImageField(upload_to='static/profile/', name="Image")
    address = models.CharField(max_length=128)
    birth_date = models.DateField("Date", default=date.today)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.id})'


class Image(models.Model):
    id = models.IntegerField(name='ID', unique=True, primary_key=True, editable=False)
    image = models.ImageField(upload_to=get_photo_upload_path, name="Image")
    user = models.ForeignKey('User', on_delete=models.CASCADE)


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
