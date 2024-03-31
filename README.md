# tracker

A face recognition based attendance system.

![Django CI](https://github.com/Husseinfo/tracker/actions/workflows/django.yml/badge.svg)
[![GitHub license](https://img.shields.io/github/license/husseinfo/tracker.svg)](https://github.com/husseinfo/tracker/blob/main/LICENSE)
[![views-counter](https://github.com/Husseinfo/views-counter/blob/master/svg/90946301/badge.svg)](https://github.com/Husseinfo/views-counter/blob/master/readme/90946301/year.md)
[![GitHub stars](https://img.shields.io/github/stars/husseinfo/tracker.svg)](https://github.com/husseinfo/tracker/stargazers)

## ***UPDATE***

- [OpenCV](https://github.com/opencv/opencv) replaced
  with [face_recognition](https://github.com/ageitgey/face_recognition/)
- Upgraded to [Django 4](https://github.com/django/django/releases/tag/4.0.6)
- UI with [django-bootstrap5](https://github.com/zostera/django-bootstrap5)

![homepage](https://github.com/Husseinfo/tracker/blob/main/static/images/homepage.png?raw=true)

## Running

Python 3.11

Install libraries: ```pip3 install -r requirements.txt```

Initialize the database:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run development server:
```python manage.py runserver```
