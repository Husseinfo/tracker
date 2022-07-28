from base64 import b64decode
from datetime import datetime
from os import listdir
from os.path import isfile, getmtime

from . import model_filename, photos_path
from .recognition import get_nbr_photos


def time_spent(sec):
    lm = datetime.now() - datetime.fromtimestamp(sec)
    if lm.days > 0:
        return str(lm.days) + 'd'
    if int(lm.seconds / 3600) > 0:
        return str(int(lm.seconds / 3600)) + 'h'
    if int(lm.seconds / 60) > 0:
        return str(int(lm.seconds / 60)) + 'm'
    return str(int(lm.seconds)) + 's'


def last_training():
    try:
        return time_spent(getmtime(model_filename))
    except Exception as e:
        print(e)
        return 'N/A'


def is_model_trained():
    return isfile(model_filename)


def are_there_photos():
    return True if get_nbr_photos() > 0 else False


def save_base64_photos(label, photos):
    num = len([x for x in listdir(photos_path) if x.split('_')[0] == label])
    paths = []
    for photo in photos:
        ext, img = photo.split(';base64,')
        ext = ext.split('/')[-1]
        name = 'static/photos/' + str(label) + '_' + str(num) + '.' + ext
        fh = open(name, 'wb')
        num += 1
        fh.write(b64decode(img))
        fh.close()
        paths.append(name)
