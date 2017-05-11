#!/usr/bin/env python3

from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.contrib.auth import authenticate, login as _login, logout as _logout
from tracker.models import UserForm, User
from tracker import trainer, train_file_name
from tracker import utility
import base64
import os


def home(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, "home.html",
                  {'photos': trainer.get_nbr_photos(),
                   'users': User.objects.count(),
                   'last_training': utility.time_spent(os.path.getmtime(train_file_name))},)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            _login(request, user)
            return redirect(home)
        else:
            return render(request, 'login.html')
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return redirect(home)
        return render(request, 'login.html')


def logout(request):
    _logout(request)
    return redirect(login)


def about(request):
    return render(request, 'about.html', {})


def add_user(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'adduser.html', {'formset': UserForm()})


def capture(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, 'capture.html')


def display_users(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render_to_response('user.html', {'users': User.objects.all()})


def train(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, 'train.html')


def handler404(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def receive_images(request):
    if not request.is_ajax():
        return redirect(handler404)
    label = request.POST.get('label')
    photos = request.POST.getlist('photos[]')
    for photo in photos:
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        fh = open('static/photos/'+str(label)+'_'+str(photos.index(photo))+'.'+ext, 'wb')
        fh.write(base64.b64decode(img))
        fh.close()
    return HttpResponse()


def receive_train(request):
    if not request.is_ajax():
        return redirect(handler404)
    trainer.train()
    return HttpResponse()

def delete_user(request):
    if not request.is_ajax():
        return redirect(handler404)
    id = request.POST.get('id')
    print(id)
    User.objects.filter(id=id).delete()
    return HttpResponse()
