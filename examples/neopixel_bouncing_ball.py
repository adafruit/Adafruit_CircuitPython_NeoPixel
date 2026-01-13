# SPDX-FileCopyrightText: 2025 Jose D. Montoya
# SPDX-License-Identifier: MIT

# This example simulates a ball bouncing on a NeoPixel strip affected by gravity.
# Most NeoPixels = neopixel.GRB or neopixel.GRBW
# The 8mm Diffused NeoPixel (PID 1734) = neopixel.RGB
import time
from math import ceil

import board

import neopixel

# Configure the setup
PIXEL_PIN = board.A3  # pin that the NeoPixel is connected to
ORDER = neopixel.RGB  # pixel color channel order
COLOR = (255, 50, 150)  # color to blink
CLEAR = (0, 0, 0)  # clear (or second color)
DELAY = 0.1  # blink rate in seconds

# Simulation Values.
gravity = 0.5
velocity = 2
energy_loss = 0.6

# Create the NeoPixel object
num_pixels = 60
pixel_seg = neopixel.NeoPixel(PIXEL_PIN, num_pixels, pixel_order=ORDER)

# Animation start values
travel = 0
going_up = False
floor_count = 0
top = 0

# Loop forever and simulate
while True:
    # Blink the color
    pixel_seg[travel] = COLOR
    time.sleep(0.05)
    pixel_seg[travel] = CLEAR
    time.sleep(DELAY)
    velocity += gravity

    # Check if the ball is at the top to change direction
    if velocity >= 0 and going_up:
        velocity = ceil(-velocity)
        going_up = False
        top = travel

    # Check if the ball is at the bottom to break the loop
    if top == num_pixels - 1:
        floor_count = floor_count + 1
    if floor_count == 3:
        break

    travel = int(travel + velocity)

    # Check if the ball is at the floor to change direction
    if travel >= num_pixels:
        travel = num_pixels - 1
        velocity = ceil(-velocity * energy_loss)
        going_up = True

# Clear the strip
pixel_seg.fill(0)
