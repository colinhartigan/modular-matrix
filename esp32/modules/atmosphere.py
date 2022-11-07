import random

from customLED import np
import _g
from utils import *
from modules.shapes import shapes

class Atmosphere:
    def __init__(self):
        self.id = "atmosphere"
        
        self.visibility = 10000

        self.fog_step = 0
        self.fog_step_target = 4

        self.line_length = 8
        self.line_interval = 2
        self.lines = []
        self.moon = shapes.moon


    def step(self, day, **kwargs):
        if day:
            np.fill((20, 20, 20))
        else:
            np.fill((0, 0, 0))

        if self.visibility != kwargs["visibility"]:
            self.visibility = kwargs["visibility"]
            self.lines = []

        visibility_factor = 11 - int(map_range(self.visibility, 0, 10000, 1, 10)) 
        print(visibility_factor)

        if self.lines == []:
            self.line_length = int(map_range(visibility_factor, 0, 10, 5, 10))
            self.line_interval = int(map_range(11-visibility_factor, 0, 10, 2, 4)) # map range onto another; isnt that nifty!

            for i in range(0, 16, self.line_interval):
                length_offset = random.randint(-1,1)
                self.lines.append({
                    "x": 7-(self.line_length//2),
                    "y": i,
                    "length": self.line_length + length_offset,
                    "step": 0,
                    "target_step": random.randint(4,8)
                })
        
        for line in self.lines:
            if line["step"] == line["target_step"]:
                factor = random.randint(-1, 1)
                line["x"] = line["x"] + factor
                line["step"] = 0
                line["target_step"] = random.randint(4,8)

            line["step"] += 1

            for i in range(0, line["length"]):
                if line["x"] + i < 16 and line["x"] + i >= 0:
                    np[get_led(line["x"] + i, line["y"])] = (40, 40, 40)   


        if day: 
            for i in range(0, 12):
                for j in range(0, 12):
                    if math.sqrt(i**2 + j**2) < 8:
                        np[get_led(i, j)] = (201//visibility_factor, 197//visibility_factor, 109//visibility_factor)
        else:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.moon[i][j] == 1:
                        np[get_led(i, j)] = (135//visibility_factor,136//visibility_factor,156//visibility_factor) 