from os import remove
from os.path import isfile

from django.test import TestCase

from tracker.engine import train, predict
from tracker.models import User


class RecognitionTestCase(TestCase):
    def setUp(self):
        self.photos_train_path = 'tests/recognition/photos/train'
        self.photos_test_path = 'tests/recognition/photos/test'
        self.model_path = 'tests/recognition/model'
        User.objects.create(first_name="Barack", last_name="Obama")
        User.objects.create(first_name="Cristiano", last_name="Ronaldo")

    def test_training(self):
        if isfile(self.model_path):
            remove(self.model_path)
        train(self.model_path, self.photos_train_path)
        self.assertTrue(isfile(self.model_path))

    def test_prediction(self):
        if not isfile(self.model_path):
            train(self.model_path, self.photos_train_path)
            self.assertTrue(isfile(self.model_path))

        predictions = predict((f'{self.photos_test_path}/cr7.jpg',))
        self.assertEqual(User.objects.get(id=predictions[0][0]).first_name, 'Cristiano')

        predictions = predict((f'{self.photos_test_path}/obama.jpg',))
        self.assertEqual(User.objects.get(id=predictions[0][0]).first_name, 'Barack')
