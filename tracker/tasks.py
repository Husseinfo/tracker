#!/usr/bin/env python3

from tracker.mqtt import Mqtt
from tracker.models import Task, UserTask


def on_message(self, mosq, obj, message):
    print(str(message.payload, 'utf-8'))


def db_sync():
    stored = [x.name for x in Task.objects.all()]
    if tuple(stored) == TASKS: return
    for task in tuple(set(tuple(stored)) ^ set(TASKS)):
        Task.objects.create(name=task)
    pass


def do_user_tasks(user):
    for task in UserTask.objects.filter(user=user):
        mqtt_client.send(topic='room1', message=str(task.task.name) + ',' + str(user))


TASKS = ('Turn Lamp On', )
mqtt_client = Mqtt(ip='192.168.0.2', port=8883, username='pi', password='123456', subscription='', on_message=on_message)
db_sync()
