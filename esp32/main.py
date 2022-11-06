import machine, sys, time
import uasyncio as asyncio
import math
import utime as time
import _thread
from collections import OrderedDict

from utils import *
from customLED import np
import _g
import weather

np.fill((0,0,0)) 
framerate = 20

def task_loop():
    weather_driver = weather.Weather()

    render_tasks = [
        {
            "task": weather_driver.loop,
            "interval": 5,
        },
        {
            "task": weather_driver.update_time,
            "interval": 5,
        },
        {
            "task": scroll_loop,
            "interval": 5,
        },
    ]

    last_time = time.ticks_ms()
    target_frame_time = 1/framerate

    while True:

        t = time.ticks_ms()
        time_diff = t - last_time
        
        #print(t - last_time)
        last_time = t

        for task in render_tasks:
            task["task"]()
        _g.render_step = _g.render_step + 1 if _g.render_step < (framerate - 1) else 0
        np.write()

        time_left = target_frame_time - (1/(time.ticks_ms() - last_time)) # keep frame times consistent (under normal circumstances)
        #print(time_left)
        if time_left > 0:
            time.sleep(time_left)
        else:
            print(f"frame time exceeded target frame time by {time_left} seconds")

async def main():
    # dispatch async tasks
    # asyncio.create_task(scroll_loop())
    # asyncio.create_task(render_loop())
    task_loop()

    #asyncio.get_event_loop().run_forever() 

if __name__ == "__main__":
    asyncio.run(main())

np.write()  