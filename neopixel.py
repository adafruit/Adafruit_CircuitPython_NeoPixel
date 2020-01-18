# The MIT License (MIT)
#
# Copyright (c) 2016 Damien P. George
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2019 Carter Nelson
# Copyright (c) 2019 Roy Hooper
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

* Author(s): Damien P. George, Scott Shawcroft, Carter Nelson, Roy Hooper
"""

import digitalio
from neopixel_write import neopixel_write
try:
    import _pixelbuf
except ImportError:
    import adafruit_pypixelbuf as _pixelbuf


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel.git"


# Pixel color order constants
RGB = 'RGB'
"""Red Green Blue"""
GRB = 'GRB'
"""Green Red Blue"""
RGBW = 'RGBW'
"""Red Green Blue White"""
GRBW = 'GRBW'
"""Green Red Blue White"""


class NeoPixel(_pixelbuf.PixelBuf):
    """
    A sequence of neopixels.

    :param ~microcontroller.Pin pin: The pin to output neopixel data on.
    :param int n: The number of neopixels in the chain
    :param int bpp: Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0 where 1.0 is full
      brightness
    :param bool auto_write: True if the neopixels should immediately change when set. If False,
      `show` must be called explicitly.
    :param str: Set the pixel color channel order. GRBW is set by default.

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
    bpp = None
    n = 0

    def __init__(self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        self.bpp = bpp
        self.n = n

        if not pixel_order:
            pixel_order = GRB if bpp == 3 else GRBW
        else:
            self.bpp = bpp = len(pixel_order)
            if isinstance(pixel_order, tuple):
                order_chars = RGBW
                order = []
                for char_no, order in enumerate(pixel_order):
                    order[pixel_order] = order_chars[char_no]
                pixel_order = ''.join(order)

        self._buf = bytearray(self.n * bpp)
        self._rawbuf = bytearray(self.n * bpp)
        super().__init__(n, self._buf,
                         brightness=brightness,
                         rawbuf=self._rawbuf,
                         byteorder=pixel_order,
                         auto_write=auto_write)

        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT

    def deinit(self):
        """Blank out the NeoPixels and release the pin."""
        self.fill(0)
        self.show()
        self.pin.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def write(self):
        """.. deprecated: 1.0.0

             Use ``show`` instead. It matches Micro:Bit and Arduino APIs."""
        self.show()

    def show(self):
        """Shows the new colors on the pixels themselves if they haven't already
        been autowritten.

        The colors may or may not be showing after this function returns because
        it may be done asynchronously."""
        neopixel_write(self.pin, self._buf)

    def fill(self, color):
        """Colors all pixels the given ***color***."""
        _pixelbuf.fill(self, color)

    @property
    def buf(self):
        """
        Get or set the unadjusted buffer.
        """
        return self._rawbuf

    @buf.setter
    def buf(self, value):
        """
        Update the unadjusted buffer.
        """
        self._rawbuf[:] = value[:]
        self.brightness = self.brightness  # pylint: disable=attribute-defined-outside-init
