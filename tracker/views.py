#!/usr/bin/env python3

from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.http import JsonResponse

from tracker.models import UserForm, User
from tracker import trainer, face_recognizer, train_file_name, photos_path, utility
import base64
import os


def home(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, "home.html",
                  {'photos': trainer.get_nbr_photos(),
                   'users': User.objects.count(),
                   'last_training': utility.last_training()}, )


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
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
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, 'about.html', {})


def add_user(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'adduser.html', {'formset': UserForm()})


def capture(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, 'capture.html', {'users': User.objects.all()})


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
    if not request.user.is_authenticated():
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    label = request.POST.get('label')
    photos = request.POST.getlist('photos[]')
    num = len([x for x in os.listdir(photos_path) if x.split('_')[0] == label])
    for photo in photos:
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        fh = open('static/photos/' + str(label) + '_' + str(num) + '.' + ext, 'wb')
        num += 1
        fh.write(base64.b64decode(img))
        fh.close()
    return HttpResponse()


def receive_train(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    trainer.train()
    face_recognizer.reload()
    return HttpResponse()


def profile(request, id=1):
    if not request.user.is_authenticated():
        return redirect(login)
    user_data = User.objects.get(pk=id)
    images = [filename for filename in os.listdir(photos_path) if filename.startswith(str(id))]
    return render(request, 'profile.html', {'user': user_data, 'images': images})


def delete_user(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    user_id = request.POST.get('id')
    User.objects.filter(id=user_id).delete()
    return HttpResponse()


def recognize_camera(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not utility.is_model_trained():
        return redirect(train)
    return render(request, 'camera.html')


def receive_recognize(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    photo = request.POST.get('photo')
    ext, img = photo.split(';base64,')
    ext = ext.split('/')[-1]
    fh = open('static/temp/rec.' + ext, 'wb')
    fh.write(base64.b64decode(img))
    fh.close()
    user_id = face_recognizer.get_image_label('static/temp/rec.' + ext)
    name = 'Unknown' if user_id == -1 or user_id is None else User.objects.get(id=user_id).first_name + ' ' + User\
        .objects.get(id=user_id).last_name
    return JsonResponse({'id': user_id, 'name': name})


def recognize_photo(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not utility.is_model_trained():
        return redirect(train)
    return render(request, 'recognise_photo.html')


def view_photos(request):
    if not request.user.is_authenticated():
        return redirect(login)
    users = User.objects.all()
    data = []
    for user in users:
        images = [filename for filename in os.listdir(photos_path) if filename.startswith(str(user.id))]
        data.append({'user': user.first_name + " " + user.last_name, 'images': images})
    return render(request, 'viewPhoto.html', {'data': data})


def edit_user(request,id=None):
    if not request.user.is_authenticated():
        return redirect(login)
    instance = User.objects.get(id=id)
    form = UserForm(request.POST or None, request.FILES or None,instance=instance)
    if request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'user_details.html', {'formset': form})

