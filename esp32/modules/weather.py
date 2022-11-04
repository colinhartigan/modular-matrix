import random
import ntptime
import utime as time
import urequests as requests
from machine import RTC

from customLED import np
import _g
from utils import *

rtc = RTC()

clouds = {
    "cloud_small": [
        [0, 0, 1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 1, 1, 0],
    ],
    "cloud_large": [
        [0, 0, 1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 1, 1, 0],
    ],
}

states = {
    "cloudy": {
        "cloud_small": {
            "offset": 16,
            "y": 0,
            "shape": clouds["cloud_small"]
        },
        "cloud_large": {
            "offset": 16,
            "y": 0,
            "shape": clouds["cloud_large"]
        },
        "clouds": []
    },
    "clear": {
        "sun": {
            "gaps": [(2, 2), (2, 5), (4, 2), (4, 5), (5, 3), (5, 4)],
            "rays": [(1, 9), (1, 10), (1, 11), (1, 12), (3, 9), (3, 10), (4, 11), (4, 12), (5, 8), (6, 9), (6, 10), (7, 7), (8, 8), (9, 9)]
        },
    },
    "atmosphere": {
        "target_step": 5,
        "step": 0,
        "lines": []
    },
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
                # just mirror for other half lol
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            ]
        }
    }
}


def clouds_step():
    np.fill((28, 159, 189))

    # draw a quarter-circle in the upper left corner
    for i in range(0, 12):
        for j in range(0, 12):
            if math.sqrt(i**2 + j**2) < 8:
                np[get_led(i, j)] = (201, 197, 109)

# cloud updating
    cloud = states["cloudy"]["cloud_small"]
    cloud["offset"] -= 1

    for i in range(4):
        for j in range(8):
            if cloud["shape"][i][j] == 1:
                if cloud["offset"] + j >= 0 and cloud["offset"] + j < 16:
                    np[get_led(cloud["offset"] + j, cloud["y"] + i)] = (150, 150, 150)

    if cloud["offset"] < -8:
        cloud["y"] = random.randint(0, 5)
        cloud["offset"] = 16


def clear_step():
    np.fill((28, 159, 189))

    for i in range(0, 12):
        for j in range(0, 12):
            if math.sqrt(i**2 + j**2) < 8:
                np[get_led(i, j)] = (201, 197, 109)

    for i in states["clear"]["sun"]["gaps"]:
        np[get_led(i[1], i[0])] = (40, 40, 40)

    for i in states["clear"]["sun"]["rays"]:
        np[get_led(i[1], i[0])] = (201, 197, 109)
        np[get_led(i[0], i[1])] = (201, 197, 109)


def atmosphere_step():
    np.fill((20, 20, 20))

    states["atmosphere"]["step"] += 1
    if states["atmosphere"]["step"] == states["atmosphere"]["target_step"]:
        states["atmosphere"]["target_step"] = random.randint(2, 8)
        length = random.randint(4, 14)
        y_offset = random.randint(1, 14)
        x_offset = random.randint(1, (15 - length))
 
        states["atmosphere"]["lines"].append({
            "length": length,
            "y_offset": y_offset,
            "x_offset": x_offset,
            "step": 0
        })
        states["atmosphere"]["step"] = 0

    for line in [i for i in states["atmosphere"]["lines"]]:
        for i in range(line["length"]):
            brightness = random.randint(30, 100)
            np[get_led(line["x_offset"] + i, line["y_offset"])
               ] = (brightness, brightness, brightness)

        line["step"] += 1
        if line["step"] > 30:
            states["atmosphere"]["lines"].remove(line)


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
            "thunderstorm": clear_step,
            "drizzle": clear_step,
            "rain": clear_step,
            "snow": snow_step,
            "atmosphere": atmosphere_step,
            "clear": clear_step,
            "clouds": clouds_step,
        }
        self.condition = "clouds"
        self.condition_desc = "clear sky"
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
        if hours == 0:
            hours = "00"

        mins = time[5]

        if int(mins) < 10:
            mins = "0" + str(mins)

        secs = time[6]
        colon = int(secs) % 2 == 0

        self.hours = str(hours)
        self.minutes = str(mins)
        self.colon = colon


    def update_weather(self):
        weather = requests.get(url='https://api.openweathermap.org/data/2.5/weather?lat=33.77947361084321&lon=-84.40386294762466&appid=bc31366f445bd9b7e31876cd030a2c99')  # get weather
        weather = weather.json()
        temp = (weather["main"]["temp"] - 273.15) * (9/5) + 32

        self.condition = weather["weather"][0]["main"].lower()
        self.temp = int(temp)
        self.condition_desc = weather["weather"][0]["description"].lower().strip()

        condition_desc_text, _ = generate_word_offsets(self.condition_desc, 0, 11, 1)
        
        def finish_scroll():
            self.hide_time = False

        queue_scroll(condition_desc_text, clear=True, color=(255, 255, 255), callback=finish_scroll)
        self.hide_time = True


    def loop(self):
        self.conditions[self.condition]()
        self.update_timer += 1
        if self.update_timer == 200:
            self.time = False
        if self.update_timer == 250:
            self.update_timer = 0
            self.update_weather()
            self.time = True

        if self.time and not self.hide_time:
            hours_offsets, _ = generate_word_offsets(self.hours, 9, 5, 1)
            mins_offsets, _ = generate_word_offsets((":" if self.colon else " ") + self.minutes, 7, 11, 1)
            write_word(hours_offsets, clear=False, color=(252, 251, 220))
            write_word(mins_offsets, clear=False, color=(252, 251, 220))
        elif not self.hide_time:
            temp_offsets, _ = generate_word_offsets(f"{str(self.temp)}F", 5, 11, font=1)
            write_word(temp_offsets, clear=False, color=(252, 251, 220))