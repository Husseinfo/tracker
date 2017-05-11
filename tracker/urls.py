"""tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from tracker import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^admin/', admin.site.urls),
    url(r'^about/', view=views.about),
    url(r'^adduser/', view=views.add_user),
    url(r'^home/', view=views.home),
    url(r'^capture/', view=views.capture),
    url(r'^train/', view=views.train),
    url(r'^404/', view=views.handler404),
    url(r'^sendimage/', view=views.receive_images),
    url(r'^sendtrain/', view=views.receive_train),
    url(r'^users/', view=views.display_users),
    url(r'^delete_user/', view=views.delete_user)
]
