import machine, sys, time
import uasyncio as asyncio
import math
from collections import OrderedDict

from utils import *
from customLED import np
import _g
import modules.weather as weather

np.fill((0,0,0))

change = True

async def module_loop():
    global change
    task = None
    while True:
        if change:
            change = False
            if task:
                task.cancel()
            elif _g.active_module == "weather":
                task = asyncio.create_task(weather.run())

        await asyncio.sleep(1)

        # listener to change mode somewhere in here

async def render_loop():
    while True:
        np.write()
        await asyncio.sleep(.05)

async def main():
    # dispatch async tasks
    asyncio.create_task(scroll_loop())
    asyncio.create_task(module_loop())
    asyncio.create_task(render_loop())

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())

np.write()