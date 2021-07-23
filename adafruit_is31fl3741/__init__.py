# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3741`
====================================================

CircuitPython driver for the IS31FL3741 RGB Matrix IC.

Base library.

* Author(s): Ladyada

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import math
import time
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bit import RWBit
from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3741.git"

_IS3741_ADDR_DEFAULT = 0x30

_IS3741_COMMANDREGISTER = 0xFD
_IS3741_COMMANDREGISTERLOCK = 0xFE
_IS3741_INTMASKREGISTER = 0xF0
_IS3741_INTSTATUSREGISTER = 0xF1
_IS3741_IDREGISTER = 0xFC

_IS3741_FUNCREG_CONFIG = 0x00
_IS3741_FUNCREG_GCURRENT = 0x01
_IS3741_FUNCREG_RESET = 0x3F


class IS31FL3741:
    """
    The IS31FL3741 is an abstract class contain the main function related to this chip.
    Each board needs to define width, height and pixel_addr.

    :param ~adafruit_bus_device.i2c_device i2c_device: the connected i2c bus i2c_device
    :param address: the device address; defaults to 0x30
    """

    width = 13
    height = 9

    _page_reg = UnaryStruct(_IS3741_COMMANDREGISTER, "<B")
    _lock_reg = UnaryStruct(_IS3741_COMMANDREGISTERLOCK, "<B")
    _id_reg = UnaryStruct(_IS3741_IDREGISTER, "<B")
    _config_reg = UnaryStruct(_IS3741_FUNCREG_CONFIG, "<B")
    _gcurrent_reg = UnaryStruct(_IS3741_FUNCREG_GCURRENT, "<B")
    _reset_reg = UnaryStruct(_IS3741_FUNCREG_RESET, "<B")
    _shutdown_bit = RWBit(_IS3741_FUNCREG_CONFIG, 0)

    def __init__(self, i2c, address=_IS3741_ADDR_DEFAULT):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        if self._id_reg != 2 * address:
            raise AttributeError("Cannot find a IS31FL3741 at address 0x", address)
        self._buf = bytearray(2)
        self._page = None
        self.reset()


    def reset(self):
        self.page = 4
        self._reset_reg = 0xAE

    def unlock(self):
        self._lock_reg = 0xC5

    def set_led_scaling(self, scale):
        scalebuf = [scale] * 181
        scalebuf[0] = 0
        self.page = 2
        with self.i2c_device as i2c:
            i2c.write(bytes(scalebuf))
        self.page = 3
        with self.i2c_device as i2c:
            i2c.write(bytes(scalebuf))

    @property
    def global_current(self):
        self.page = 4
        return self._gcurrent_reg

    @global_current.setter
    def global_current(self, gc):
        self.page = 4
        self._gcurrent_reg = gc
        

    @property
    def enable(self):
        self.page = 4
        return self._shutdown_bit

    @enable.setter
    def enable(self, en):
        self.page = 4
        self._shutdown_bit = en
        
    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, p):
        if p == self._page:
            return  # already set
        if p > 4:
            raise ValueError("Page must be 0 ~ 4")
        self._page = p  # cache
        self.unlock()
        self._page_reg = p



    def __getitem__(self, key):
        print(key)

    def __setitem__(self, led, pwm):
        if not 0 <= led <= 350:
            raise ValueError("LED must be 0 ~ 350")
        if not 0 <= pwm <= 255:
            raise ValueError("PWM must be 0 ~ 255")
        print(led, pwm)
        
        if led < 180:
            self.page = 0
            self._buf[0] = led
        else:
            self.page = 1
            self._buf[0] = led - 180
        self._buf[1] = pwm
        with self.i2c_device as i2c:
            i2c.write(self._buf)
            
            



    # This function must be replaced for each board
    @staticmethod
    def pixel_addr(x, y):
        """Calulate the offset into the device array for x,y pixel"""
        return x + y * 16

    # pylint: disable-msg=too-many-arguments
    def pixel(self, x, y, color=None):
        """
        Color of for x-, y-pixel

        :param x: horizontal pixel position
        :param y: vertical pixel position
        :param color: hex color value 0x000000 to 0xFFFFFF
        """
        if not 0 <= x <= self.width:
            return None
        if not 0 <= y <= self.height:
            return None
        pixel = self.pixel_addr(x, y)
        if color is None and blink is None:
            return self._register(self._frame, pixel)
        if frame is None:
            frame = self._frame
        if color is not None:
            if not 0 <= color <= 255:
                raise ValueError("Color out of range")
            self._register(frame, _COLOR_OFFSET + pixel, color)
        if blink is not None:
            addr, bit = divmod(pixel, 8)
            bits = self._register(frame, _BLINK_OFFSET + addr)
            if blink:
                bits |= 1 << bit
            else:
                bits &= ~(1 << bit)
            self._register(frame, _BLINK_OFFSET + addr, bits)
        return None

    # pylint: enable-msg=too-many-arguments

    def image(self, img, blink=None, frame=None):
        """Set buffer to value of Python Imaging Library image.  The image should
        be in 8-bit mode (L) and a size equal to the display size.

        :param img: Python Imaging Library image
        :param blink: True to blink
        :param frame: the frame to set the image
        """
        if img.mode != "L":
            raise ValueError("Image must be in mode L.")
        imwidth, imheight = img.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError(
                "Image must be same dimensions as display ({0}x{1}).".format(
                    self.width, self.height
                )
            )
        # Grab all the pixels from the image, faster than getpixel.
        pixels = img.load()

        # Iterate through the pixels
        for x in range(self.width):  # yes this double loop is slow,
            for y in range(self.height):  #  but these displays are small!
                self.pixel(x, y, pixels[(x, y)], blink=blink, frame=frame)
