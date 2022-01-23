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
`is31fl3741_pixelbuf` - IS31FL3741 PixelBuf driver
====================================================

* Author(s): Mark Komus, Damien P. George, Scott Shawcroft, Carter Nelson, Rose Hooper
"""

# pylint: disable=ungrouped-imports
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
    import is31fl3741
except ImportError:
    pass


__version__ = "0.0.0-auto.0"
# __repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741.git"


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


class IS31FL3741_PixelBuf(adafruit_pixelbuf.PixelBuf):
    """
    A sequence of LEDs controlled by an IS31FL3741 driver.

    :param ~is31fl3741.IS31FL3741 is31: the IS31FL3741 device to output with
    :param ~Tuple[int, ...] mapping: map the pixels in the buffer to the order addressed
        by the driver chip
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

    def __init__(
        self,
        is31: is31fl3741.IS31FL3741,
        mapping: tuple,
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

        n = int(len(mapping) / 3)

        super().__init__(
            n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
        )

        self.is31fl3741 = is31
        self.addr = addr
        if not isinstance(mapping, tuple):
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
        self.is31fl3741.reset()

        # Set scaling for all LEDs to maximum
        for led in range(352):
            self.is31fl3741.set_led(led, 0xFF, 2)

        self.is31fl3741.set_global_current(0xFE)
        self.is31fl3741.enable()

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
        self.is31fl3741.write(self.mapping, buffer)
