#!/usr/bin/env python3

import datetime
import os
from tracker import lbph_train_file_name
from tracker import trainer
from tracker import photos_path, temp_path


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


def add_new_user_photos(user, paths):
    num = len([x for x in os.listdir(photos_path) if x.split('_')[0] == str(user)])
    for image in paths:
        os.popen('mv {} {}/{}_{}.png'.format(image, photos_path, user, num))
        num += 1
