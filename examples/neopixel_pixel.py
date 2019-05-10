# This example shows how to create a single pixel with a specific color channel
# order and blink it.
# Most NeoPixels = neopixel.GRB or neopixel.GRBW
# The 8mm Diffused NeoPixel (PID 1734) = neopixel.RGB
import time
import board
import neopixel

# Configure the setup
PIXEL_PIN = board.D1   # pin that the NeoPixel is connected to
ORDER = neopixel.RGB   # pixel color channel order
COLOR = (100, 50, 150) # color to blink
CLEAR = (0, 0, 0)      # clear (or second color)
DELAY = 0.25           # blink rate in seconds

# Create the NeoPixel object
pixel = neopixel.NeoPixel(PIXEL_PIN, 1, pixel_order=ORDER)

# Loop forever and blink the color
while True:
    pixel[0] = COLOR
    time.sleep(DELAY)
    pixel[0] = CLEAR
    time.sleep(DELAY)
