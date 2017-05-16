from recognition.trainer import Trainer
from recognition.recognizer import Recognizer

photos_path = 'static/photos'
train_file_name = 'recognition/trained.yml'
video_source = 0


trainer = Trainer(photos_path, train_file_name)
face_recognizer = Recognizer(train_file_name, video_source)
