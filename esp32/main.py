import sys, time
#import machine
#import uasyncio as asyncio
import math
#import utime as time
import time
import _thread
from collections import OrderedDict

from utils import *
from customLED import np
import _g
import weather
import clock

np.fill((0,0,0)) 

def task_loop():
    weather_driver = weather.Weather()
    clock_driver = clock.Clock()

    render_tasks = [
        {
            "task": weather_driver.loop,
        },
        {
            "task": scroll_loop,
        },
        {
            "task": scroll_render,
        },
        {
            "task": clock_driver.tick,
        },
        {
            "task": clock_driver.draw,
        }
    ]

    #last_time = time.ticks_ms()
    last_time = time.time() * 1000

    while True:

        target_frame_time = (1/_g.framerate)*1000

        #t = time.ticks_ms()
        t = time.time() * 1000
        time_diff = t - last_time
        
        #print(t - last_time)
        last_time = t

        for task in render_tasks:
            task["task"]()
        _g.render_step = _g.render_step + 1 if _g.render_step < (_g.framerate - 1) else 0

        #time_left = (target_frame_time - (time.ticks_ms() - last_time)) # keep frame times consistent (under normal circumstances)
        time_left = (target_frame_time - ((time.time() * 1000) - last_time)) # keep frame times consistent (under normal circumstances)
        #print(target_frame_time, time.ticks_ms() - last_time, time_left/1000)
        if time_left > 0:
            time.sleep(time_left/1000)
        elif time_left < 0 and abs(time_left/1000) < 5:
            pass
            #print(f"target frame time exceeded but within safe zone ({abs(time_left/1000)}ms)")
        else:
            print(f"frame time exceeded target frame time by {abs(time_left/1000)}ms")

        np.write()

def main():
    print("initializing")
    task_loop()

if __name__ == "__main__":
    main()

np.write()