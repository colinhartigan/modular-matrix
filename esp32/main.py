import machine, sys, time
import uasyncio as asyncio
import math
import utime as time
import _thread
from collections import OrderedDict

from utils import *
from customLED import np
import _g
import modules.weather as weather

np.fill((0,0,0)) 
framerate = 10

lock = _thread.allocate_lock()

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
    while True:

        t = time.ticks_ms()
        #print(t - last_time)
        last_time = t

        for task in render_tasks:
            task["task"]()
        _g.render_step = _g.render_step + 1 if _g.render_step < (framerate - 1) else 0
        np.write()
        time.sleep(1/framerate)

async def main():
    # dispatch async tasks
    # asyncio.create_task(scroll_loop())
    # asyncio.create_task(render_loop())
    t1, t2 = None, None 
    try:
        t1 = _thread.start_new_thread(task_loop, ())
        #t2 = _thread.start_new_thread(render_loop, ())
    except KeyboardInterrupt:
        t1.exit()
        #t2.exit()

    #asyncio.get_event_loop().run_forever() 

if __name__ == "__main__":
    asyncio.run(main())

np.write()  