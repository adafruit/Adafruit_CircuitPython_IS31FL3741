# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3741.issi_evb`
====================================================

CircuitPython driver for the IS31FL3741 ISSI Eval Board


* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

* `ISSI IS31FL3741 eval board
  <https://www.digikey.com/en/products/detail/issi-integrated-silicon-solution-inc/IS31FL3741-QFLS4-EB/10243951>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from adafruit_is31fl3741 import _IS3741_ADDR_DEFAULT, NO_BUFFER, IS3741_BGR
from adafruit_is31fl3741 import IS31FL3741_colorXY

try:
    # Used only for typing
    from typing import Tuple  # pylint: disable=unused-import
    import busio
except ImportError:
    pass


class ISSI_EVB(IS31FL3741_colorXY):
    """Supports the ISSI IS31FL3741 eval board"""

    def __init__(
        self,
        i2c: busio.I2C,
        address: int = _IS3741_ADDR_DEFAULT,
        allocate: int = NO_BUFFER,
        order: int = IS3741_BGR,
    ):
        super().__init__(i2c, 9, 13, address=address, allocate=allocate, order=order)

    @staticmethod
    def pixel_addrs(x: int, y: int) -> Tuple[int, int, int]:
        """Calulate the RGB offsets into the device array for x,y pixel"""
        if y > 2:
            offset = (x * 10 + 12 - y) * 3
        else:
            offset = (92 + x * 3 - y) * 3

        return (offset, offset + 1, offset + 2)
