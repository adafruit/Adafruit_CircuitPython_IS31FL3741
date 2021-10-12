# SPDX-FileCopyrightText: 2021 Rose Hooper
# SPDX-License-Identifier: MIT
"""
LED Animation compatibility layer.
"""
import array


def _int_as_tuple(value):
    if isinstance(value, int):
        return value >> 16 & 0xFF, value >> 8 & 0xFF, value & 0xFF
    return value


def _setup_pixels(grid, led_glasses, left, left_start, right, right_start):
    # pylint: disable=too-many-locals, too-many-arguments
    left_right_size = 24
    order = [
        (left, "l", led_glasses.left_ring),
        (right, "r", led_glasses.right_ring),
        (grid, "g", led_glasses.grid),
    ]
    order.sort()
    sequence = []
    for _, strip_type, strip in sorted(order):
        if strip_type == "g":
            for y in range(strip.height):
                for x in range(strip.width):
                    sequence.extend(strip.pixel_addrs(x, y))
        else:
            start = left_start if strip_type == "l" else right_start
            for pixel_no in range(left_right_size):
                sequence.extend(strip.pixel_addrs((pixel_no + start) % left_right_size))
    return sequence


class LED_Glasses_Animation:
    """
    Library that wraps the LED Glasses with neo-pixel like behaviour so that Adafruit LED Animation
    can work.
    """

    _brightness = 1
    _auto_write = True

    def __init__(
        self,
        led_glasses,
        left=1,
        grid=2,
        right=3,
        auto_write=True,
        brightness=1,
        left_start=21,
        right_start=8,
    ):
        # pylint: disable=too-many-arguments
        self._glasses = led_glasses

        # improvements:
        # Over, Under, Overlap, Not.
        # Left Start, Right Start, Grid Order

        sequence = _setup_pixels(
            grid, led_glasses, left, left_start, right, right_start
        )

        self.brightness = brightness
        self.auto_write = auto_write
        self._map = array.array("H", sequence)
        self.n = len(self._map) // 3

    def __len__(self):
        return self.n

    @property
    def brightness(self):
        """Get or set brightness."""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._glasses.set_led_scaling(255 * value)
        self._brightness = value

    @property
    def auto_write(self):
        """Enable/disable auto-write"""
        return self._auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._auto_write = value

    def show(self):
        """Show pixels."""
        self._glasses.show()

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self._get_pixel(idx) for idx in self._range_for_slice(key)]
        return self._get_pixel(key)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            for idx, val in zip(self._range_for_slice(key), value):
                r, g, b = self._map_pixel(idx)
                self._glasses[r], self._glasses[g], self._glasses[b] = _int_as_tuple(
                    val
                )
                return
        r, g, b = self._map_pixel(key)
        self._glasses[r], self._glasses[g], self._glasses[b] = _int_as_tuple(value)
        if self.auto_write:
            self.show()

    def _map_pixel(self, key):
        return self._map[key * 3 : key * 3 + 3]

    def fill(self, value):
        """Set all pixels to `value`."""
        for n in range(self.n):
            self[n] = value
        if self.auto_write:
            self.show()

    def _range_for_slice(self, key):
        return range(key.start or 0, key.stop or len(self), key.step or 1)

    def _get_pixel(self, key):
        r, g, b = self._map_pixel(key)
        return self._glasses[r], self._glasses[g], self._glasses[b]
