import neopixel

ORDER = neopixel.GRB
num_pixels = 450 # total length of led strip

try:
    import board
    PIXEL_GPIO = board.D18

except NotImplementedError as n:
    print('not implemented!! {}'.format(n))
    PIXEL_GPIO = 0
    mock = True

pixels = neopixel.NeoPixel(PIXEL_GPIO, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER, mock=mock)


pixels.fill((255,50,255))
