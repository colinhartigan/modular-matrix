import random
import ntptime
import utime as time
import urequests as requests
from machine import RTC

from customLED import np
import _g
from utils import *

from modules.atmosphere import Atmosphere
from modules.clear import Clear 
from modules.clouds import Clouds 

rtc = RTC()

states = {
    "snow": {
        "step": 0,
        "target_step": 5,
        "flake": {
            "offset_x": 3,
            "offset_y": 1,
            "shape": [
                [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                [1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            ]
        }
    }
}

def snow_step():
    np.fill((130, 197, 255))

    for i in range(0, 6):
        for j in range(0, 10):
            if states["snow"]["flake"]["shape"][i][j] == 1:
                np[get_led(states["snow"]["flake"]["offset_x"] + j, states["snow"]["flake"]["offset_y"] + i)] = (0, 62, 138)
                np[get_led(states["snow"]["flake"]["offset_x"] + j, 10 - states["snow"]["flake"]["offset_y"] - i)] = (0, 62, 138)

    states["snow"]["step"] += 1
    if states["snow"]["step"] == states["snow"]["target_step"]:
        states["snow"]["target_step"] = random.randint(1, 5)
        states["snow"]["step"] = 0
        np[get_led(random.randint(0, 15), random.randint(0, 15))] = (255, 255, 255)


class Weather:
    def __init__(self):
        ntptime.settime()

        self.conditions = {
            # "thunderstorm": clear_step,
            # "drizzle": clear_step,
            # "rain": clear_step,
            # "snow": snow_step,
            "atmosphere": Atmosphere(), 
            "clear": Clear(),
            "clouds": Clouds(),
        }
        self.condition = "clouds"
        self.condition_desc = "clear sky"
        self.cloud_cover = 80
        self.temp = 69
        self.day = False
        self.update_timer = 0

        self.time = True
        self.hide_time = False
        self.hours, self.minutes, self.colon = "", "", False

        self.update_weather()

    def update_time(self):
        time = rtc.datetime()
        hours = time[4] - 4  # -4 for EDT, -5 for EST
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


    def update_weather(self):
        print(time.time())
        weather = requests.get(url='https://api.openweathermap.org/data/2.5/weather?lat=33.77947361084321&lon=-84.40386294762466&appid=bc31366f445bd9b7e31876cd030a2c99')  # get weather
        weather = weather.json()
        temp = (weather["main"]["temp"] - 273.15) * (9/5) + 32

        self.condition = weather["weather"][0]["main"].lower()
        self.temp = int(temp)
        #self.cloud_cover = weather["clouds"]["all"]
        self.condition_desc = weather["weather"][0]["description"].lower().strip()

        condition_desc_text, _ = generate_word_offsets(self.condition_desc, 0, 11, 1)
        
        def finish_scroll():
            self.hide_time = False

        if self.day:
            queue_scroll(condition_desc_text, clear=True, color=(255, 255, 255), callback=finish_scroll)
            self.hide_time = True


    def loop(self):
        kwargs = {
            "cloud_cover": self.cloud_cover
        }
        self.conditions["clear"].step(self.day, **kwargs)

        if self.day:
            self.update_timer += 1
            if self.update_timer == 200:
                self.time = False
            if self.update_timer == 250:
                self.update_timer = 0
                self.update_weather()
                self.time = True
        else:
            self.time = True 
            self.colon = False

        if self.time and not self.hide_time:
            hours_offsets, _ = generate_word_offsets(self.hours, 9, 5, 1)
            mins_offsets, _ = generate_word_offsets((":" if self.colon else " ") + self.minutes, 7, 11, 1)
            write_word(hours_offsets, clear=False, color=(252, 251, 220))
            write_word(mins_offsets, clear=False, color=(252, 251, 220))
        elif not self.hide_time:
            temp_offsets, _ = generate_word_offsets(f"{str(self.temp)}F", 5, 11, font=1)
            write_word(temp_offsets, clear=False, color=(252, 251, 220))