from cv2 import CascadeClassifier

"""
    This configuration file contains some common used data
"""

cascade_path = 'static/haarcascade_frontalface_default.xml'
face_cascade = CascadeClassifier(cascade_path)
