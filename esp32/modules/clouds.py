import random

from customLED import np
import _g
from utils import *
from modules.shapes import shapes

class Clouds:
    def __init__(self):
        self.id = "clouds"

        self.cloud = {
            "large": False,
            "offset_x": 0,
            "offset_y": 0,
            "max_offset": 2,
            "anchor": (1, 2),
            "shape": shapes.cloud_small
        }
        self.cloud_cycle = 0

        self.moon = shapes.moon

        self.day = True 


    def step(self, day, **kwargs):

        # unpack kwargs
        cloud_cover = kwargs["cloud_cover"]
        if cloud_cover >= 50 and not self.cloud["large"]:
            self.cloud["large"] = True
            self.cloud["shape"] = shapes.cloud_large
        elif cloud_cover < 50 and self.cloud["large"]:
            self.cloud["large"] = False
            self.cloud["shape"] = shapes.cloud_small

        if day:
            np.fill((40, 159, 189))
            # sun
            for i in range(0, 12):
                for j in range(0, 12):
                    if math.sqrt(i**2 + j**2) < 8:
                        np[get_led(i, j)] = (201, 197, 109)
        else:
            np.fill((0, 0, 0))
            # moon
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.moon[i][j] == 1:
                        np[get_led(i, j)] = (135,136,156) 

        # cloud updating
        cloud = self.cloud

        if self.cloud_cycle == 20:
            rand_x = random.randint(-1, 1)
            rand_y = random.randint(-1, 1)
            self.cloud["offset_x"] = self.cloud["offset_x"] + rand_x
            self.cloud["offset_y"] = self.cloud["offset_y"] + rand_y
            if self.cloud["offset_y"] > self.cloud["max_offset"] or self.cloud["offset_y"] < -self.cloud["max_offset"]:
                self.cloud["offset_y"] = self.cloud["max_offset"]
            if self.cloud["offset_x"] > self.cloud["max_offset"] or self.cloud["offset_x"] < -self.cloud["max_offset"]:
                self.cloud["offset_x"] = self.cloud["max_offset"]
            
            self.cloud_cycle = 0
        self.cloud_cycle += 1
        
        for i in range(len(cloud["shape"])):
            for j in range(len(cloud["shape"][i])):
                if cloud["shape"][i][j] == 1:
                    if cloud["offset_x"] + j + cloud["anchor"][0] >= 0 and cloud["offset_y"] + i + cloud["anchor"][1] < 16:
                        np[get_led(cloud["offset_x"] + j + cloud["anchor"][0], cloud["offset_y"] + i + cloud["anchor"][1])] = (50, 50, 50)