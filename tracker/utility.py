#!/usr/bin/env python3

import datetime


def time_spent(sec):
    lm = datetime.datetime.now() - datetime.datetime.fromtimestamp(sec)
    if lm.days > 0:
        return str(lm.days) + 'd'
    if lm.seconds / 3600 > 0:
        return str(int(lm.seconds / 3600)) + 'h'
    return str(int(lm.seconds / 60)) + 'm'
