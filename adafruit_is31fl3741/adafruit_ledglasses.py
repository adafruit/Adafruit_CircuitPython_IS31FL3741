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
from struct import unpack_from  # pylint: disable=no-name-in-module

from adafruit_is31fl3741 import _IS3741_ADDR_DEFAULT, NO_BUFFER, IS3741_BGR, MUST_BUFFER
from . import IS31FL3741_colorXY

try:
    # Used only for typing
    from typing import Tuple, Any  # pylint: disable=unused-import
    import busio
except ImportError:
    pass


class BaseRing:
    """
    Base class implementing common ring behaviour.
    """

    ledmap_bytes = b""

    def __init__(self, is31_controller: IS31FL3741_colorXY, order: int):
        self._is31 = is31_controller
        self.r_offset = (order >> 4) & 3
        self.g_offset = (order >> 2) & 3
        self.b_offset = order & 3

    def __setitem__(self, led: int, color: int) -> None:
        offset = self.pixel_addrs(led)
        self._is31[offset[self.r_offset]] = (color >> 16) & 0xFF
        self._is31[offset[self.g_offset]] = (color >> 8) & 0xFF
        self._is31[offset[self.b_offset]] = color & 0xFF

    def __getitem__(self, led: int) -> int:
        offset = self.pixel_addrs(led)
        return (
            (self._is31[offset[self.r_offset]] << 16)
            | (self._is31[offset[self.g_offset]] << 8)
            | self._is31[offset[self.b_offset]]
        )

    def fill(self, color: int) -> None:
        """Sets all LEDs in a ring to the same color.

        :param color: Packed RGB color (0xRRGGBB).
        """
        red = (color >> 16) & 0xFF
        green = (color >> 8) & 0xFF
        blue = color & 0xFF
        for x in range(24):
            offset = unpack_from(">HHH", self.ledmap_bytes, x * 6)
            self._is31[offset[self.r_offset]] = red
            self._is31[offset[self.g_offset]] = green
            self._is31[offset[self.b_offset]] = blue

    def pixel_addrs(self, led):
        """
        Get RGB addresses for led no `led`.
        """
        if not 0 <= led <= 23:
            raise ValueError("led must be 0~23")
        return unpack_from(">HHH", self.ledmap_bytes, led * 6)


class Right_Ring(BaseRing):
    """The right eye ring of the LED glasses"""

    ledmap_bytes = (
        b"\x01\x1F\x00\x1E\x00\x1F"
        b"\x01\x16\x00\x00\x00\x01"
        b"\x01\x11\x01\x13\x01\x12"
        b"\x01\x1A\x01\x1C\x01\x1B"
        b"\x01\x0E\x01\x10\x01\x0F"
        b"\x00\x1B\x00\x1D\x00\x1C"
        b"\x00\x17\x00\x19\x00\x18"
        b"\x01\x14\x00\x16\x01\x15"
        b"\x00\x14\x00\x1A\x00\x15"
        b"\x00\x32\x00\x38\x00\x33"
        b"\x00\x50\x00\x56\x00\x51"
        b"\x00\x6E\x00\x74\x00\x6F"
        b"\x00\x8C\x00\x92\x00\x8D"
        b"\x00\xAA\x00\xB0\x00\xAB"
        b"\x00\xC8\x00\xCE\x00\xC9"
        b"\x00\xE6\x00\xEC\x00\xE7"
        b"\x01\x04\x01\x0A\x01\x05"
        b"\x01\x5C\x01\x06\x01\x5D"
        b"\x00\xE9\x00\xEB\x00\xEA"
        b"\x00\xED\x00\xEF\x00\xEE"
        b"\x01\x53\x00\xE8\x01\x54"
        b"\x01\x47\x01\x49\x01\x48"
        b"\x01\x31\x00\x5A\x00\x5B"
        b"\x01\x28\x00\x3C\x00\x3D"
    )


class Left_Ring(BaseRing):
    """The left eye ring of the LED glasses"""

    ledmap_bytes = (
        b"\x01\x55\x00\xD2\x00\xD3"
        b"\x01\x4C\x00\xB4\x00\xB5"
        b"\x01\x43\x00\x96\x00\x97"
        b"\x00\x7F\x00\x7D\x00\x7E"
        b"\x00\x9A\x00\x98\x00\x99"
        b"\x00\xA3\x00\xA1\x00\xA2"
        b"\x00\xA6\x00\xA4\x00\xA5"
        b"\x00\xF4\x00\xF2\x00\xF3"
        b"\x01\x03\x01\x01\x01\x02"
        b"\x00\xA9\x00\xA7\x00\xA8"
        b"\x00\x8B\x00\x89\x00\x8A"
        b"\x00\x6D\x00\x6B\x00\x6C"
        b"\x00\x4F\x00\x4D\x00\x4E"
        b"\x00\x31\x00\x2F\x00\x30"
        b"\x00\xC7\x00\xC5\x00\xC6"
        b"\x00\xE5\x00\xE3\x00\xE4"
        b"\x00\x13\x00\x11\x00\x12"
        b"\x00\x04\x00\x02\x00\x03"
        b"\x00\x10\x00\x0E\x00\x0F"
        b"\x00\x0D\x00\x0B\x00\x0C"
        b"\x00\x0A\x00\x08\x00\x09"
        b"\x00\xD9\x00\xD7\x00\xD8"
        b"\x00\x07\x00\x05\x00\x06"
        b"\x01\x5E\x00\xF0\x00\xF1"
    )


class LED_Glasses(IS31FL3741_colorXY):
    """Class representing LED Glasses"""

    # 'missing' pixels, such as the nose bridge, are assigned to indices
    # 120, 121 and 314 (elements unused by the glasses, which has 116 RGB
    # LEDs of a possible 117).
    ledmap_bytes = (
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x00\x0A\x00\x08\x00\x09"
        b"\x00\x0D\x00\x0B\x00\x0C"
        b"\x00\x10\x00\x0E\x00\x0F"
        b"\x00\x04\x00\x02\x00\x03"
        b"\x00\xD9\x00\xD7\x00\xD8"
        b"\x00\xDC\x00\xDA\x00\xDB"
        b"\x00\xDF\x00\xDD\x00\xDE"
        b"\x00\xE2\x00\xE0\x00\xE1"
        b"\x00\xD6\x00\xD4\x00\xD5"
        b"\x00\xBB\x00\xB9\x00\xBA"
        b"\x00\xBE\x00\xBC\x00\xBD"
        b"\x00\xC1\x00\xBF\x00\xC0"
        b"\x00\xC4\x00\xC2\x00\xC3"
        b"\x00\xB8\x00\xB6\x00\xB7"
        b"\x00\x25\x00\x23\x00\x24"
        b"\x00\x28\x00\x26\x00\x27"
        b"\x00\x2B\x00\x29\x00\x2A"
        b"\x00\x2E\x00\x2C\x00\x2D"
        b"\x00\x22\x00\x20\x00\x21"
        b"\x00\x43\x00\x41\x00\x42"
        b"\x00\x46\x00\x44\x00\x45"
        b"\x00\x49\x00\x47\x00\x48"
        b"\x00\x4C\x00\x4A\x00\x4B"
        b"\x00\x40\x00\x3E\x00\x3F"
        b"\x00\x61\x00\x5F\x00\x60"
        b"\x00\x64\x00\x62\x00\x63"
        b"\x00\x67\x00\x65\x00\x66"
        b"\x00\x6A\x00\x68\x00\x69"
        b"\x00\x5E\x00\x5C\x00\x5D"
        b"\x00\x7F\x00\x7D\x00\x7E"
        b"\x00\x82\x00\x80\x00\x81"
        b"\x00\x85\x00\x83\x00\x84"
        b"\x00\x88\x00\x86\x00\x87"
        b"\x00\x7C\x00\x7A\x00\x7B"
        b"\x00\x9D\x00\x9B\x00\x9C"
        b"\x00\xA0\x00\x9E\x00\x9F"
        b"\x00\xA3\x00\xA1\x00\xA2"
        b"\x00\xA6\x00\xA4\x00\xA5"
        b"\x00\xF4\x00\xF2\x00\xF3"
        b"\x00\xF7\x00\xF5\x00\xF6"
        b"\x00\xFA\x00\xF8\x00\xF9"
        b"\x00\xFD\x00\xFB\x00\xFC"
        b"\x01\x00\x00\xFE\x00\xFF"
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x01\x59\x01\x5B\x01\x5A"
        b"\x01\x56\x01\x58\x01\x57"
        b"\x01\x0B\x01\x0D\x01\x0C"
        b"\x01\x07\x01\x09\x01\x08"
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x01\x50\x01\x52\x01\x51"
        b"\x01\x4D\x01\x4F\x01\x4E"
        b"\x00\xED\x00\xEF\x00\xEE"
        b"\x00\xE9\x00\xEB\x00\xEA"
        b"\x01\x5C\x01\x06\x01\x5D"
        b"\x01\x47\x01\x49\x01\x48"
        b"\x01\x44\x01\x46\x01\x45"
        b"\x00\xCF\x00\xD1\x00\xD0"
        b"\x00\xCB\x00\xCD\x00\xCC"
        b"\x01\x4A\x00\xCA\x01\x4B"
        b"\x01\x3E\x01\x40\x01\x3F"
        b"\x01\x3B\x01\x3D\x01\x3C"
        b"\x00\xB1\x00\xB3\x00\xB2"
        b"\x00\xAD\x00\xAF\x00\xAE"
        b"\x01\x41\x00\xAC\x01\x42"
        b"\x01\x35\x01\x37\x01\x36"
        b"\x01\x32\x01\x34\x01\x33"
        b"\x00\x93\x00\x95\x00\x94"
        b"\x00\x8F\x00\x91\x00\x90"
        b"\x01\x38\x00\x8E\x01\x39"
        b"\x01\x2C\x01\x2E\x01\x2D"
        b"\x01\x29\x01\x2B\x01\x2A"
        b"\x00\x75\x00\x77\x00\x76"
        b"\x00\x71\x00\x73\x00\x72"
        b"\x01\x2F\x00\x70\x01\x30"
        b"\x01\x23\x01\x25\x01\x24"
        b"\x01\x20\x01\x22\x01\x21"
        b"\x00\x57\x00\x59\x00\x58"
        b"\x00\x53\x00\x55\x00\x54"
        b"\x01\x26\x00\x52\x01\x27"
        b"\x01\x1A\x01\x1C\x01\x1B"
        b"\x01\x17\x01\x19\x01\x18"
        b"\x00\x39\x00\x3B\x00\x3A"
        b"\x00\x35\x00\x37\x00\x36"
        b"\x01\x1D\x00\x34\x01\x1E"
        b"\x00\x78\x00\x79\x01\x3A"
        b"\x01\x0E\x01\x10\x01\x0F"
        b"\x00\x1B\x00\x1D\x00\x1C"
        b"\x00\x17\x00\x19\x00\x18"
        b"\x01\x14\x00\x16\x01\x15"
    )

    def __init__(
        self,
        i2c: busio.I2C,
        address: int = _IS3741_ADDR_DEFAULT,
        allocate: int = NO_BUFFER,
        order: int = IS3741_BGR,
    ):
        super().__init__(i2c, 18, 5, address=address, allocate=allocate, order=order)

        self.set_led_scaling(0xFF)  # turn on LEDs all the way
        self.global_current = 0xFE  # set current to max
        self.enable = True  # enable!

        self.right_ring = Right_Ring(self, order)
        self.left_ring = Left_Ring(self, order)
        self.grid = self

    @staticmethod
    def pixel_addrs(x: int, y: int) -> Tuple[Any, ...]:
        return unpack_from(">HHH", LED_Glasses.ledmap_bytes, ((x * 5) + y) * 6)


__all__ = ["LED_Glasses", "Left_Ring", "Right_Ring", "NO_BUFFER", "MUST_BUFFER"]
