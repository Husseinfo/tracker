#!/usr/local/bin/python3

import cv2
import time
from __init__ import face_cascade as detector


def capture_faces(video_source=0, start=0, stop=100, label=100, path='.'):
    """
    Captures photos, detects faces, saves them in path
    Naming will follow the model: [label]_[number].jpg
    :param video_source: Source of video, usually 0
    :param start: Start number of names
    :param stop: End number of names
    :param label: The first part of the name in the file
    :param path: Where the photos will be saved
    :return: None
    """
    cam = cv2.VideoCapture(video_source)
    for i in range(start, stop):
        time.sleep(0.1)
        img = cam.read()[1]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(path + '/' + str(label) + '_' + str(i) + ".jpg", gray[y:y + h, x:x + w])

    cam.release()
