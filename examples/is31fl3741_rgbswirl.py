"""CircuitPython Essentials I2C Scan example"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import board
import adafruit_is31fl3741
from rainbowio import colorwheel

#from adafruit_is31fl3741.issi_evb import ISSI_EVB
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT

i2c = board.I2C()

is31 = Adafruit_RGBMatrixQT(i2c)
is31.set_led_scaling(0xFF)
is31.global_current = 0xFF
#print("global current is", is31.global_current)
is31.enable = True
#print("Enabled?", is31.enable)

wheeloffset = 0
while True:

    for y in range (9):
        for x in range (13):
            is31.pixel(x, y, colorwheel((y*13 + x)*2 + wheeloffset))
    wheeloffset += 1
