# NeoPixel driver for MicroPython on ESP8266
# MIT license; Copyright (c) 2016 Damien P. George

import nativeio
from neopixel_write import neopixel_write

class NeoPixel:
    ORDER = (1, 0, 2, 3)
    def __init__(self, pin, n, bpp=3):
        self.pin = nativeio.DigitalInOut(pin)
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.switch_to_output()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.pin.deinit()

    def __setitem__(self, index, val):
        offset = index * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = val[i]

    def __getitem__(self, index):
        offset = index * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]]
                     for i in range(self.bpp))

    def fill(self, color):
        for i in range(self.n):
            self[i] = color

    def write(self):
        neopixel_write(self.pin, self.buf, True)
