from django.contrib.auth import views as auth_views
from django.urls import path, include

from tracker import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('accounts/', include('django.contrib.auth.urls')),

    path(r'', view=views.home, name='home'),
    path(r'capture', view=views.capture, name='capture'),
    path(r'upload', view=views.upload, name='upload'),
    path(r'train/', view=views.train, name='train'),

    path(r'users', view=views.users, name='users'),
    path(r'profile/<user_id>', view=views.profile, name="profile"),
    path(r'adduser/', view=views.add_user, name='adduser'),
    path(r'edituser/<user_id>', view=views.edit_user, name="edituser"),
    path(r'deleteuser/<user_id>', view=views.delete_user, name='deleteuser'),

    path(r'recognize', view=views.recognize, name='recognize'),
    path(r'attendance', view=views.attendance, name='attendance'),
]
