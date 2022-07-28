from _thread import start_new_thread
from base64 import b64decode
from datetime import datetime
from math import ceil
from os import listdir, remove
from time import time

from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

from tracker import photos_path, utility
from .models import UserForm, User, Attendance
from .recognition import predict, get_nbr_photos, train as do_train
from .serializers import AttendanceSerializer


def home(request):
    if not request.user.is_authenticated:
        return redirect(login)
    return render(request, "home.html",
                  {'photos': get_nbr_photos(),
                   'users': User.objects.count(),
                   'last_training': utility.last_training()}, )


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            _login(request, user)
            return redirect(home)
        else:
            return render(request, 'login.html')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(home)
        return render(request, 'login.html')


def logout(request):
    _logout(request)
    return redirect(login)


def about(request):
    if not request.user.is_authenticated:
        return redirect(login)
    return render(request, 'about.html', {})


def add_user(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'adduser.html', {'formset': UserForm()})


def capture(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if User.objects.count() == 0:
        return redirect('/adduser/?status=empty')
    return render(request, 'capture.html', {'users': User.objects.all()})


def display_users(request):
    if not request.user.is_authenticated:
        return redirect(login)
    return render(request, 'user.html', {'users': User.objects.all()})


def train(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not utility.are_there_photos():
        return redirect('/capture/?status=empty')
    return render(request, 'train.html')


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def receive_images(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    label = request.POST.get('label')
    photos = request.POST.getlist('photos[]')
    start_new_thread(utility.save_base64_photos, (label, photos))
    return HttpResponse()


def receive_train(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    start = time()
    do_train()
    duration = ceil(time() - start)
    return JsonResponse({'duration': duration})


def profile(request, _id=1):
    if not request.user.is_authenticated:
        return redirect(login)
    user_data = User.objects.get(pk=_id)
    images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(_id)]
    return render(request, 'profile.html', {'user': user_data, 'images': images})


def delete_user(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    user_id = request.POST.get('id')
    User.objects.filter(id=user_id).delete()
    images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(user_id)]
    for image in images:
        remove('static/photos/' + image)
    return HttpResponse()


def recognize_camera(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    return render(request, 'camera.html')


def receive_recognize(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not request.is_ajax():
        return redirect(handler404)
    photos = request.POST.getlist('photos[]')
    paths = []
    for i, photo in enumerate(photos):
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        name = 'static/temp/rec' + str(i) + '.' + ext
        fh = open(name, 'wb')
        fh.write(b64decode(img))
        fh.close()
        paths.append('static/temp/rec' + str(i) + '.' + ext)
    user_id, percentage = predict(paths)
    name = 'Unknown' if user_id in (-1, None) else User.objects.get(id=user_id).first_name + ' ' + User \
        .objects.get(id=user_id).last_name
    data_rec = {'user': user_id, 'date': datetime.now(), 'inout': None}
    serializer = AttendanceSerializer(data=data_rec)
    if serializer.is_valid() and percentage == 100:
        serializer.save()
    return JsonResponse({'id': user_id, 'name': name, 'percentage': percentage})


def recognize_photo(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    return render(request, 'recognize_photo.html')


def view_photos(request):
    if not request.user.is_authenticated:
        return redirect(login)
    users = User.objects.all()
    data = []
    for user in users:
        images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(user.id)]
        data.append({'user': user.first_name + " " + user.last_name, 'images': images})
    return render(request, 'viewPhoto.html', {'data': data})


def edit_user(request, _id=None):
    if not request.user.is_authenticated:
        return redirect(login)
    instance = User.objects.get(id=_id)
    form = UserForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'user_details.html', {'formset': form})


def attendance(request):
    if not request.user.is_authenticated:
        return redirect(login)
    return render(request, 'attendance.html', {'attendance': Attendance.objects.all()})
