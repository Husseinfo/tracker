from tracker.recognition.recognizer import Recognizer
from tracker.recognition.trainer import Trainer
from tracker.mqtt import Mqtt

photos_path = 'static/photos'
temp_path = 'static/temp'
train_file_name = 'static/trained'
lbph_train_file_name = 'static/trained_lbph.yml'
video_source = 0


trainer = Trainer(photos_path, train_file_name)
w, h = trainer.get_photo_size()
face_recognizer = Recognizer(train_file_name, video_source, max_width=w, max_height=h)
