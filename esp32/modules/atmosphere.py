import random

from customLED import np
import _g
from utils import *
from modules.shapes import shapes

class Atmosphere:
    def __init__(self):
        self.id = "atmosphere"
        
        self.target_step = 5
        self.step = 0
        self.lines = []


    def step(self, day, **kwargs):
        np.fill((20, 20, 20))

        self.step += 1
        if self.step == self.target_step:
            self.target_step = random.randint(2, 8)
            length = random.randint(4, 14)
            y_offset = random.randint(1, 14)
            x_offset = random.randint(1, (15 - length))
    
            self.lines.append({
                "length": length,
                "y_offset": y_offset,
                "x_offset": x_offset,
                "step": 0
            })
            self.step = 0

        for line in [i for i in self.lines]:
            for i in range(line["length"]):
                brightness = random.randint(30, 100)
                np[get_led(line["x_offset"] + i, line["y_offset"])
                ] = (brightness, brightness, brightness)

            line["step"] += 1
            if line["step"] > 30:
                self.lines.remove(line)