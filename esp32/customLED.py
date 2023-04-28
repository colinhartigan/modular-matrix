#from neopixel import NeoPixel
from emulator.emulator_backend import Adafruit_NeoPixel
#import machine


class LED(Adafruit_NeoPixel):

    # def __init__(self, pin, n, brightness_divide=1, **kwargs):
    #     super().__init__(pin, n, **kwargs)
    #     self.brightness_divide = brightness_divide

    def __init__(self, n, brightness_divide=1, **kwargs):
        self.n = n
        self.brightness_divide = brightness_divide
        super().__init__(n, 6, "NEO_GRB + NEO_KHZ800")
        super().begin(draw_matrix=True, width=16, height=16)

    def __setitem__(self, i, val):
        # val[3] is custom dim factor
        if not len(val) == 4:
            val = (val[0], val[1], val[2], self.brightness_divide)
        if 0 <= i < self.n:
            val = (self.dim(val[0], val[3]), self.dim(
                val[1], val[3]), self.dim(val[2], val[3]))
            super().__setitem__(i, (val[0], val[1], val[2]))

    def dim(self, val, factor=None):
        # if factor is None:
        #     factor = self.brightness_divide
        # d = val / factor
        # if d < 1 and d != 0:
        #     d = 1
        # return int(d)
        return int(val)

    def fill(self, val):
        val = (self.dim(val[0]), self.dim(val[1]), self.dim(val[2]))
        super().fill(val)


#np = LED(machine.Pin(13), 256, brightness_divide=20)
np = LED(256, brightness_divide=1)
