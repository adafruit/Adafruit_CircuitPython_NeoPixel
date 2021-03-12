import time
import board
from neopixelhsv import NeoPixelHSV

# On a Raspberry pi, use this instead, not all pins are supported
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 10

pixels = NeoPixelHSV(
    pixel_pin, num_pixels, brightness=1, auto_write=True
)

for i in range(0, 360, 1):
    pixels[9] = ((i, 100, 100))
    time.sleep(0.01)
