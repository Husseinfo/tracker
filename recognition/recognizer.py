#!/usr/local/bin/python3

import cv2
import numpy as np
import urllib.request
import webbrowser
from recognition import face_cascade
from recognition import users
from recognition import twitter
from recognition import facebook


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
        self.recognizer = cv2.face.createLBPHFaceRecognizer()
        self.recognizer.load(recognizer_filename)
        if threshold is not None: self.recognizer.setThreshold(threshold)

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

    def get_image_label(self, path):
        """
        Gets the label of a saved photo on the disk
        :param path: Path of the photo
        :return: The predicted label of the photo
        """
        image = np.array(cv2.imread(path))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        for x, y, w, h in faces:
            return self.recognizer.predict(gray[y: y + h, x: x + w])[0]
        return None

    def get_image_name(self, path):
        """
        Get the name of the corresponding user of the predicted label of photo
        :param path: Path to the photo
        :return: The name of the predicted owner of the photo
        """
        label = self.get_image_label(path)
        if label is not None:
            return users[label]
        return None

    def recognize(self, num=10):
        """
        A generator the predicts the label of photos read from video source
        :param num: Number of iterations
        :return: The prediction of the photo
        """
        for i in range(num):
            image, gray = self.read_image()
            faces = face_cascade.detectMultiScale(gray)
            for x, y, w, h in faces:
                yield self.recognizer.predict(gray[y: y + h, x: x + w])

    def recognize_name(self):
        """
        Opens the video source and starts taking photos, predict the name of the owner
        :return: The name of predicted user
        """
        for i in range(5):
            image, gray = self.read_image()
            cv2.imshow('Recognizing', image)
            cv2.waitKey(10)
        faces = face_cascade.detectMultiScale(gray)
        for x, y, w, h in faces:
            face = self.recognizer.predict(gray[y: y + h, x: x + w])[0]
            if face == -1: return None
            name = users[face]
            if name is None: pass
            else:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(image, str(name), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow(name, image)
                cv2.waitKey(10)
                return name
        return None

    def recognize_and_show(self):
        """
        Real time recognition of faces taken from video source
        :return: None
        """
        while True:
            image, gray = self.read_image()
            faces = face_cascade.detectMultiScale(gray)
            for x, y, w, h in faces:
                label, conf = self.recognizer.predict(gray[y: y + h, x: x + w])
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(image, str(label), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Prediction', image)
            cv2.waitKey(10)

    def is_valid_user(self, user, username, url, platform='tw'):
        """
        Reads the image of the username, open the account if the label matches the user
        :param user: The name of the user to be searched on social media
        :param username: The username of the owner of the photo
        :param url: The url of the photo
        :param platform: Twitter or Facebook
        :return: True if the photo, and therefore the username belongs to the user, False if not
        """
        try:
            response = urllib.request.urlopen(url)
            resp = response.read()
        except: return False
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if image is None: return False
        faces = face_cascade.detectMultiScale(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            label, conf = self.recognizer.predict(gray[y: y + h, x: x + w])
            cv2.putText(image, users[label], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow(username, image)
            cv2.waitKey(1000)
            if users[label] == user:
                if platform == 'tw':
                    webbrowser.open_new('https://www.twitter.com/' + username)
                else:
                    webbrowser.open_new('https://www.facebook.com/' + username)
                return True
            cv2.destroyWindow(username)
        return False

    def real_time_recognition(self, platform='tw'):
        """
        Real time recognition and searching on social media
        :param platform: Twitter or Facebook
        :return: None
        """
        occurrences = {}
        if platform == 'fb':
            get_user_account = facebook.get_user_account
        elif platform == 'tw':
            get_user_account = twitter.get_user_account
        while True:
            image, gray = self.read_image()
            faces = face_cascade.detectMultiScale(gray)
            for x, y, w, h in faces:
                face = self.recognizer.predict(gray[y: y + h, x: x + w])[0]
                name = users[face]
                if face == -1 or face == 1: continue
                if occurrences.__contains__(face):
                    occurrences[face] += 1
                else: occurrences[face] = 0
                if occurrences[face] == 3: get_user_account(self, name)
                if name is None: pass
                else:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(image, str(name), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Recognizing', image)
            cv2.waitKey(10)
