import time
import board
import neopixel


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL

# The number of NeoPixels
num_pixels = 10

# The number of colors in each pixel: 3 for RGB, 4 for RGBW (RGB plus white)
BPP = 3

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, bpp=BPP, brightness=0.3, auto_write=False)


def format_tuple(r, g, b):
    if BPP == 3:
        return r, g, b
    return r, g, b, 0


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return format_tuple(0, 0, 0)
    if pos < 85:
        return format_tuple(int(pos * 3), int(255 - (pos*3)), 0)
    if pos < 170:
        pos -= 85
        return format_tuple(int(255 - pos*3), 0, int(pos*3))
    pos -= 170
    return format_tuple(0, int(pos*3), int(255 - pos*3))


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    pixels.fill(format_tuple(255, 0, 0))
    pixels.show()
    time.sleep(1)

    pixels.fill(format_tuple(0, 255, 0))
    pixels.show()
    time.sleep(1)

    pixels.fill(format_tuple(0, 0, 255))
    pixels.show()
    time.sleep(1)

    rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step
