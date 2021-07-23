# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_is31fl3741

i2c = board.I2C()

is31 =  adafruit_is31fl3741.IS31FL3741(i2c)

is31.set_led_scaling(0xFF) # turn on LEDs all the way
is31.global_current = 0xFE # set current to max
is31.enable = True         # enable!

# light up every LED, one at a time
while True:
    for i in range(351):
        is31[i] = 255
        time.sleep(0.01)
        is31[i] = 0
