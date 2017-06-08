#!/usr/bin/env python3

from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.http import JsonResponse

from tracker.serializers import AttendanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from tracker.models import UserForm, User, Attendance, UserTask, Task
from tracker import trainer, face_recognizer, photos_path, utility
from tracker import tasks

from math import ceil
import base64
import os
import time


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
    if User.objects.count() == 0:
        return redirect('/adduser/?status=empty')
    return render(request, 'capture.html', {'users': User.objects.all()})


def display_users(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, 'user.html', {'users': User.objects.all()})


def train(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not utility.are_there_photos():
        return redirect('/capture/?status=empty')
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
    start = time.time()
    trainer.train()
    face_recognizer.reload()
    duration = ceil(time.time() - start)
    return JsonResponse({'duration': duration})


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
        return redirect('/train/?status=untrained')
    return render(request, 'camera.html')


def receive_recognize(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    photos = request.POST.getlist('photos[]')
    paths=[]
    for i, photo in enumerate(photos):
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        fh = open('static/temp/rec'+str(i)+'.' + ext, 'wb')
        fh.write(base64.b64decode(img))
        fh.close()
        paths.append('static/temp/rec'+str(i)+'.' + ext)
    user_id = face_recognizer.get_image_label(*paths)
    name = 'Unknown' if user_id in (-1, None) else User.objects.get(id=user_id).first_name + ' ' + User\
        .objects.get(id=user_id).last_name
    return JsonResponse({'id': user_id, 'name': name})


def recognize_photo(request):
    if not request.user.is_authenticated():
        return redirect(login)
    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
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


def edit_user(request, id=None):
    if not request.user.is_authenticated():
        return redirect(login)
    instance = User.objects.get(id=id)
    form = UserForm(request.POST or None, request.FILES or None,instance=instance)
    if request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'user_details.html', {'formset': form})


class AttendanceRecord(APIView):
    def post(self, request, format=None):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Run assigned tasks
            tasks.do_user_tasks(serializer.data['user'], serializer.data['inout'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def task(request, id=-1):
    user_task = UserTask.objects.filter(user__id=id)
    user_data = User.objects.get(pk=id)
    tasks = []
    for t in Task.objects.all():
        if t not in [tsk.task for tsk in user_task]: tasks.append(t.name)
    return render(request, 'tasks.html', {'tasks': tasks, 'user_tasks': user_task, 'user_data': user_data})


def save_tasks(request):
    id = request.POST.get('id')
    tasks = request.POST.getlist('tasks[]')
    UserTask.objects.filter(user_id=id).delete()
    id_user = User.objects.get(id=id)
    for t in tasks:
        tak = t[0:len(t) - 1]
        db_task = Task.objects.get(name=tak)
        UserTask.objects.create(user=id_user, task=db_task)
    return HttpResponse()


def attendance(request):
    if not request.user.is_authenticated():
        return redirect(login)
    return render(request, 'attendance.html', {'attendance': Attendance.objects.all()})
