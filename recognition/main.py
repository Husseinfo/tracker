#!/usr/local/bin/python3

import capture
from trainer import Trainer
from recognizer import Recognizer
import twitter
import facebook

"""
    A main script to test the program, uncomment the wanted section to test
"""

video_source = 0
path = 'photos'
train_file_name = 'trained.yml'


def main():

    ### Capturing some photos and saving them in ./photos
    # capture.capture_faces(video_source=video_source, start=300, stop=320, label=500, path=path)
    ###

    ### Training a model from photos containing in ./photos
    # trainer = Trainer(path, train_file_name)
    # trainer.train()
    ###

    ### Start real time recognition and searching Twitter
    face_recognizer = Recognizer(train_file_name, video_source, threshold=50)
    # name = recognizer.recognize_name()
    # print(name)
    # print(twitter.get_user_account(recognizer, name))
    face_recognizer.real_time_recognition(platform='fb')
    # facebook.get_user_account(face_recognizer, name)
    ###

if __name__ == '__main__': main()
