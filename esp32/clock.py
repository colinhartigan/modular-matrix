import ntptime
from machine import RTC

from customLED import np
import _g
from utils import *

rtc = RTC()

class Clock:
    def __init__(self):
        ntptime.settime()

        self.hours, self.minutes, self.colon = "", "", False

    def tick(self):
        time = rtc.datetime()
        hours = time[4] - 5  # -4 for EDT, -5 for EST
        if hours < 0:
            hours += 24
        if hours < 10:
            hours = f"0{str(hours)}"

        mins = time[5]

        if int(mins) < 10:
            mins = "0" + str(mins)

        secs = time[6]
        colon = int(secs) % 2 == 0

        self.hours = str(hours)
        self.minutes = str(mins)
        self.colon = colon

        if not _g.day:
            self.colon = False 

    def draw(self):
        if _g.time_enabled:
            hours_offsets, _ = generate_word_offsets(self.hours, 9, 5, 1)
            mins_offsets, _ = generate_word_offsets((":" if self.colon else " ") + self.minutes, 7, 11, 1)
            write_word(hours_offsets, clear=False, color=(252, 251, 220))
            write_word(mins_offsets, clear=False, color=(252, 251, 220))