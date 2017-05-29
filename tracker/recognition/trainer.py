#!/usr/local/bin/python3

import os

import cv2
import numpy as np

from tracker.recognition import face_cascade


class Trainer:
    """
    The trainer class is the responsible of reading datasets, training them, and exporting the trained model
    """

    def __init__(self, photos, export):
        """
        Initialization of attributes
        :param photos: The directory containing photos to be trained on
        :param export: The path where the trained model will be saved
        """
        self.photos = photos
        self.export = export

    def get_nbr_photos(self):
        return len(os.listdir(self.photos))

    def get_images_and_labels(self):
        """
        Reads each photo from photos directory, extract its label from its name, train it 
        :return: A tuple containing the list of images and the list of corresponding labels
        """
        # append all the absolute image paths in a list image_paths
        # we will not read the image with .sad extension in the training set
        # rather, we will use them to test our accuracy the training
        image_paths = [os.path.join(self.photos, f) for f in os.listdir(self.photos)]
        image_paths += [os.path.join('static/negatives', f) for f in os.listdir('static/negatives')]
        # images will contain face images
        images = []
        # labels will contains the label that is assigned to the image
        labels = []

        for image_path in image_paths:
            # read the image and convert to greyscale
            image_pil = cv2.imread(image_path, 0)

            # convert the image format into numpy array
            image = np.array(image_pil, 'uint8')

            # get the label of the image
            nbr = int(os.path.split(image_path)[1].split("_")[0])

            # detect the face in the image
            faces = face_cascade.detectMultiScale(image)

            # if face is detected, append the face to images and the label to labels
            for x, y, w, h in faces:
                images.append(image)
                labels.append(nbr)

        # return the images list and labels list
        return images, labels

    def train(self):
        """
        Trains a model from dataset, saves the file to export path
        This process may take several minutes, make sure you have an SSD!
        :return: 
        """
        # create the face recognizer object
        recognizer = cv2.face.createLBPHFaceRecognizer()

        # call get_images_and_labels
        images, labels = self.get_images_and_labels()

        # perform the training
        recognizer.train(images, np.array(labels))
        recognizer.save(self.export)
