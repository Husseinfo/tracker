from tracker.recognition.recognizer import Recognizer
from tracker.recognition.trainer import Trainer


photos_path = 'static/photos'
train_file_name = 'static/trained.yml'
video_source = 0


trainer = Trainer(photos_path, train_file_name)
face_recognizer = Recognizer(train_file_name, video_source)
