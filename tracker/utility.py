#!/usr/bin/env python3

import datetime


def time_spent(sec):
    lm = datetime.datetime.now() - datetime.datetime.fromtimestamp(sec)
    if lm.days > 0:
        return str(lm.days) + 'd'
    if int(lm.seconds / 3600) > 0:
        return str(int(lm.seconds / 3600)) + 'h'
    if int(lm.seconds / 60) > 0:
        return str(int(lm.seconds / 60)) + 'm'
    return str(int(lm.seconds)) + 's'
