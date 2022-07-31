from os import mkdir
from os.path import isdir

temp_path = 'static/temp'
photos_path = 'static/photos'
profile_path = 'static/profile'
model_filename = 'static/model'

for path in (temp_path, profile_path, profile_path):
    if not isdir(path):
        mkdir(path)
