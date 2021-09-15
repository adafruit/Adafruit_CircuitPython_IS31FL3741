
import time
import board
import microcontroller
import busio
from adafruit_is31fl3741.adafruit_ledglasses import LED_Glasses
from rainbowio import colorwheel

i2c = busio.I2C(microcontroller.pin.P0_08, microcontroller.pin.P0_06)
glasses = LED_Glasses(i2c)

wheeloffset = 0
while True:
    for i in range(24):
        glasses.right_ring[i] = colorwheel(i/24*255 + wheeloffset)
        glasses.left_ring[23-i] = colorwheel(i/24*255 + wheeloffset)
    wheeloffset += 10
