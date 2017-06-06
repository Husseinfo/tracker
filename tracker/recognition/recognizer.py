#!/usr/local/bin/python3

import cv2
import numpy as np
from collections import Counter

from tracker.recognition import face_cascade


class Recognizer:
    """
    The recognizer class contains a recognizer object that predicts the label of a given photo
    Several methods are included such as reading an image from disk, from video source, from a URL, searching in social
    media...
    """
    def __init__(self, recognizer_filename, source, threshold=None):
        """
        Initialization of attributes
        :param recognizer_filename: Path of the file containing the exported trained model
        :param source: Video source to read from in case of reading from a camera
        :param threshold: Threshold between recognizing and not recognizing an input photo
        """
        self.recognizer_filename = recognizer_filename
        self.source = source
        self.video_capture = None
        self.lbph_rec = self.eigenface_rec = self.fisherface_rec = None
        self.reload()

    def reload(self):
        for recognizer, name in zip((self.lbph_rec, self.eigenface_rec, self.fisherface_rec), ('lbph', 'eigenface', 'fisherface')):
            try: recognizer.load(self.recognizer_filename+'_'+name+'.yml')
            except: pass

    def open_source(self):
        """
        Opens the source of video
        :return: 
        """
        self.video_capture = cv2.VideoCapture(self.source)

    def read_image(self):
        """
        Read a single image from the source
        :return: A tuple containing the original image and a greyscale version of it
        """
        self.open_source()
        image = np.array(self.video_capture.read()[1])
        return image, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def predict(self, gray):
        res = []
        for recognizer in (self.lbph_rec, self.eigenface_rec, self.fisherface_rec):
            faces = face_cascade.detectMultiScale(gray)
            for x, y, w, h in faces:
                try:
                    res.append(recognizer.predict(gray[y: y + h, x: x + w])[0])
                except: pass
        print(res)
        return Counter(res).most_common(1)[0][0]

    def get_image_label(self, path):
        """
        Gets the label of a saved photo on the disk
        :param path: Path of the photo
        :return: The predicted label of the photo
        """
        image = np.array(cv2.imread(path))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.predict(gray)

    def recognize_from_video(self, num=10):
        """
        A generator the predicts the label of photos read from video source
        :param num: Number of iterations
        :return: The prediction of the photo
        """
        for i in range(num):
            image, gray = self.read_image()
            yield self.predict(gray)

    def get_label(self):
        for i in range(5):
            image, gray = self.read_image()
            yield self.predict(gray)

    def save_and_get_label(self):
        for i in range(5):
            img, gray = self.read_image()
        faces = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite('img.jpg', gray[y:y + h, x:x + w])
        return self.get_image_label('img.jpg')
