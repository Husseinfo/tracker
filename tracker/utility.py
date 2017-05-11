#!/usr/bin/env python3

import os
import datetime


def time_spent(sec):
    lm = datetime.datetime.now() - datetime.datetime.fromtimestamp(sec)
    if 
    lm = str(lm.days) + 'd' if lm.days > 0 else str(int(lm.seconds / 3600)) + 'h'

    return lm
