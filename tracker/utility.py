#!/usr/bin/env python3

import datetime
import os
import cv2
import base64
from tracker import lbph_train_file_name
from tracker import trainer
from tracker import photos_path
from tracker.recognition import face_cascade as detector


def time_spent(sec):
    lm = datetime.datetime.now() - datetime.datetime.fromtimestamp(sec)
    if lm.days > 0:
        return str(lm.days) + 'd'
    if int(lm.seconds / 3600) > 0:
        return str(int(lm.seconds / 3600)) + 'h'
    if int(lm.seconds / 60) > 0:
        return str(int(lm.seconds / 60)) + 'm'
    return str(int(lm.seconds)) + 's'


def last_training():
    try:
        return time_spent(os.path.getmtime(lbph_train_file_name))
    except:
        return 'N/A'


def is_model_trained():
    return os.path.isfile(lbph_train_file_name)


def are_there_photos():
    return True if trainer.get_nbr_photos() > 0 else False


def add_new_user_photos(user, path):
    num = len([x for x in os.listdir(photos_path) if x.split('_')[0] == str(user)])
    os.popen('mv {} {}/{}_{}.png'.format(path, photos_path, user, num))
    num += 1


def save_base64_photos(label, photos):
    num = len([x for x in os.listdir(photos_path) if x.split('_')[0] == label])
    paths = []
    for photo in photos:
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        name = 'static/photos/' + str(label) + '_' + str(num) + '.' + ext
        fh = open(name, 'wb')
        num += 1
        fh.write(base64.b64decode(img))
        fh.close()
        paths.append(name)
    crop_photos(paths=paths)


def crop_photos(paths):
    for image in paths:
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.imwrite(image, gray[y:y + h, x:x + w])


def test(paths):
    for image in paths:
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.imwrite(image, gray[y:y + h, x:x + w])
