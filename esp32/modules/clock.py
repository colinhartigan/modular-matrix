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
    
        time = rtc.datetime()
        hour_tens = time[3]
        hour_ones = time[4]
        mins = time[5]

        if int(mins) < 10:
            mins = "0" + str(mins)

        secs = time[6]
        colon = int(secs) % 2 == 0

        print(f"{hour_tens}{hour_ones}:{mins}:{secs}")

        hour_offsets, _ = generate_word_offsets(f"{hour_tens}{hour_ones}", 3, 1, 2)
        mins_offsets, _ = generate_word_offsets((':' if colon else ' ') + f"{mins}", 1, 8, 2)

        #_g.np.fill_gradient(0xDC143C, 0xF08080, 25)
        _g.np.fill_solid((0,0,0))
        write_word(hour_offsets, clear=False)
        write_word(mins_offsets, clear=False)

        np.write()
        
        await asyncio.sleep(1)