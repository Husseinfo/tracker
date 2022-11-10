from _thread import start_new_thread
from base64 import b64decode
from datetime import datetime
from math import ceil
from os import listdir, remove
from time import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, HttpResponse

from . import photos_path, utility, temp_path
from .forms import UserForm, ImageForm
from .models import Attendance
from .models import User
from .recognition import predict, get_nbr_photos, train as do_train
from .serializers import AttendanceSerializer


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
    return render(request, 'adduser.html', {'formset': UserForm()})


@login_required
def capture(request):
    if User.objects.count() == 0:
        return redirect('/adduser/?status=empty')
    return render(request, 'capture.html', {'users': User.objects.all()})


@login_required
def upload(request):
    if User.objects.count() == 0:
        return redirect('/adduser/?status=empty')
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
    return render(request, 'train.html')


def handler404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required
def receive_images(request):
    label = request.POST.get('label')
    photos = request.POST.getlist('photos[]')
    start_new_thread(utility.save_base64_photos, (label, photos))
    return HttpResponse()


@login_required
def receive_train(request):
    start = time()
    do_train()
    duration = ceil(time() - start)
    return JsonResponse({'duration': duration})


@login_required
def profile(request, _id=1):
    user_data = User.objects.get(pk=_id)
    images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(_id)]
    return render(request, 'profile.html', {'user': user_data, 'images': images})


@login_required
def delete_user(request):
    user_id = request.POST.get('id')
    User.objects.filter(id=user_id).delete()
    images = [filename for filename in listdir(photos_path) if filename.split('_')[0] == str(user_id)]
    for image in images:
        remove('static/photos/' + image)
    return HttpResponse()


@login_required
def recognize_camera(request):
    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    return render(request, 'camera.html')


@login_required
def receive_recognize(request):
    photos = request.POST.getlist('photos[]')
    paths = []
    for i, photo in enumerate(photos):
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        name = f'{temp_path}/rec' + str(i) + '.' + ext
        fh = open(name, 'wb')
        fh.write(b64decode(img))
        fh.close()
        paths.append('static/temp/rec' + str(i) + '.' + ext)

    if predictions := predict(paths):
        user_id, percentage = predictions[0][:2]
        name = 'Unknown' if user_id in (-1, None) else User.objects.get(id=user_id).first_name + ' ' + User \
            .objects.get(id=user_id).last_name
        data_rec = {'user': user_id, 'date': datetime.now(), 'inout': None}
        serializer = AttendanceSerializer(data=data_rec)
        if serializer.is_valid() and percentage >= 85:
            serializer.save()
        return JsonResponse({'id': user_id, 'name': name, 'percentage': percentage})
    return JsonResponse({'id': None})


@login_required
def recognize_photo(request):
    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    return render(request, 'recognize_photo.html')


@login_required
def edit_user(request, _id=None):
    instance = User.objects.get(id=_id)
    form = UserForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        return redirect(home)
    return render(request, 'user_details.html', {'formset': form})


@login_required
def attendance(request):
    return render(request, 'attendance.html', {'attendance': Attendance.objects.all()})
