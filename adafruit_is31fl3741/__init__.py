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

from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bit import RWBit

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

# Buffer allocation behaviors passed to constructor
NO_BUFFER = 0x00  # DO NOT buffer pixel data, write pixels as needed
PREFER_BUFFER = 0x01  # OPTIONALLY buffer pixel data, RAM permitting
MUST_BUFFER = 0x02  # MUST buffer pixel data, else throw MemoryError


class IS31FL3741:
    """
    The IS31FL3741 is an abstract class contain the main function related to this chip.
    Each board needs to define width, height and pixel_addr.

    :param ~adafruit_bus_device.i2c_device i2c_device: the connected i2c bus i2c_device
    :param address: the device address; defaults to 0x30
    :param allocate: buffer allocation strategy: NO_BUFFER = pixels are always
                     sent to device as they're set. PREFER_BUFFER = RAM
                     permitting, buffer pixels in RAM, updating device only
                     when show() is called, but fall back on NO_BUFFER
                     behavior. MUST_BUFFER = buffer pixels in RAM, throw
                     MemoryError if allocation fails.
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
    _pixel_buffer = None

    def __init__(self, i2c, address=_IS3741_ADDR_DEFAULT, allocate=NO_BUFFER):
        if allocate >= PREFER_BUFFER:
            try:
                # Pixel buffer intentionally has an extra item at the start
                # (value of 0) so we can i2c.write() from the buffer directly
                # (don't need a temp/copy buffer to pre-pend the register
                # address).
                self._pixel_buffer = bytearray(352)
            except MemoryError:
                if allocate == MUST_BUFFER:
                    raise
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        if self._id_reg != 2 * address:
            raise AttributeError("Cannot find a IS31FL3741 at address 0x", address)
        self._buf = bytearray(2)
        self._page = None
        self.reset()

    def reset(self):
        """Reset"""
        self.page = 4
        self._reset_reg = 0xAE

    def unlock(self):
        """Unlock"""
        self._lock_reg = 0xC5

    def set_led_scaling(self, scale):
        """Set LED scaling.

        param scale: The scale.
        """
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
        """Global current"""
        self.page = 4
        return self._gcurrent_reg

    @global_current.setter
    def global_current(self, current):
        self.page = 4
        self._gcurrent_reg = current

    @property
    def enable(self):
        """Enable"""
        self.page = 4
        return self._shutdown_bit

    @enable.setter
    def enable(self, enable):
        self.page = 4
        self._shutdown_bit = enable

    @property
    def page(self):
        """Page"""
        return self._page

    @page.setter
    def page(self, page_value):
        if page_value == self._page:
            return  # already set
        if page_value > 4:
            raise ValueError("Page must be 0 ~ 4")
        self._page = page_value  # cache
        self.unlock()
        self._page_reg = page_value

    def __getitem__(self, led):
        if not 0 <= led <= 350:
            raise ValueError("LED must be 0 ~ 350")
        if self._pixel_buffer:
            return self._pixel_buffer[1 + led]
        if led < 180:
            self.page = 0
            self._buf[0] = led
        else:
            self.page = 1
            self._buf[0] = led - 180

        with self.i2c_device as i2c:
            i2c.write_then_readinto(
                self._buf, self._buf, out_start=0, out_end=1, in_start=1, in_end=2
            )
        return self._buf[1]

    def __setitem__(self, led, pwm):
        if not 0 <= led <= 350:
            raise ValueError("LED must be 0 ~ 350")
        if not 0 <= pwm <= 255:
            raise ValueError("PWM must be 0 ~ 255")
        # print(led, pwm)
        if self._pixel_buffer:
            self._pixel_buffer[1 + led] = pwm
        else:
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
    def pixel_addrs(x, y):
        """Calulate the offset into the device array for x,y pixel"""
        raise NotImplementedError("Supported in subclasses only")

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
        addrs = self.pixel_addrs(x, y)
        # print(addrs)
        if color is not None:  # set the color
            self[addrs[0]] = (color >> 16) & 0xFF
            self[addrs[1]] = (color >> 8) & 0xFF
            self[addrs[2]] = color & 0xFF
            return None
        # we want to fetch the color
        color = self[addrs[0]]
        color <<= 8
        color |= self[addrs[1]]
        color <<= 8
        color |= self[addrs[2]]
        return color

    # pylint: enable-msg=too-many-arguments

    def image(self, img):
        """Set buffer to value of Python Imaging Library image.  The image should
        be in 8-bit mode (L) and a size equal to the display size.

        :param img: Python Imaging Library image
        """
        if img.mode != "RGB":
            raise ValueError("Image must be in mode RGB.")
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
                self.pixel(x, y, pixels[(x, y)])

    def show(self):
        """Issue in-RAM pixel data to device. No effect if pixels are
        unbuffered.
        """
        if self._pixel_buffer:
            self.page = 0
            with self.i2c_device as i2c:
                # _pixel_buffer[0] is always 0! (First register addr)
                i2c.write(self._pixel_buffer, start=0, end=181)
            self.page = 1
            with self.i2c_device as i2c:
                # In order to write from pixel buffer directly (without a
                # whole extra temp buffer), element 180 is saved in a temp var
                # and replaced with 0 (representing the first regisyer addr on
                # page 1), then we can i2c.write() directly from that position
                # in the buffer. Element 180 is restored afterward. This is
                # the same strategy as used in the Arduino library.
                # 'end' below is 352 (not 351) because of the extra byte at
                # the start of the pixel buffer.
                save = self._pixel_buffer[180]
                self._pixel_buffer[180] = 0
                i2c.write(self._pixel_buffer, start=180, end=352)
                self._pixel_buffer[180] = save
