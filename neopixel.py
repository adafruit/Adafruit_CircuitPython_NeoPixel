# The MIT License (MIT)
#
# Copyright (c) 2016 Damien P. George
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`neopixel` - NeoPixel strip driver
====================================================

* Author(s): Damien P. George & Scott Shawcroft
"""

import digitalio
import math
from neopixel_write import neopixel_write

class NeoPixel:
    """
    A sequence of neopixels.

    :param ~microcontroller.Pin pin: The pin to output neopixel data on.
    :param int n: The number of neopixels in the chain
    :param int bpp: Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0 where 1.0 is full brightness
    :param bool auto_write: True if the neopixels should immediately change when set. If False, `show` must be called explicitly.

    Example for Circuit Playground Express:

    .. code-block:: python

        import neopixel
        from board import *

        RED = 0x100000 # (0x10, 0, 0) also works

        pixels = neopixel.NeoPixel(NEOPIXEL, 10)
        for i in range(len(pixels)):
            pixels[i] = RED

    Example for Circuit Playground Express setting every other pixel red using a slice:

    .. code-block:: python

        import neopixel
        from board import *
        import time

        RED = 0x100000 # (0x10, 0, 0) also works

        # Using `with` ensures pixels are cleared after we're done.
        with neopixel.NeoPixel(NEOPIXEL, 10) as pixels:
            pixels[::2] = [RED] * (len(pixels) // 2)
            time.sleep(2)
    """
    ORDER = (1, 0, 2, 3)
    def __init__(self, pin, n, bpp=3, brightness=1.0, auto_write=True):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.brightness = brightness
        self.auto_write = auto_write

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # Blank out the neopixels.
        for i in range(len(self.buf)):
            self.buf[i] = 0
        neopixel_write(self.pin, self.buf)
        self.pin.deinit()

    def __repr__(self):
        return "[" + ", ".join(["0x%06x" % (x,) for x in self]) + "]"

    def _set_item(self, index, value):
        offset = index * self.bpp
        r = 0
        g = 0
        b = 0
        w = 0
        if type(value) == tuple and len(value) == self.bpp:
            if self.bpp == 3:
                r, g, b = value
            else:
                r, g, b, w = value
        elif type(value) == int:
            r = value >> 16
            g = (value >> 8) & 0xff
            b = value & 0xff
            w = 0
            # If all components are the same and we have a white pixel then use it
            # instead of the individual components.
            if self.bpp == 4 and r == g and g == b:
                w = r
                r = 0
                g = 0
                b = 0
        self.buf[offset + self.ORDER[0]] = r
        self.buf[offset + self.ORDER[1]] = g
        self.buf[offset + self.ORDER[2]] = b
        if self.bpp == 4:
            self.buf[offset + self.ORDER[3]] = w

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self.buf) // self.bpp)
            length = stop - start
            if step != 0:
                length = math.ceil(length / step)
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_item(in_i, val[val_i])
        else:
            self._set_item(index, val)

        if self.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            out = []
            for in_i in range(*index.indices(len(self.buf) // self.bpp)):
                out.append(self[in_i])
            return out
        offset = index * self.bpp
        if self.bpp == 4:
            w = self.buf[offset + 3]
            if w != 0:
                return w << 16 | w << 8 | w
        return self.buf[offset + 1] << 16 | self.buf[offset] << 8 | self.buf[offset + 2]

    def __len__(self):
        return len(self.buf) // self.bpp

    def __len__(self):
        return self.n

    @property
    def brightness(self):
        """Overall brightness of the pixel"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = min(max(brightness, 0.0), 1.0)

    def fill(self, color):
        """Colors all pixels the given ***color***."""
        auto_write = self.auto_write
        self.auto_write = False
        for i in range(len(self)):
            self[i] = color
        if auto_write:
            self.show()
        self.auto_write = auto_write

    def write(self):
        """.. deprecated: 1.0.0

             Use `show` instead. It matches Micro:Bit and Arduino APIs."""
        self.show()

    def show(self):
        """Shows the new colors on the pixels themselves if they haven't already
        been autowritten.

        The colors may or may not be showing after this function returns because
        it may be done asynchronously."""
        if self.brightness > 0.99:
            neopixel_write(self.pin, self.buf)
        else:
            neopixel_write(self.pin, bytearray([int(i * self.brightness) for i in self.buf]))
