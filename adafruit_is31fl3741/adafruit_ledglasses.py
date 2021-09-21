# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries, Rose Hooper
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3741.adafruit_rgbmatrixqt`
====================================================

CircuitPython driver for the Adafruit IS31FL3741 RGB Matrix QT board


* Author(s): ladyada, Rose Hooper

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""
import adafruit_is31fl3741
from . import IS31FL3741


class Right_Ring:
    """The right eye ring of the LED glasses"""

    ledmap = (
        (287, 31, 30),  # 0
        (278, 1, 0),  # 1
        (273, 274, 275),  # 2
        (282, 283, 284),  # 3
        (270, 271, 272),  # 4
        (27, 28, 29),  # 5
        (23, 24, 25),  # 6
        (276, 277, 22),  # 7
        (20, 21, 26),  # 8
        (50, 51, 56),  # 9
        (80, 81, 86),  # 10
        (110, 111, 116),  # 11
        (140, 141, 146),  # 12
        (170, 171, 176),  # 13
        (200, 201, 206),  # 14
        (230, 231, 236),  # 15
        (260, 261, 266),  # 16
        (348, 349, 262),  # 17
        (233, 234, 235),  # 18
        (237, 238, 239),  # 19
        (339, 340, 232),  # 20
        (327, 328, 329),  # 21
        (305, 91, 90),  # 22
        (296, 61, 60),  # 23
    )

    def __init__(self, is31_controller):
        self._is31 = is31_controller

    def __setitem__(self, led, color):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")

        rgb = Right_Ring.ledmap[led]
        self._is31[rgb[0]] = (color >> 16) & 0xFF
        self._is31[rgb[1]] = (color >> 8) & 0xFF
        self._is31[rgb[2]] = color & 0xFF

    def __getitem__(self, led):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")
        rgb = Right_Ring.ledmap[led]
        return (
            (self._is31[rgb[0]] << 16) | (self._is31[rgb[1]] << 8) | self._is31[rgb[2]]
        )


class Left_Ring:
    """The left eye ring of the LED glasses"""

    ledmap = (
        (341, 211, 210),  # 0
        (332, 181, 180),  # 1
        (323, 151, 150),  # 2
        (127, 126, 125),  # 3
        (154, 153, 152),  # 4
        (163, 162, 161),  # 5
        (166, 165, 164),  # 6
        (244, 243, 242),  # 7
        (259, 258, 257),  # 8
        (169, 168, 167),  # 9
        (139, 138, 137),  # 10
        (109, 108, 107),  # 11
        (79, 78, 77),  # 12
        (49, 48, 47),  # 13
        (199, 198, 197),  # 14
        (229, 228, 227),  # 15
        (19, 18, 17),  # 16
        (4, 3, 2),  # 17
        (16, 15, 14),  # 18
        (13, 12, 11),  # 19
        (10, 9, 8),  # 20
        (217, 216, 215),  # 21
        (7, 6, 5),  # 22
        (350, 241, 240),  # 23
    )

    def __init__(self, is31_controller):
        self._is31 = is31_controller

    def __setitem__(self, led, color):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")

        rgb = Left_Ring.ledmap[led]
        self._is31[rgb[0]] = (color >> 16) & 0xFF
        self._is31[rgb[1]] = (color >> 8) & 0xFF
        self._is31[rgb[2]] = color & 0xFF

    def __getitem__(self, led):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")
        rgb = Left_Ring.ledmap[led]
        return (
            (self._is31[rgb[0]] << 16) | (self._is31[rgb[1]] << 8) | self._is31[rgb[2]]
        )


class LED_Glasses(IS31FL3741):
    """Class representing LED Glasses"""

    ledmap = [
        (None, None, None),
        (216, 215, 217),
        (186, 185, 187),
        (36, 35, 37),
        (66, 65, 67),
        (96, 95, 97),
        (126, 125, 127),
        (156, 155, 157),
        (246, 245, 247),
        (346, 347, 345),
        (337, 338, 336),
        (328, 329, 327),
        (319, 320, 318),
        (310, 311, 309),
        (301, 302, 300),
        (292, 293, 291),
        (283, 284, 282),
        (None, None, None),
        (9, 8, 10),
        (219, 218, 220),
        (189, 188, 190),
        (39, 38, 40),
        (69, 68, 70),
        (99, 98, 100),
        (129, 128, 130),
        (159, 158, 160),
        (249, 248, 250),
        (343, 344, 342),
        (334, 335, 333),
        (325, 326, 324),
        (316, 317, 315),
        (307, 308, 306),
        (298, 299, 297),
        (289, 290, 288),
        (280, 281, 279),
        (271, 272, 270),
        (12, 11, 13),
        (222, 221, 223),
        (192, 191, 193),
        (42, 41, 43),
        (72, 71, 73),
        (102, 101, 103),
        (132, 131, 133),
        (162, 161, 163),
        (252, 251, 253),
        (268, 269, 267),
        (238, 239, 237),
        (208, 209, 207),
        (178, 179, 177),
        (148, 149, 147),
        (118, 119, 117),
        (88, 89, 87),
        (58, 59, 57),
        (28, 29, 27),
        (15, 14, 16),
        (225, 224, 226),
        (195, 194, 196),
        (45, 44, 46),
        (75, 74, 76),
        (105, 104, 106),
        (135, 134, 136),
        (165, 164, 166),
        (255, 254, 256),
        (264, 265, 263),
        (234, 235, 233),
        (204, 205, 203),
        (174, 175, 173),
        (144, 145, 143),
        (114, 115, 113),
        (84, 85, 83),
        (54, 55, 53),
        (24, 25, 23),
        (3, 2, 4),
        (213, 212, 214),
        (183, 182, 184),
        (33, 32, 34),
        (63, 62, 64),
        (93, 92, 94),
        (123, 122, 124),
        (243, 242, 244),
        (None, None, None),
        (None, None, None),
        (349, 262, 348),
        (331, 202, 330),
        (322, 172, 321),
        (313, 142, 312),
        (304, 112, 303),
        (295, 82, 294),
        (286, 52, 285),
        (277, 22, 276),
    ]
    width = 18
    height = 5
    # These pixels aren't connected to anything and are safe to use for pixels that aren't visible
    unused_pixels = (120, 121, 314)

    def __init__(self, i2c, allocate=adafruit_is31fl3741.NO_BUFFER):
        super().__init__(i2c, allocate=allocate)

        self.set_led_scaling(0xFF)  # turn on LEDs all the way
        self.global_current = 0xFE  # set current to max
        self.enable = True  # enable!

        self.right_ring = Right_Ring(self)
        self.left_ring = Left_Ring(self)
        self.grid = self

    @staticmethod
    def pixel_addrs(x, y):
        addrs = LED_Glasses.ledmap[x + (LED_Glasses.width * y)]
        if addrs[0] is None:
            return LED_Glasses.unused_pixels
        return addrs
