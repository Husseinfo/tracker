from tracker.recognition.recognizer import Recognizer
from tracker.recognition.trainer import Trainer
from tracker.mqtt import Mqtt

photos_path = 'static/photos'
train_file_name = 'static/trained'
lbph_train_file_name = 'static/trained_lbph.yml'
video_source = 0


trainer = Trainer(photos_path, train_file_name)
face_recognizer = Recognizer(train_file_name, video_source)
