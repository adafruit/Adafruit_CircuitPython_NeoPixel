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

import math

import digitalio
from neopixel_write import neopixel_write
from pixelbuf import PixelBuf


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel.git"

# Pixel color order constants
RGB = PixelBuf.RGB
"""Red Green Blue"""
GRB = PixelBuf.GRB
"""Green Red Blue"""
RGBW = PixelBuf.RGB
"""Red Green Blue White"""
GRBW = PixelBuf.GRB
"""Green Red Blue White"""

class NeoPixel:
    """
    A sequence of neopixels.

    :param ~microcontroller.Pin pin: The pin to output neopixel data on.
    :param int n: The number of neopixels in the chain
    :param int bpp: Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0 where 1.0 is full
      brightness
    :param bool auto_write: True if the neopixels should immediately change when set. If False,
      `show` must be called explicitly.
    :param tuple pixel_order: Set the pixel color channel order. GRBW is set by default.

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

        # Using ``with`` ensures pixels are cleared after we're done.
        with neopixel.NeoPixel(NEOPIXEL, 10) as pixels:
            pixels[::2] = [RED] * (len(pixels) // 2)
            time.sleep(2)
    """
    def __init__(self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.n = n
        self.auto_write = auto_write
        self.bpp = bpp
        self.buf = PixelBuf(self.n, bytearray(self.n * bpp), 
                            bpp=self.bpp, brightness=brightness,
                            rawbuf=bytearray(self.n * bpp),
                            byteorder=pixel_order or PixelBuf.BGR)

    def deinit(self):
        """Blank out the NeoPixels and release the pin."""
        for i in range(len(self.buf)):
            self.buf[i] = 0
        neopixel_write(self.pin, self.buf.buf)
        self.pin.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            self.buf[index.start:index.stop:index.step] = val
        else:
            self.buf[index] = val

        if self.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.buf[index.start:index.stop:index.step]
        else:
            return self.buf[index]

    def __len__(self):
        return len(self.buf) // self.bpp

    @property
    def brightness(self):
        """Overall brightness of the pixel"""
        return self.buf.brightness

    @brightness.setter
    def brightness(self, brightness):
        # pylint: disable=attribute-defined-outside-init
        self.buf.brightness = brightness
        if self.auto_write:
            self.show()

    def fill(self, color):
        """Colors all pixels the given ***color***."""
        auto_write = self.auto_write
        self.auto_write = False
        for i, _ in enumerate(self):
            self[i] = color
        if auto_write:
            self.show()
        self.auto_write = auto_write

    def write(self):
        """.. deprecated: 1.0.0

             Use ``show`` instead. It matches Micro:Bit and Arduino APIs."""
        self.show()

    def show(self):
        """Shows the new colors on the pixels themselves if they haven't already
        been autowritten.

        The colors may or may not be showing after this function returns because
        it may be done asynchronously."""
        neopixel_write(self.pin, self.buf.buf)
