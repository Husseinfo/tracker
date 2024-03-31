# tracker

A face recognition based attendance system.

![Django CI](https://github.com/Husseinfo/tracker/actions/workflows/django.yml/badge.svg)
[![GitHub license](https://img.shields.io/github/license/husseinfo/tracker.svg)](https://github.com/husseinfo/tracker/blob/main/LICENSE)
[![views-counter](https://github.com/Husseinfo/views-counter/blob/master/svg/90946301/badge.svg)](https://github.com/Husseinfo/views-counter/blob/master/readme/90946301/year.md)
[![GitHub stars](https://img.shields.io/github/stars/husseinfo/tracker.svg)](https://github.com/husseinfo/tracker/stargazers)

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
