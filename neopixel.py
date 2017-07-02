# NeoPixel driver for MicroPython on ESP8266
# MIT license; Copyright (c) 2016 Damien P. George

import digitalio
from neopixel_write import neopixel_write

class NeoPixel:
    ORDER = (1, 0, 2, 3)
    def __init__(self, pin, n, bpp=3, brightness=1.0):
        self.pin = digitalio.DigitalInOut(pin)
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.switch_to_output()
        self.brightness = brightness

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

    def __len__(self):
        return self.n

    def set_brightness(self, range):
        if (range > 1.0):
            self.brightness = 1.0
        elif (range < 0):
            self.brightness = 0.0
        else:
            self.brightness = range

    def fill(self, color):
        for i in range(self.n):
            self[i] = color

    def write(self):
        neopixel_write(self.pin, bytearray([int(i * self.brightness) for i in self.buf]))
