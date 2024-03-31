from base64 import b64decode
from datetime import datetime
from os import listdir
from os.path import isfile, getmtime

from tracker import model_filename, photos_path
from tracker.recognition import get_nbr_photos


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
        return datetime.fromtimestamp(getmtime(model_filename))
    except FileNotFoundError:
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
        with open(name, 'wb') as fh:
            fh.write(b64decode(img))
        num += 1
        paths.append(name)
