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
from . import IS31FL3741


class ISSI_EVB(IS31FL3741):
    """Supports the ISSI IS31FL3741 eval board"""

    width = 13
    height = 9

    @staticmethod
    def pixel_addrs(x, y):
        """Calulate the RGB offsets into the device array for x,y pixel"""
        if x > 9:
            offset = (x + 80 + y * 3) * 3
        else:
            offset = (x + y * 10) * 3

        return (offset + 2, offset + 1, offset)
