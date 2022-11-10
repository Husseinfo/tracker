"""tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include

from . import views
from .api import AttendanceRecord

urlpatterns = [
    path('', views.home),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'admin', admin.site.urls),
    path(r'adduser/', view=views.add_user, name='adduser'),
    path(r'home', view=views.home),
    path(r'capture', view=views.capture),
    path(r'upload', view=views.upload),
    path(r'train/', view=views.train),
    path(r'sendimage/', view=views.receive_images),
    path(r'sendtrain/', view=views.receive_train),
    path(r'users', view=views.display_users),
    path(r'deleteuser', view=views.delete_user),
    re_path(r'profile/(?P<_id>\d+)/$', view=views.profile, name="profile"),
    path(r'recognize/camera', view=views.recognize_camera),
    path(r'recognize/', view=views.receive_recognize),
    path(r'recognize/photo', view=views.recognize_photo),
    re_path(r'edituser/(?P<_id>\d+)/$', view=views.edit_user, name="edituser"),
    path(r'attendance', view=views.attendance),
    path(r'api/attendance', view=AttendanceRecord.as_view()),
]
