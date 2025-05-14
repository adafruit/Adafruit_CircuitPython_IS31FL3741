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

from adafruit_is31fl3741 import _IS3741_ADDR_DEFAULT, IS3741_BGR, MUST_BUFFER, NO_BUFFER

from . import IS31FL3741_colorXY

try:
    # Used only for typing
    from typing import Any, Tuple

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
        b"\x01\x1f\x00\x1e\x00\x1f"
        b"\x01\x16\x00\x00\x00\x01"
        b"\x01\x11\x01\x13\x01\x12"
        b"\x01\x1a\x01\x1c\x01\x1b"
        b"\x01\x0e\x01\x10\x01\x0f"
        b"\x00\x1b\x00\x1d\x00\x1c"
        b"\x00\x17\x00\x19\x00\x18"
        b"\x01\x14\x00\x16\x01\x15"
        b"\x00\x14\x00\x1a\x00\x15"
        b"\x00\x32\x00\x38\x00\x33"
        b"\x00\x50\x00\x56\x00\x51"
        b"\x00\x6e\x00\x74\x00\x6f"
        b"\x00\x8c\x00\x92\x00\x8d"
        b"\x00\xaa\x00\xb0\x00\xab"
        b"\x00\xc8\x00\xce\x00\xc9"
        b"\x00\xe6\x00\xec\x00\xe7"
        b"\x01\x04\x01\x0a\x01\x05"
        b"\x01\x5c\x01\x06\x01\x5d"
        b"\x00\xe9\x00\xeb\x00\xea"
        b"\x00\xed\x00\xef\x00\xee"
        b"\x01\x53\x00\xe8\x01\x54"
        b"\x01\x47\x01\x49\x01\x48"
        b"\x01\x31\x00\x5a\x00\x5b"
        b"\x01\x28\x00\x3c\x00\x3d"
    )


class Left_Ring(BaseRing):
    """The left eye ring of the LED glasses"""

    ledmap_bytes = (
        b"\x01\x55\x00\xd2\x00\xd3"
        b"\x01\x4c\x00\xb4\x00\xb5"
        b"\x01\x43\x00\x96\x00\x97"
        b"\x00\x7f\x00\x7d\x00\x7e"
        b"\x00\x9a\x00\x98\x00\x99"
        b"\x00\xa3\x00\xa1\x00\xa2"
        b"\x00\xa6\x00\xa4\x00\xa5"
        b"\x00\xf4\x00\xf2\x00\xf3"
        b"\x01\x03\x01\x01\x01\x02"
        b"\x00\xa9\x00\xa7\x00\xa8"
        b"\x00\x8b\x00\x89\x00\x8a"
        b"\x00\x6d\x00\x6b\x00\x6c"
        b"\x00\x4f\x00\x4d\x00\x4e"
        b"\x00\x31\x00\x2f\x00\x30"
        b"\x00\xc7\x00\xc5\x00\xc6"
        b"\x00\xe5\x00\xe3\x00\xe4"
        b"\x00\x13\x00\x11\x00\x12"
        b"\x00\x04\x00\x02\x00\x03"
        b"\x00\x10\x00\x0e\x00\x0f"
        b"\x00\x0d\x00\x0b\x00\x0c"
        b"\x00\x0a\x00\x08\x00\x09"
        b"\x00\xd9\x00\xd7\x00\xd8"
        b"\x00\x07\x00\x05\x00\x06"
        b"\x01\x5e\x00\xf0\x00\xf1"
    )


class LED_Glasses(IS31FL3741_colorXY):
    """Class representing LED Glasses"""

    # 'missing' pixels, such as the nose bridge, are assigned to indices
    # 120, 121 and 314 (elements unused by the glasses, which has 116 RGB
    # LEDs of a possible 117).
    ledmap_bytes = (
        b"\x00\x78\x00\x79\x01\x3a"
        b"\x00\x0a\x00\x08\x00\x09"
        b"\x00\x0d\x00\x0b\x00\x0c"
        b"\x00\x10\x00\x0e\x00\x0f"
        b"\x00\x04\x00\x02\x00\x03"
        b"\x00\xd9\x00\xd7\x00\xd8"
        b"\x00\xdc\x00\xda\x00\xdb"
        b"\x00\xdf\x00\xdd\x00\xde"
        b"\x00\xe2\x00\xe0\x00\xe1"
        b"\x00\xd6\x00\xd4\x00\xd5"
        b"\x00\xbb\x00\xb9\x00\xba"
        b"\x00\xbe\x00\xbc\x00\xbd"
        b"\x00\xc1\x00\xbf\x00\xc0"
        b"\x00\xc4\x00\xc2\x00\xc3"
        b"\x00\xb8\x00\xb6\x00\xb7"
        b"\x00\x25\x00\x23\x00\x24"
        b"\x00\x28\x00\x26\x00\x27"
        b"\x00\x2b\x00\x29\x00\x2a"
        b"\x00\x2e\x00\x2c\x00\x2d"
        b"\x00\x22\x00\x20\x00\x21"
        b"\x00\x43\x00\x41\x00\x42"
        b"\x00\x46\x00\x44\x00\x45"
        b"\x00\x49\x00\x47\x00\x48"
        b"\x00\x4c\x00\x4a\x00\x4b"
        b"\x00\x40\x00\x3e\x00\x3f"
        b"\x00\x61\x00\x5f\x00\x60"
        b"\x00\x64\x00\x62\x00\x63"
        b"\x00\x67\x00\x65\x00\x66"
        b"\x00\x6a\x00\x68\x00\x69"
        b"\x00\x5e\x00\x5c\x00\x5d"
        b"\x00\x7f\x00\x7d\x00\x7e"
        b"\x00\x82\x00\x80\x00\x81"
        b"\x00\x85\x00\x83\x00\x84"
        b"\x00\x88\x00\x86\x00\x87"
        b"\x00\x7c\x00\x7a\x00\x7b"
        b"\x00\x9d\x00\x9b\x00\x9c"
        b"\x00\xa0\x00\x9e\x00\x9f"
        b"\x00\xa3\x00\xa1\x00\xa2"
        b"\x00\xa6\x00\xa4\x00\xa5"
        b"\x00\xf4\x00\xf2\x00\xf3"
        b"\x00\xf7\x00\xf5\x00\xf6"
        b"\x00\xfa\x00\xf8\x00\xf9"
        b"\x00\xfd\x00\xfb\x00\xfc"
        b"\x01\x00\x00\xfe\x00\xff"
        b"\x00\x78\x00\x79\x01\x3a"
        b"\x01\x59\x01\x5b\x01\x5a"
        b"\x01\x56\x01\x58\x01\x57"
        b"\x01\x0b\x01\x0d\x01\x0c"
        b"\x01\x07\x01\x09\x01\x08"
        b"\x00\x78\x00\x79\x01\x3a"
        b"\x01\x50\x01\x52\x01\x51"
        b"\x01\x4d\x01\x4f\x01\x4e"
        b"\x00\xed\x00\xef\x00\xee"
        b"\x00\xe9\x00\xeb\x00\xea"
        b"\x01\x5c\x01\x06\x01\x5d"
        b"\x01\x47\x01\x49\x01\x48"
        b"\x01\x44\x01\x46\x01\x45"
        b"\x00\xcf\x00\xd1\x00\xd0"
        b"\x00\xcb\x00\xcd\x00\xcc"
        b"\x01\x4a\x00\xca\x01\x4b"
        b"\x01\x3e\x01\x40\x01\x3f"
        b"\x01\x3b\x01\x3d\x01\x3c"
        b"\x00\xb1\x00\xb3\x00\xb2"
        b"\x00\xad\x00\xaf\x00\xae"
        b"\x01\x41\x00\xac\x01\x42"
        b"\x01\x35\x01\x37\x01\x36"
        b"\x01\x32\x01\x34\x01\x33"
        b"\x00\x93\x00\x95\x00\x94"
        b"\x00\x8f\x00\x91\x00\x90"
        b"\x01\x38\x00\x8e\x01\x39"
        b"\x01\x2c\x01\x2e\x01\x2d"
        b"\x01\x29\x01\x2b\x01\x2a"
        b"\x00\x75\x00\x77\x00\x76"
        b"\x00\x71\x00\x73\x00\x72"
        b"\x01\x2f\x00\x70\x01\x30"
        b"\x01\x23\x01\x25\x01\x24"
        b"\x01\x20\x01\x22\x01\x21"
        b"\x00\x57\x00\x59\x00\x58"
        b"\x00\x53\x00\x55\x00\x54"
        b"\x01\x26\x00\x52\x01\x27"
        b"\x01\x1a\x01\x1c\x01\x1b"
        b"\x01\x17\x01\x19\x01\x18"
        b"\x00\x39\x00\x3b\x00\x3a"
        b"\x00\x35\x00\x37\x00\x36"
        b"\x01\x1d\x00\x34\x01\x1e"
        b"\x00\x78\x00\x79\x01\x3a"
        b"\x01\x0e\x01\x10\x01\x0f"
        b"\x00\x1b\x00\x1d\x00\x1c"
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
