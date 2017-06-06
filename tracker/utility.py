#!/usr/bin/env python3

import datetime
import os
from tracker import lbph_train_file_name
from tracker import trainer


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
