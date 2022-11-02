import machine, sys, time
import neopixel
import uasyncio as asyncio
import math
from collections import OrderedDict

from utils import *
import _g

if __name__ == "__main__":
    #asyncio.run(main())

    uart = machine.UART(0, 115200, bits=8, parity=None, stop=1, tx=1, rx=3, timeout=10000)

    while True:
        data = sys.stdin.read(1)
        if data == "a":
            _g.np.fill((255,255,255))
            _g.np.write()
        elif data == "b":
            for i in range(255,0, -10):
                _g.np.fill((i,i,i))
                _g.np.write()
                time.sleep_ms(10)
            _g.np.fill((0,0,0))
            _g.np.write()
        time.sleep(.05)