# SPDX-FileCopyrightText: 2016 Damien P. George
# SPDX-FileCopyrightText: 2017 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
# SPDX-FileCopyrightText: 2019 Rose Hooper
# SPDX-FileCopyrightText: 2021 Mark Komus
#
# SPDX-License-Identifier: MIT
#
# Based on the Neopixel python library

"""
`is31fl3741` - IS31FL3741 driver
====================================================

* Author(s): Mark Komus, Damien P. George, Scott Shawcroft, Carter Nelson, Rose Hooper
"""

# pylint: disable=ungrouped-imports
import sys
from is31fl3741 import is31fl3741_write
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bit import RWBit
from adafruit_bus_device import i2c_device
import time

try:
    import adafruit_pixelbuf
except ImportError:
    try:
        import _pixelbuf as adafruit_pixelbuf
    except ImportError:
        import adafruit_pypixelbuf as adafruit_pixelbuf


try:
    # Used only for typing
    from typing import Optional, Type
    from types import TracebackType
except ImportError:
    pass


__version__ = "0.0.0-auto.0"
#__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741.git"


# Pixel color order constants
BGR = "BGR"
"""Blue Green Red"""
RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""

_IS3741_COMMANDREGISTER = 0xFD
_IS3741_COMMANDREGISTERLOCK = 0xFE
_IS3741_INTMASKREGISTER = 0xF0
_IS3741_INTSTATUSREGISTER = 0xF1
_IS3741_IDREGISTER = 0xFC

_IS3741_FUNCREG_CONFIG = 0x00
_IS3741_FUNCREG_GCURRENT = 0x01
_IS3741_FUNCREG_RESET = 0x3F

class IS31FL3741_PixelBuf(adafruit_pixelbuf.PixelBuf):
    """
    A sequence of LEDs controlled by an IS31FL3741 driver.

    :param ~busio.I2C i2c: the I2C bus to output with
    :param ~int addr: the I2C address of the IS31FL3741 device
    :param ~Tuple[int, ...] mapping: map the pixels in the buffer to the order addressed by the driver chip
    :param int n: The number of neopixels in the chain
    :param int bpp: Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0 where 1.0 is full
      brightness
    :param bool auto_write: True if the neopixels should immediately change when set. If False,
      `show` must be called explicitly.
    :param str pixel_order: Set the pixel color channel order. GRBW is set by default.
    :param bool init: True if the IS31FL3741 chip should be initialized.

    .. py:method:: IS31FL3741_PixelBuf.show()

        Shows the new colors on the pixels themselves if they haven't already
        been autowritten.

        The colors may or may not be showing after this function returns because
        it may be done asynchronously.

    .. py:method:: IS31FL3741_PixelBuf.fill(color)

        Colors all pixels the given ***color***.

    .. py:attribute:: brightness

        Overall brightness of the pixels (0 to 1.0)

    """

    _page_reg = UnaryStruct(_IS3741_COMMANDREGISTER, "<B")
    _lock_reg = UnaryStruct(_IS3741_COMMANDREGISTERLOCK, "<B")
    _id_reg = UnaryStruct(_IS3741_IDREGISTER, "<B")
    _config_reg = UnaryStruct(_IS3741_FUNCREG_CONFIG, "<B")
    _gcurrent_reg = UnaryStruct(_IS3741_FUNCREG_GCURRENT, "<B")
    _reset_reg = UnaryStruct(_IS3741_FUNCREG_RESET, "<B")
    _shutdown_bit = RWBit(_IS3741_FUNCREG_CONFIG, 0)

    def __init__(
        self,
        i2c: busio.I2C,
        mapping: tuple,
        n: int,
        *,
        addr: int = 0x30,
        bpp: int = 3,
        brightness: float = 1.0,
        auto_write: bool = True,
        pixel_order: str = None,
        init: bool = True
    ):
        if not pixel_order:
            pixel_order = BGR if bpp == 3 else GRBW
        elif isinstance(pixel_order, tuple):
            order_list = [RGBW[order] for order in pixel_order]
            pixel_order = "".join(order_list)

        super().__init__(
            n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
        )

        self.i2c = i2c
        self.i2c_device = i2c_device.I2CDevice(i2c, addr)
        self.addr = addr
        if type(mapping) is not tuple:
            raise AttributeError("Mapping must be a tuple")
        self.mapping = mapping

        if init is True:
            self.initialize()

    def deinit(self) -> None:
        """Blank out the LEDs."""
        self.fill(0)
        self.show()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def initialize(self) -> None:
        """Initialize"""
        self._lock_reg = 0xC5
        self._page_reg = 4
        self._reset_reg = 0xAE

        # Set scaling for all LEDs to maximum
        scalebuf = bytearray([0xFF] * 181)  # 180 bytes + 1 for reg addr
        scalebuf[0] = 0  # Initial register address
        self._lock_reg = 0xC5
        self._page_reg = 2
        with self.i2c_device as i2c:
            i2c.write(scalebuf)

        self._lock_reg = 0xC5
        self._page_reg = 3
        with self.i2c_device as i2c:
            i2c.write(scalebuf, end=172)  # 2nd page is smaller

        self._lock_reg = 0xC5
        self._page_reg = 4
        self._gcurrent_reg = 0xFE # Set global current to max

        self._lock_reg = 0xC5
        self._page_reg = 4
        self._shutdown_bit = True # Enable driver chip

    @property
    def n(self) -> int:
        """
        The number of LEDs in the chain (read-only)
        """
        return len(self)

    def write(self) -> None:
        """.. deprecated: 1.0.0

        Use ``show`` instead. It matches Micro:Bit and Arduino APIs."""
        self.show()

    def _transmit(self, buffer: bytearray) -> None:
        is31fl3741_write(i2c=self.i2c, addr=self.addr, mapping=self.mapping, buffer=buffer)
