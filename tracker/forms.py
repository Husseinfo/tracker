from django.forms import ModelForm

from .models import User, Image


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
