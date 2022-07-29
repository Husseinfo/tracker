# tracker

## ***UPDATE***

- [OpenCV](https://github.com/opencv/opencv) replaced
  with [face_recognition](https://github.com/ageitgey/face_recognition/)
- Upgraded to [Django 4](https://github.com/django/django/releases/tag/4.0.6)


![alt homepage](https://github.com/Husseinfo/tracker/blob/master/static/images/homepage.png?raw=true)

## Overview

A face recognition based attendance system.

## Functionalities

- Login
- Homepage: showing last stats of the system
- Add user: to add new faces
- Capture page: to take faces photos from a local or remote device
- Train page: to train models
- Attendance page: shows attendance records
- A RESTful API interface to send attendance records (from the raspberry pi in the prototype device)

## Environment

Python: > 3.6

Install libraries: ```pip3 install -r requirements.txt```

## Running

Initialize the database from django:

- ```python manage.py migrate```
- ```python manage.py createsuperuser```

Start the server:
```python manage.py runserver```
