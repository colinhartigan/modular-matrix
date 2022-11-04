from neopixel import NeoPixel
import machine

class LED(NeoPixel):

    def __init__(self, pin, n, brightness_divide=1, **kwargs):
        super().__init__(pin, n, **kwargs)
        self.brightness_divide = brightness_divide

    def __setitem__(self, i, val):
        if 0 <= i < self.n:
            val = (val[0] // self.brightness_divide, val[1] // self.brightness_divide, val[2] // self.brightness_divide)
            super().__setitem__(i, val)

    def fill(self, val):
        val = (val[0] // self.brightness_divide, val[1] // self.brightness_divide, val[2] // self.brightness_divide)
        super().fill(val)

np = LED(machine.Pin(13), 256, brightness_divide=20)  