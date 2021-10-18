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
from adafruit_is31fl3741 import _IS3741_ADDR_DEFAULT, NO_BUFFER, IS3741_BGR
from . import IS31FL3741_colorXY

try:
    # Used only for typing
    from typing import Tuple
    import busio
except ImportError:
    pass


class Adafruit_RGBMatrixQT(IS31FL3741_colorXY):
    """Supports the Adafruit STEMMA QT IS31FL3741 RGB LED matrix."""

    rowmap = [8, 5, 4, 3, 2, 1, 0, 7, 6]

    def __init__(
        self,
        i2c: busio.I2C,
        address: int = _IS3741_ADDR_DEFAULT,
        allocate: int = NO_BUFFER,
        order: int = IS3741_BGR,
    ):
        super().__init__(i2c, 13, 9, address=address, allocate=allocate, order=order)

    @staticmethod
    def pixel_addrs(x: int, y: int) -> Tuple[int, int, int]:
        """Calulate the RGB offsets into the device array for x,y pixel"""
        y = Adafruit_RGBMatrixQT.rowmap[y]  # Reorder rows

        offset = 3 * (x + (y * 10) if x < 10 else x + (80 + y * 3))

        # print(x, ",", y, "->", hex(offset))
        if x & 1 or x == 12:  # odds + last col
            r_off, g_off, b_off = 2, 0, 1
        else:  # evens
            r_off, g_off, b_off = 0, 1, 2

        return (offset + r_off, offset + g_off, offset + b_off)
