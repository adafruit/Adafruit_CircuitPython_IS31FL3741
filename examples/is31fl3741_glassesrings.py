# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from rainbowio import colorwheel
from adafruit_is31fl3741.adafruit_ledglasses import LED_Glasses

glasses = LED_Glasses(board.I2C())

wheeloffset = 0
while True:
    for i in range(24):
        glasses.right_ring[i] = colorwheel(i / 24 * 255 + wheeloffset)
        glasses.left_ring[23 - i] = colorwheel(i / 24 * 255 + wheeloffset)
    wheeloffset += 10
