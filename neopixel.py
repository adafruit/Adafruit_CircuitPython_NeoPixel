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

try:
    # imports needed for main NeoPixel class
    import digitalio
    from neopixel_write import neopixel_write
except NotImplementedError:
    # silently accept this, can still use NeoPixel SPI class
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel.git"

# Pixel color order constants
RGB = (0, 1, 2)
"""Red Green Blue"""
GRB = (1, 0, 2)
"""Green Red Blue"""
RGBW = (0, 1, 2, 3)
"""Red Green Blue White"""
GRBW = (1, 0, 2, 3)
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
        if pixel_order is None:
            self.order = GRBW
            self.bpp = bpp
        else:
            self.order = pixel_order
            self.bpp = len(self.order)
        self.buf = bytearray(self.n * self.bpp)
        # Set auto_write to False temporarily so brightness setter does _not_
        # call show() while in __init__.
        self.auto_write = False
        self.brightness = brightness
        self.auto_write = auto_write

    def deinit(self):
        """Blank out the NeoPixels and release the pin."""
        for i in range(len(self.buf)):
            self.buf[i] = 0
        neopixel_write(self.pin, self.buf)
        self.pin.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def _set_item(self, index, value):
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        offset = index * self.bpp
        r = 0
        g = 0
        b = 0
        w = 0
        if isinstance(value, int):
            if value>>24:
                raise ValueError("only bits 0->23 valid for integer input")
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
        elif (len(value) == self.bpp) or ((len(value) == 3) and (self.bpp == 4)):
            if len(value) == 3:
                r, g, b = value
            else:
                r, g, b, w = value
        else:
            raise ValueError("Color tuple size does not match pixel_order.")

        self.buf[offset + self.order[0]] = r
        self.buf[offset + self.order[1]] = g
        self.buf[offset + self.order[2]] = b
        if self.bpp == 4:
            self.buf[offset + self.order[3]] = w

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
                out.append(tuple(self.buf[in_i * self.bpp + self.order[i]]
                                 for i in range(self.bpp)))
            return out
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        offset = index * self.bpp
        return tuple(self.buf[offset + self.order[i]]
                     for i in range(self.bpp))

    def __len__(self):
        return len(self.buf) // self.bpp

    @property
    def brightness(self):
        """Overall brightness of the pixel"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        # pylint: disable=attribute-defined-outside-init
        self._brightness = min(max(brightness, 0.0), 1.0)
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
        if self.brightness > 0.99:
            neopixel_write(self.pin, self.buf)
        else:
            neopixel_write(self.pin, bytearray([int(i * self.brightness) for i in self.buf]))

class NeoPixel_SPI(NeoPixel):
    """
    A sequence of neopixels.

    :param ~busio.SPI spi: The SPI bus to output neopixel data on.
    :param int n: The number of neopixels in the chain
    :param int bpp: Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0 where 1.0 is full
      brightness
    :param bool auto_write: True if the neopixels should immediately change when set. If False,
      `show` must be called explicitly.
    :param tuple pixel_order: Set the pixel color channel order. GRBW is set by default.

    Example:

    .. code-block:: python

        import board
        import neopixel

        pixels = neopixel.NeoPixel_SPI(board.SPI(), 10)
        pixels.fill(0xff0000)
    """
    #pylint: disable=invalid-name, super-init-not-called

    FREQ = 6400000  # 800kHz * 8, actual may be different
    TRST = 80e-6    # Reset code low level time

    def __init__(self, spi, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        from adafruit_bus_device.spi_device import SPIDevice
        self._spi = SPIDevice(spi, baudrate=self.FREQ)
        with self._spi as spibus:
            try:
                # get actual SPI frequency
                freq = spibus.frequency
            except AttributeError:
                # use nominal
                freq = self.FREQ
        self.RESET = bytes([0]*round(freq*self.TRST))
        self.n = n
        if pixel_order is None:
            self.order = GRBW
            self.bpp = bpp
        else:
            self.order = pixel_order
            self.bpp = len(self.order)
        self.buf = bytearray(self.n * self.bpp)
        self.spibuf = bytearray(8*len(self.buf))
        # Set auto_write to False temporarily so brightness setter does _not_
        # call show() while in __init__.
        self.auto_write = False
        self.brightness = brightness
        self.auto_write = auto_write

    def deinit(self):
        """Blank out the NeoPixels."""
        for i in range(len(self.buf)):
            self.buf[i] = 0
        self.show()

    def show(self):
        """Shows the new colors on the pixels themselves if they haven't already
        been autowritten."""
        self._transmogrify()
        with self._spi as spi:
            # write out special byte sequence surrounded by RESET
            # leading RESET needed for cases where MOSI rests HI
            spi.write(self.RESET + self.spibuf + self.RESET)

    def _transmogrify(self):
        """Turn every BIT of buf into a special BYTE pattern."""
        k = 0
        for byte in self.buf:
            byte = int(byte * self.brightness)
            # MSB first
            for i in range(7, -1, -1):
                if byte >> i & 0x01:
                    self.spibuf[k] = 0b11110000 # A NeoPixel 1 bit
                else:
                    self.spibuf[k] = 0b11000000 # A NeoPixel 0 bit
                k += 1
