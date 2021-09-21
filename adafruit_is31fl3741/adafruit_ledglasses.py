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
from struct import unpack_from
import adafruit_is31fl3741
from . import IS31FL3741


class Right_Ring:
    """The right eye ring of the LED glasses"""

    # ledmap = ( # These are BRG order; reordered to RGB in bytes below
    #    (287, 31, 30),  # 0
    #    (278, 1, 0),  # 1
    #    (273, 274, 275),  # 2
    #    (282, 283, 284),  # 3
    #    (270, 271, 272),  # 4
    #    (27, 28, 29),  # 5
    #    (23, 24, 25),  # 6
    #    (276, 277, 22),  # 7
    #    (20, 21, 26),  # 8
    #    (50, 51, 56),  # 9
    #    (80, 81, 86),  # 10
    #    (110, 111, 116),  # 11
    #    (140, 141, 146),  # 12
    #    (170, 171, 176),  # 13
    #    (200, 201, 206),  # 14
    #    (230, 231, 236),  # 15
    #    (260, 261, 266),  # 16
    #    (348, 349, 262),  # 17
    #    (233, 234, 235),  # 18
    #    (237, 238, 239),  # 19
    #    (339, 340, 232),  # 20
    #    (327, 328, 329),  # 21
    #    (305, 91, 90),  # 22
    #    (296, 61, 60),  # 23
    # )
    ledmap_bytes = (
        b"\x00\x1F\x00\x1E\x01\x1F"
        b"\x00\x01\x00\x00\x01\x16"
        b"\x01\x12\x01\x13\x01\x11"
        b"\x01\x1B\x01\x1C\x01\x1A"
        b"\x01\x0F\x01\x10\x01\x0E"
        b"\x00\x1C\x00\x1D\x00\x1B"
        b"\x00\x18\x00\x19\x00\x17"
        b"\x01\x15\x00\x16\x01\x14"
        b"\x00\x15\x00\x1A\x00\x14"
        b"\x00\x33\x00\x38\x00\x32"
        b"\x00\x51\x00\x56\x00\x50"
        b"\x00\x6F\x00\x74\x00\x6E"
        b"\x00\x8D\x00\x92\x00\x8C"
        b"\x00\xAB\x00\xB0\x00\xAA"
        b"\x00\xC9\x00\xCE\x00\xC8"
        b"\x00\xE7\x00\xEC\x00\xE6"
        b"\x01\x05\x01\x0A\x01\x04"
        b"\x01\x5D\x01\x06\x01\x5C"
        b"\x00\xEA\x00\xEB\x00\xE9"
        b"\x00\xEE\x00\xEF\x00\xED"
        b"\x01\x54\x00\xE8\x01\x53"
        b"\x01\x48\x01\x49\x01\x47"
        b"\x00\x5B\x00\x5A\x01\x31"
        b"\x00\x3D\x00\x3C\x01\x28"
    )

    def __init__(self, is31_controller):
        self._is31 = is31_controller

    def __setitem__(self, led, color):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")

        rgb = unpack_from(">HHH", self.ledmap_bytes, led * 6)
        self._is31[rgb[0]] = (color >> 16) & 0xFF
        self._is31[rgb[1]] = (color >> 8) & 0xFF
        self._is31[rgb[2]] = color & 0xFF

    def __getitem__(self, led):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")
        rgb = unpack_from(">HHH", self.ledmap_bytes, led * 6)
        return (
            (self._is31[rgb[0]] << 16) | (self._is31[rgb[1]] << 8) | self._is31[rgb[2]]
        )


class Left_Ring:
    """The left eye ring of the LED glasses"""

    # ledmap = ( # These are BRG order; reordered to RGB in bytes below
    #    (341, 211, 210),  # 0
    #    (332, 181, 180),  # 1
    #    (323, 151, 150),  # 2
    #    (127, 126, 125),  # 3
    #    (154, 153, 152),  # 4
    #    (163, 162, 161),  # 5
    #    (166, 165, 164),  # 6
    #    (244, 243, 242),  # 7
    #    (259, 258, 257),  # 8
    #    (169, 168, 167),  # 9
    #    (139, 138, 137),  # 10
    #    (109, 108, 107),  # 11
    #    (79, 78, 77),  # 12
    #    (49, 48, 47),  # 13
    #    (199, 198, 197),  # 14
    #    (229, 228, 227),  # 15
    #    (19, 18, 17),  # 16
    #    (4, 3, 2),  # 17
    #    (16, 15, 14),  # 18
    #    (13, 12, 11),  # 19
    #    (10, 9, 8),  # 20
    #    (217, 216, 215),  # 21
    #    (7, 6, 5),  # 22
    #    (350, 241, 240),  # 23
    # )
    ledmap_bytes = (
        b"\x00\xD3\x00\xD2\x01\x55"
        b"\x00\xB5\x00\xB4\x01\x4C"
        b"\x00\x97\x00\x96\x01\x43"
        b"\x00\x7E\x00\x7D\x00\x7F"
        b"\x00\x99\x00\x98\x00\x9A"
        b"\x00\xA2\x00\xA1\x00\xA3"
        b"\x00\xA5\x00\xA4\x00\xA6"
        b"\x00\xF3\x00\xF2\x00\xF4"
        b"\x01\x02\x01\x01\x01\x03"
        b"\x00\xA8\x00\xA7\x00\xA9"
        b"\x00\x8A\x00\x89\x00\x8B"
        b"\x00\x6C\x00\x6B\x00\x6D"
        b"\x00\x4E\x00\x4D\x00\x4F"
        b"\x00\x30\x00\x2F\x00\x31"
        b"\x00\xC6\x00\xC5\x00\xC7"
        b"\x00\xE4\x00\xE3\x00\xE5"
        b"\x00\x12\x00\x11\x00\x13"
        b"\x00\x03\x00\x02\x00\x04"
        b"\x00\x0F\x00\x0E\x00\x10"
        b"\x00\x0C\x00\x0B\x00\x0D"
        b"\x00\x09\x00\x08\x00\x0A"
        b"\x00\xD8\x00\xD7\x00\xD9"
        b"\x00\x06\x00\x05\x00\x07"
        b"\x00\xF1\x00\xF0\x01\x5E"
    )

    def __init__(self, is31_controller):
        self._is31 = is31_controller

    def __setitem__(self, led, color):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")

        rgb = unpack_from(">HHH", self.ledmap_bytes, led * 6)
        self._is31[rgb[0]] = (color >> 16) & 0xFF
        self._is31[rgb[1]] = (color >> 8) & 0xFF
        self._is31[rgb[2]] = color & 0xFF

    def __getitem__(self, led):
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")
        rgb = unpack_from(">HHH", self.ledmap_bytes, led * 6)
        return (
            (self._is31[rgb[0]] << 16) | (self._is31[rgb[1]] << 8) | self._is31[rgb[2]]
        )


class LED_Glasses(IS31FL3741):
    """Class representing LED Glasses"""

    # ledmap = ( # These are RGB order
    #    (None, None, None),
    #    (216, 215, 217),
    #    (186, 185, 187),
    #    (36, 35, 37),
    #    (66, 65, 67),
    #    (96, 95, 97),
    #    (126, 125, 127),
    #    (156, 155, 157),
    #    (246, 245, 247),
    #    (346, 347, 345),
    #    (337, 338, 336),
    #    (328, 329, 327),
    #    (319, 320, 318),
    #    (310, 311, 309),
    #    (301, 302, 300),
    #    (292, 293, 291),
    #    (283, 284, 282),
    #    (None, None, None),
    #    (9, 8, 10),
    #    (219, 218, 220),
    #    (189, 188, 190),
    #    (39, 38, 40),
    #    (69, 68, 70),
    #    (99, 98, 100),
    #    (129, 128, 130),
    #    (159, 158, 160),
    #    (249, 248, 250),
    #    (343, 344, 342),
    #    (334, 335, 333),
    #    (325, 326, 324),
    #    (316, 317, 315),
    #    (307, 308, 306),
    #    (298, 299, 297),
    #    (289, 290, 288),
    #    (280, 281, 279),
    #    (271, 272, 270),
    #    (12, 11, 13),
    #    (222, 221, 223),
    #    (192, 191, 193),
    #    (42, 41, 43),
    #    (72, 71, 73),
    #    (102, 101, 103),
    #    (132, 131, 133),
    #    (162, 161, 163),
    #    (252, 251, 253),
    #    (268, 269, 267),
    #    (238, 239, 237),
    #    (208, 209, 207),
    #    (178, 179, 177),
    #    (148, 149, 147),
    #    (118, 119, 117),
    #    (88, 89, 87),
    #    (58, 59, 57),
    #    (28, 29, 27),
    #    (15, 14, 16),
    #    (225, 224, 226),
    #    (195, 194, 196),
    #    (45, 44, 46),
    #    (75, 74, 76),
    #    (105, 104, 106),
    #    (135, 134, 136),
    #    (165, 164, 166),
    #    (255, 254, 256),
    #    (264, 265, 263),
    #    (234, 235, 233),
    #    (204, 205, 203),
    #    (174, 175, 173),
    #    (144, 145, 143),
    #    (114, 115, 113),
    #    (84, 85, 83),
    #    (54, 55, 53),
    #    (24, 25, 23),
    #    (3, 2, 4),
    #    (213, 212, 214),
    #    (183, 182, 184),
    #    (33, 32, 34),
    #    (63, 62, 64),
    #    (93, 92, 94),
    #    (123, 122, 124),
    #    (243, 242, 244),
    #    (None, None, None),
    #    (None, None, None),
    #    (349, 262, 348),
    #    (331, 202, 330),
    #    (322, 172, 321),
    #    (313, 142, 312),
    #    (304, 112, 303),
    #    (295, 82, 294),
    #    (286, 52, 285),
    #    (277, 22, 276))
    # These pixels aren't connected to anything and are safe to use for pixels that aren't visible
    # unused_pixels = (120, 121, 314)

    # This table has 'None' elements replaced w/unused_pixels equivalent
    ledmap_bytes = (
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x00\xD8\x00\xD7\x00\xD9"
        b"\x00\xBA\x00\xB9\x00\xBB"
        b"\x00\x24\x00\x23\x00\x25"
        b"\x00\x42\x00\x41\x00\x43"
        b"\x00\x60\x00\x5F\x00\x61"
        b"\x00\x7E\x00\x7D\x00\x7F"
        b"\x00\x9C\x00\x9B\x00\x9D"
        b"\x00\xF6\x00\xF5\x00\xF7"
        b"\x01\x5A\x01\x5B\x01\x59"
        b"\x01\x51\x01\x52\x01\x50"
        b"\x01\x48\x01\x49\x01\x47"
        b"\x01\x3F\x01\x40\x01\x3E"
        b"\x01\x36\x01\x37\x01\x35"
        b"\x01\x2D\x01\x2E\x01\x2C"
        b"\x01\x24\x01\x25\x01\x23"
        b"\x01\x1B\x01\x1C\x01\x1A"
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x00\x09\x00\x08\x00\x0A"
        b"\x00\xDB\x00\xDA\x00\xDC"
        b"\x00\xBD\x00\xBC\x00\xBE"
        b"\x00\x27\x00\x26\x00\x28"
        b"\x00\x45\x00\x44\x00\x46"
        b"\x00\x63\x00\x62\x00\x64"
        b"\x00\x81\x00\x80\x00\x82"
        b"\x00\x9F\x00\x9E\x00\xA0"
        b"\x00\xF9\x00\xF8\x00\xFA"
        b"\x01\x57\x01\x58\x01\x56"
        b"\x01\x4E\x01\x4F\x01\x4D"
        b"\x01\x45\x01\x46\x01\x44"
        b"\x01\x3C\x01\x3D\x01\x3B"
        b"\x01\x33\x01\x34\x01\x32"
        b"\x01\x2A\x01\x2B\x01\x29"
        b"\x01\x21\x01\x22\x01\x20"
        b"\x01\x18\x01\x19\x01\x17"
        b"\x01\x0F\x01\x10\x01\x0E"
        b"\x00\x0C\x00\x0B\x00\x0D"
        b"\x00\xDE\x00\xDD\x00\xDF"
        b"\x00\xC0\x00\xBF\x00\xC1"
        b"\x00\x2A\x00\x29\x00\x2B"
        b"\x00\x48\x00\x47\x00\x49"
        b"\x00\x66\x00\x65\x00\x67"
        b"\x00\x84\x00\x83\x00\x85"
        b"\x00\xA2\x00\xA1\x00\xA3"
        b"\x00\xFC\x00\xFB\x00\xFD"
        b"\x01\x0C\x01\x0D\x01\x0B"
        b"\x00\xEE\x00\xEF\x00\xED"
        b"\x00\xD0\x00\xD1\x00\xCF"
        b"\x00\xB2\x00\xB3\x00\xB1"
        b"\x00\x94\x00\x95\x00\x93"
        b"\x00\x76\x00\x77\x00\x75"
        b"\x00\x58\x00\x59\x00\x57"
        b"\x00\x3A\x00\x3B\x00\x39"
        b"\x00\x1C\x00\x1D\x00\x1B"
        b"\x00\x0F\x00\x0E\x00\x10"
        b"\x00\xE1\x00\xE0\x00\xE2"
        b"\x00\xC3\x00\xC2\x00\xC4"
        b"\x00\x2D\x00\x2C\x00\x2E"
        b"\x00\x4B\x00\x4A\x00\x4C"
        b"\x00\x69\x00\x68\x00\x6A"
        b"\x00\x87\x00\x86\x00\x88"
        b"\x00\xA5\x00\xA4\x00\xA6"
        b"\x00\xFF\x00\xFE\x01\x00"
        b"\x01\x08\x01\x09\x01\x07"
        b"\x00\xEA\x00\xEB\x00\xE9"
        b"\x00\xCC\x00\xCD\x00\xCB"
        b"\x00\xAE\x00\xAF\x00\xAD"
        b"\x00\x90\x00\x91\x00\x8F"
        b"\x00\x72\x00\x73\x00\x71"
        b"\x00\x54\x00\x55\x00\x53"
        b"\x00\x36\x00\x37\x00\x35"
        b"\x00\x18\x00\x19\x00\x17"
        b"\x00\x03\x00\x02\x00\x04"
        b"\x00\xD5\x00\xD4\x00\xD6"
        b"\x00\xB7\x00\xB6\x00\xB8"
        b"\x00\x21\x00\x20\x00\x22"
        b"\x00\x3F\x00\x3E\x00\x40"
        b"\x00\x5D\x00\x5C\x00\x5E"
        b"\x00\x7B\x00\x7A\x00\x7C"
        b"\x00\xF3\x00\xF2\x00\xF4"
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x01\x5D\x01\x06\x01\x5C"
        b"\x01\x4B\x00\xCA\x01\x4A"
        b"\x01\x42\x00\xAC\x01\x41"
        b"\x01\x39\x00\x8E\x01\x38"
        b"\x01\x30\x00\x70\x01\x2F"
        b"\x01\x27\x00\x52\x01\x26"
        b"\x01\x1E\x00\x34\x01\x1D"
        b"\x01\x15\x00\x16\x01\x14"
    )
    width = 18
    height = 5

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
        return unpack_from(
            ">HHH", LED_Glasses.ledmap_bytes, ((y * LED_Glasses.width) + x) * 6
        )
