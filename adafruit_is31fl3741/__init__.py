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

from sys import implementation
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bit import RWBit

try:
    # Used only for typing
    from typing import Optional, Tuple, Union  # pylint: disable=unused-import
    from PIL.ImageFile import ImageFile
    from adafruit_framebuf import FrameBuffer
    import busio
except ImportError:
    pass

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
    The IS31FL3741 is an abstract class containing the main function related
    to this chip. It focuses on lowest-level I2C operations and chip
    registers, and has no concept of a 2D graphics coordinate system, nor of
    RGB colors (subclasses provide these). It is linear and monochromatic.

    :param ~adafruit_bus_device.i2c_device i2c_device: the connected i2c bus
           i2c_device
    :param address: the device address; defaults to 0x30
    :param allocate: buffer allocation strategy: NO_BUFFER = pixels are always
                     sent to device as they're set. PREFER_BUFFER = RAM
                     permitting, buffer pixels in RAM, updating device only
                     when show() is called, but fall back on NO_BUFFER
                     behavior. MUST_BUFFER = buffer pixels in RAM, throw
                     MemoryError if allocation fails.
    """

    _page_reg = UnaryStruct(_IS3741_COMMANDREGISTER, "<B")
    _lock_reg = UnaryStruct(_IS3741_COMMANDREGISTERLOCK, "<B")
    _id_reg = UnaryStruct(_IS3741_IDREGISTER, "<B")
    _config_reg = UnaryStruct(_IS3741_FUNCREG_CONFIG, "<B")
    _gcurrent_reg = UnaryStruct(_IS3741_FUNCREG_GCURRENT, "<B")
    _reset_reg = UnaryStruct(_IS3741_FUNCREG_RESET, "<B")
    _shutdown_bit = RWBit(_IS3741_FUNCREG_CONFIG, 0)
    _pixel_buffer = None

    def __init__(
        self,
        i2c: busio.I2C,
        address: int = _IS3741_ADDR_DEFAULT,
        allocate: int = NO_BUFFER,
    ):
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

    def reset(self) -> None:
        """Reset"""
        self.page = 4
        self._reset_reg = 0xAE

    def unlock(self) -> None:
        """Unlock"""
        self._lock_reg = 0xC5

    def set_led_scaling(self, scale: int) -> None:
        """Set scaling level for all LEDs.

        :param scale: Scaling level from 0 (off) to 255 (brightest).
        """
        scalebuf = bytearray([scale] * 181)  # 180 bytes + 1 for reg addr
        scalebuf[0] = 0  # Initial register address
        self.page = 2
        with self.i2c_device as i2c:
            i2c.write(scalebuf)
        self.page = 3
        with self.i2c_device as i2c:
            i2c.write(scalebuf, end=172)  # 2nd page is smaller

    @property
    def global_current(self) -> int:
        """Global current"""
        self.page = 4
        return self._gcurrent_reg

    @global_current.setter
    def global_current(self, current: int) -> None:
        self.page = 4
        self._gcurrent_reg = current

    @property
    def enable(self) -> bool:
        """Enable"""
        self.page = 4
        return self._shutdown_bit

    @enable.setter
    def enable(self, enable: bool) -> None:
        self.page = 4
        self._shutdown_bit = enable

    @property
    def page(self) -> Union[int, None]:
        """Page"""
        return self._page

    @page.setter
    def page(self, page_value: int) -> None:
        if page_value == self._page:
            return  # already set
        if page_value > 4:
            raise ValueError("Page must be 0 ~ 4")
        self._page = page_value  # cache
        self.unlock()
        self._page_reg = page_value

    def __getitem__(self, led: int) -> int:
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

    def __setitem__(self, led: int, pwm: int) -> None:
        if self._pixel_buffer:
            # Buffered version doesn't require range checks --
            # Python will throw its own IndexError/ValueError as needed.
            self._pixel_buffer[1 + led] = pwm
        elif 0 <= led <= 350:
            if 0 <= pwm <= 255:
                # print(led, pwm)
                if led < 180:
                    self.page = 0
                    self._buf[0] = led
                else:
                    self.page = 1
                    self._buf[0] = led - 180
                self._buf[1] = pwm
                with self.i2c_device as i2c:
                    i2c.write(self._buf)
            else:
                raise ValueError("PWM must be 0 ~ 255")
        else:
            raise ValueError("LED must be 0 ~ 350")

    def show(self) -> None:
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


IS3741_RGB = (0 << 4) | (1 << 2) | (2)  # Encode as R,G,B
IS3741_RBG = (0 << 4) | (2 << 2) | (1)  # Encode as R,B,G
IS3741_GRB = (1 << 4) | (0 << 2) | (2)  # Encode as G,R,B
IS3741_GBR = (2 << 4) | (0 << 2) | (1)  # Encode as G,B,R
IS3741_BRG = (1 << 4) | (2 << 2) | (0)  # Encode as B,R,G
IS3741_BGR = (2 << 4) | (1 << 2) | (0)  # Encode as B,G,R


class IS31FL3741_colorXY(IS31FL3741):
    """
    Class encompassing IS31FL3741 and a minimal layer for RGB color 2D
    pixel operations (base class is hardware- and register-centric and
    lacks these concepts). Specific boards like the QT matrix or EyeLights
    glasses then subclass this. In theory, a companion monochrome XY class
    could be separately implemented in the future if required for anything.
    Mostly though, this is about providing a place for common RGB matrix
    functions like fill() that then work across all such devices.

    :param ~adafruit_bus_device.i2c_device i2c_device: the connected i2c bus
           i2c_device
    :param width:    Matrix width in pixels.
    :param height:   Matrix height in pixels.
    :param address: the device address; defaults to 0x30
    :param allocate: buffer allocation strategy: NO_BUFFER = pixels are always
                     sent to device as they're set. PREFER_BUFFER = RAM
                     permitting, buffer pixels in RAM, updating device only
                     when show() is called, but fall back on NO_BUFFER
                     behavior. MUST_BUFFER = buffer pixels in RAM, throw
                     MemoryError if allocation fails.
    :param order:    Pixel RGB color order, one of the IS3741_* color types
                     above. Default is IS3741_BGR.
    """

    # pylint: disable-msg=too-many-arguments
    def __init__(
        self,
        i2c: busio.I2C,
        width: int,
        height: int,
        address: int = _IS3741_ADDR_DEFAULT,
        allocate: int = NO_BUFFER,
        order: int = IS3741_BGR,
    ):
        super().__init__(i2c, address=address, allocate=allocate)
        self.order = order
        self.width = width
        self.height = height
        self.r_offset = (order >> 4) & 3
        self.g_offset = (order >> 2) & 3
        self.b_offset = order & 3

    # pylint: enable-msg=too-many-arguments

    # This function must be replaced for each board
    @staticmethod
    def pixel_addrs(x: int, y: int) -> Tuple[int, ...]:
        """Calculate a device-specific LED offset for an X,Y 2D pixel."""
        raise NotImplementedError("Supported in subclasses only")

    def fill(self, color: int = 0) -> None:
        """Set all pixels to a given RGB color.

        :param color: Packed 24-bit color value (0xRRGGBB).
        """
        red = (color >> 16) & 0xFF
        green = (color >> 8) & 0xFF
        blue = color & 0xFF
        for y in range(self.height):
            for x in range(self.width):
                addrs = self.pixel_addrs(x, y)
                self[addrs[self.r_offset]] = red
                self[addrs[self.g_offset]] = green
                self[addrs[self.b_offset]] = blue

    def pixel(self, x: int, y: int, color: Optional[int] = None) -> Union[int, None]:
        """
        Set or retrieve RGB color of pixel at position (X,Y).

        :param x:     Horizontal pixel position.
        :param y:     Vertical pixel position.
        :param color: If setting, a packed 24-bit color value (0xRRGGBB).
                      If getting, either None or leave off this argument.
        :returns:     If setting, returns None. If getting, returns a packed
                      24-bit color value (0xRRGGBB).
        """

        if 0 <= x < self.width and 0 <= y < self.height:  # Clip
            addrs = self.pixel_addrs(x, y)  # LED indices
            # print(addrs)
            if color is not None:
                self[addrs[self.r_offset]] = (color >> 16) & 0xFF
                self[addrs[self.g_offset]] = (color >> 8) & 0xFF
                self[addrs[self.b_offset]] = color & 0xFF
            else:  # Return current pixel color if unspecified
                return (
                    (self[addrs[self.r_offset]] << 16)
                    | (self[addrs[self.g_offset]] << 8)
                    | self[addrs[self.b_offset]]
                )
        return None

    def image(self, img: Union[FrameBuffer, ImageFile]) -> None:
        """Copy an in-memory image to the LED matrix. Image should be in
        24-bit format (e.g. "RGB888") and dimensions should match matrix,
        this isn't super robust yet or anything.

        :param img: Source image -- either a FrameBuffer object if running
                    CircuitPython, or PIL image if running CPython w/Python
                    Imaging Lib.
        """
        if implementation.name == "circuitpython":
            for y in range(self.height):
                for x in range(self.width):
                    self.pixel(x, y, img.pixel(x, y))
        else:
            if img.mode != "RGB":
                raise ValueError("Image must be in mode RGB.")
            if img.size[0] != self.width or img.size[1] != self.height:
                raise ValueError(
                    "Image must be same dimensions as display ({0}x{1}).".format(
                        self.width, self.height
                    )
                )

            # Iterate X/Y through all image pixels
            pixels = img.load()  # Grab all pixels, faster than getpixel on each
            for y in range(self.height):
                for x in range(self.width):
                    self.pixel(x, y, pixels[(x, y)])

    def __len__(self):
        return self.width * self.height * 3
