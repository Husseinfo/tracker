from base64 import b64decode
from datetime import datetime
from math import ceil
from os import listdir, remove
from time import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from tracker import photos_path, utility, temp_path
from tracker.forms import UserForm, ImageForm
from tracker.models import Attendance, User, Image
from tracker.recognition import predict, get_nbr_photos, train as do_train


@login_required
def home(request):
    return render(request, "home.html",
                  {'photos': get_nbr_photos(),
                   'users': User.objects.count(),
                   'last_training': utility.last_training()}, )


@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'userdetails.html', {'formset': UserForm()})


@login_required
def capture(request):
    if User.objects.count() == 0:
        return redirect('/adduser/?status=empty')
    if request.method == 'POST':
        if frame := request.POST.get('frame'):
            user_id = request.POST.get('user_id')
            ext, img = frame.split(';base64,')
            ext = ext.split('/')[-1]
            filename = f'static/photos/{user_id}_{img[:10]}.{ext}'
            with open(filename, 'wb') as fh:
                fh.write(b64decode(img))
            image = Image(user_id=user_id)
            image.save()
            return redirect('profile', user_id)
    return render(request, 'capture.html', {'users': User.objects.all()})


@login_required
def upload(request):
    if not User.objects.count():
        return redirect('adduser')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'upload.html', {'formset': ImageForm()})


@login_required
def display_users(request):
    return render(request, 'user.html', {'users': User.objects.all()})


@login_required
def train(request):
    if not utility.are_there_photos():
        return redirect('/capture/?status=empty')
    if request.method == 'GET':
        return render(request, 'train.html')
    start = time()
    do_train()
    duration = ceil(time() - start)
    return render(request, 'train.html', {'duration': duration})


@login_required
def receive_images(request):
    label = request.POST.get('label')
    photos = request.POST.getlist('photos[]')
    utility.save_base64_photos(label, photos)
    return HttpResponse()


@login_required
def profile(request, user_id):
    user_data = User.objects.get(pk=user_id)
    images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(user_id)]
    return render(request, 'profile.html', {'user': user_data, 'images': images})


@login_required
def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(user_id)]
    for image in images:
        remove('static/photos/' + image)
    return redirect('users')


@login_required
def recognize(request):
    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    if request.method == 'POST':
        paths = []
        if frame := request.POST.get('frame'):
            ext, img = frame.split(';base64,')
            ext = ext.split('/')[-1]
            name = f'{temp_path}/rec_frame.{ext}'
            with open(name, 'wb') as fh:
                fh.write(b64decode(img))
            paths.append(name)
        if images := request.FILES.getlist('images'):
            for i, image in enumerate(images):
                name = f'{temp_path}/rec{i}.jpg'
                with open(name, 'wb') as fh:
                    fh.write(image.file.read())
                paths.append(name)
        if paths:
            if predictions := predict(paths):
                user_id, confidence = predictions[0][:2]
                user = User.objects.get(id=user_id)
                name = 'Unknown' if user_id in (-1, None) else user.first_name + ' ' + user.last_name
                last_attendance = user.attendance_set.last()
                if confidence >= 85:
                    Attendance.objects.create(user=user, date=datetime.now(), inout=not last_attendance.inout)
                return render(request, 'recognize.html', {'id': user_id, 'name': name, 'confidence': confidence})
            return render(request, 'recognize.html', {'confidence': -1})
    return render(request, 'recognize.html')


@login_required
def edit_user(request, user_id):
    instance = User.objects.get(id=user_id)
    form = UserForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'userdetails.html', {'formset': form})


@login_required
def attendance(request):
    return render(request, 'attendance.html', {'attendance': Attendance.objects.all()})
