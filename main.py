#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from temp_sensor import TMP117
from multimeter import S7081

short_sensor = TMP117(0x48)
long_sensor = TMP117(0x49)
print(short_sensor.read_temperature())
print(long_sensor.read_temperature())


bench_7081 = S7081(1)