import machine
import neopixel
import uasyncio as asyncio
import math
from collections import OrderedDict

from utils import *
import _g
import stocks

np = _g.np
np.fill((0, 0, 0))

change = True

async def module_loop():
    global change
    while True:
        if change:
            change = False
            if _g.active_module == "stocks":
                await stocks.run()

        await asyncio.sleep(1)

        # listener to change mode somewhere in here

async def main():
    # dispatch async tasks
    asyncio.create_task(scroll_words())
    asyncio.create_task(module_loop())

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    asyncio.run(main())

np.write()