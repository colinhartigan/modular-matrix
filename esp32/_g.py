import neopixel, machine
import driver.trickLED as trickLED 

np = trickLED.TrickLED(machine.Pin(13), 256)

active_module = "clock"

async def bruh():
    pass

scroll_complete_callback = bruh