# tracker

## Overview

The aim of the project is to provide a face recognition based attendence system.
The first part of the project is a Python module used as a library to provide face recognition functionality; managing system users and their photos, training the model and making predictions.
The second part is a Web interface to provide the configuration and administration of the system.

## The recognition module
The ```__init__.py``` of the module contains the face_cascade object. This is a common ressource to be used in order to detect the face from the picture.

The ```trainer.py``` contains the Trainer class which is the responsible of reading the photos to train them in a model.
The system uses the three available algorithms in OpenCV (```LBPH, FisherFace``` and ```EigenFace```) and store three trained models in three files.

The ```recognizer.py``` contains the Recognizer which use the trained models to make predictions.

The ```capture.py``` contains a function to capture photos of a certain user and store them in the proper way.


## The django web interface
- The web interface consists of the following functionalities:
- Login and Homepage showing last stats of the system
- Add user page to add new system users
- Capture page to capture users' photos from a local or remote device
- Train page to train the models
- Attendence page to view the attendence records
- A RESTful API interface to send attendence records (from the raspberry pi in the prototype device)

## Screenshot
![alt homepage](https://github.com/Husseinfo/tracker/blob/master/static/images/homepage.png?raw=true)

## Note
This project is a part of a complete enterprise automation system that includes IoT, NLP, and AI functionalities ending up with an intelligent automation system.

## Requirements
You need Python3.6 to be installed on your system with some additional libraries indicated in ```requirements.txt```.

You can install them with pip3 tool using the following command: ```pip install -r requirements.txt```

You also need to create an empty postgresql database for django (or use a different DBMS).

## Running
To run the project you need first to initialize the database from django:
- ```python3 manage.py makemigrations```
- ```python3 manage.py migrate```
- ```python3 manage.py createsuperuser```

Then start the server with:
```python3 manage.py runserver```
