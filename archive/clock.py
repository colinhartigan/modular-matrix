import ntptime
from machine import RTC

from utils import *
import _g

async def run():
    rtc = RTC()
    ntptime.settime()

    #pain, _ = generate_word_offsets("life is pain. i hate", 1, 1, 2)
    #queue_scroll(pain)

    while True:
        
        await asyncio.sleep(1)