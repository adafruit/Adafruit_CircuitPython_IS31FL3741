# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3741.adafruit_rgbmatrixqt`
====================================================

CircuitPython driver for the Adafruit IS31FL3741 RGB Matrix QT board


* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3741

class Right_Ring(IS31FL3741):
    """The right eye ring of the LED glasses"""
    def __init__(self, is31_controller):
        self._is31 = is31_controller
        
    def __setitem__(self, led, color):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")

        ledmap = ((287, 31, 30), # 0
                  (278, 1, 0), # 1
                  (273, 274, 275), # 2
                  (282, 283, 284), # 3
                  (270, 271, 272), # 4
                  (27, 28, 29), # 5
                  (23, 24, 25), # 6
                  (276, 277, 22), # 7
                  (20, 21, 26), # 8
                  (50, 51, 56), # 9
                  (80, 81, 86), # 10
                  (110, 111, 116), #11
                  (140, 141, 146), #12
                  (170, 171, 176), #13
                  (200, 201, 206), #14
                  (230, 231, 236), #15
                  (260, 261, 266), #16
                  (348, 349, 262), #17
                  (233, 234, 235), #18
                  (237, 238, 239), #19
                  (339, 340, 232), #20
                  (327, 328, 329), #21
                  (305, 91, 90), #22
                  (296, 61, 60), # 23
                  )
        rgb = ledmap[led]
        self._is31[rgb[0]] = (color >> 16) & 0xFF
        self._is31[rgb[1]] = (color >> 8) & 0xFF
        self._is31[rgb[2]] = color & 0xFF
        
class Left_Ring:
    """The left eye ring of the LED glasses"""
    def __init__(self, is31_controller):
        self._is31 = is31_controller
        
    def __setitem__(self, led, color):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")

        ledmap = (
            (341, 211, 210), #0
            (332, 181, 180), #1
            (323, 151, 150), #2
            (127, 126, 125), #3
            (154, 153, 152), #4
            (163, 162, 161), #5
            (166, 165, 164), #6
            (244, 243, 242), #7
            (259, 258, 257), #8
            (169, 168, 167), #9
            (139, 138, 137), #10
            (109, 108, 107), #11
            (79, 78, 77), #12
            (49, 48, 47), #13
            (199, 198, 197), #14
            (229, 228, 227), #15
            (19, 18, 17), #16
            (4, 3, 2), #17
            (16, 15, 14), #18
            (13, 12, 11), #19
            (10, 9, 8), #20
            (217, 216, 215), #21
            (7, 6, 5), #22
            (350, 241, 240), #23
            )
        rgb = ledmap[led]
        self._is31[rgb[0]] = (color >> 16) & 0xFF
        self._is31[rgb[1]] = (color >> 8) & 0xFF
        self._is31[rgb[2]] = color & 0xFF




class LED_Glasses(IS31FL3741):
    def __init__(self, i2c):
        super().__init__(i2c)
        self.set_led_scaling(0xFF)  # turn on LEDs all the way
        self.global_current = 0xFE  # set current to max
        self.enable = True  # enable!
        
        self.right_ring = Right_Ring(self)
        self.left_ring = Left_Ring(self)
