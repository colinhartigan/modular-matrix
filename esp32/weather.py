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
from modules.rain import Rain


class Weather:
    def __init__(self):

        self.conditions = {
            # "thunderstorm": clear_step,
            # "drizzle": clear_step,
            "rain": Rain(),
            # "snow": snow_step,
            "atmosphere": Atmosphere(), 
            "clear": Clear(),
            "clouds": Clouds(),
        }
        self.condition = "clouds"
        self.condition_desc = "clear sky"
        self.cloud_cover = 80
        self.visibility = 10000 # in m
        self.temp = 69
        self.day = True
        self.update_timer = 0

        self.scrolling = False

        self.update_weather()


    def update_weather(self):

        weather = requests.get(url='https://api.openweathermap.org/data/2.5/weather?lat=33.77947361084321&lon=-84.40386294762466&appid=bc31366f445bd9b7e31876cd030a2c99')  # get weather
        weather = weather.json()
        temp = (weather["main"]["temp"] - 273.15) * (9/5) + 32

        dt = weather["dt"]
        sunrise = weather["sys"]["sunrise"]
        sunset = weather["sys"]["sunset"]

        #self.day = dt > sunrise and dt < sunset
        self.day = True
        _g.day = self.day
 
        self.condition = weather["weather"][0]["main"].lower() 
        self.temp = int(temp)
        self.cloud_cover = weather["clouds"]["all"]
        self.visibility = weather["visibility"]
        self.condition_desc = weather["weather"][0]["description"].lower().strip()

        condition_desc_text, _ = generate_word_offsets(self.condition_desc, 0, 11, 1)
        
        def finish_scroll():
            _g.time_enabled = True
            self.update_timer = 0
            self.scrolling = False

        if self.day:
            queue_scroll(condition_desc_text, clear=True, color=(255, 255, 255), callback=finish_scroll)
            _g.time_enabled = False
            self.scrolling = True


    def loop(self):
        kwargs = {
            "cloud_cover": self.cloud_cover,
            "visibility": self.visibility,
        }
        self.conditions["rain"].step(self.day, **kwargs)

        if self.day:
            np.brightness_divide = 20
            if self.update_timer == 300:
                _g.time_enabled = False
        else:
            np.brightness_divide = 90
            _g.time_enabled = True
        
        if self.update_timer == 500:
            self.update_weather()
            _g.time_enabled = False

        self.update_timer += 1

        if not _g.time_enabled and not self.scrolling:
            temp_offsets, _ = generate_word_offsets(f"{str(self.temp)}F", 5, 11, font=1)
            write_word(temp_offsets, clear=False, color=(252, 251, 220))