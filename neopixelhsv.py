import colorsys
import neopixel

class NeoPixelHSV(neopixel.NeoPixel):
    """HSV:
    Hue: 0-360
    Saturation: 0-100
    Value: 0-100
    """
    def __init__(
        self, pin, n, *, bpp=3, brightness=1.0, auto_write=True
    ):
        pixel_order = neopixel.RGB if bpp == 3 else neopixel.RGBW
        super().__init__(
            pin, n, bpp=bpp, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order,
        )

    def fill(self, color):
        super().fill(self.__hsv_to_rgb(color))
            
    def __setitem__(self, index, color):
        super().__setitem__(index, self.__hsv_to_rgb(color))
        
    def __getitem__(self, index):
        return(self.__rgb_to_hsv(super().__getitem__(index)))
        
    def __hsv_to_rgb(self, color):
        rgb_color = colorsys.hsv_to_rgb(color[0]/360, color[1]/100, color[2]/100)
        return [int(x * 255) for x in rgb_color]
    
    def __rgb_to_hsv(self, color):
        hsv_color = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
        return (int(hsv_color[0]*360), int(hsv_color[1]*100), int(hsv_color[2]*100))
