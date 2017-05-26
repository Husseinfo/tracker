#!/usr/bin/env python3

import datetime
import os
from tracker import train_file_name


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
        return time_spent(os.path.getmtime(train_file_name))
    except:
        return 'N/A'


def is_model_trained():
    return os.path.isfile(train_file_name)
