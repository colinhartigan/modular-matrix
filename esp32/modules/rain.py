import random

from customLED import np
import _g
from utils import *
from modules.shapes import shapes
from modules.proc_cloud import Cloud
    
class Rain:
    def __init__(self):
        self.id = "rain"

        self.raindrops = []

        self.rain_step = 0
        self.raindrop_target_step = 3
        self.rain_odd = False
        
        self.c = Cloud(6,4)
        self.cloud = {
            "offset_x": 0,
            "offset_y": 0,
            "max_offset": 2,
            "anchor": (1, 2),
            "shape": shapes.cloud_large
        }
        self.cloud_cycle = 0
        self.target_cycle = 20

        self.bg_clouds = []
        self.cloud_step = 139
        self.cloud_shift_step = 0
        self.cloud_shift_target_step = 10

    
    def step(self, day, **kwargs):
        cloud_cover = kwargs["cloud_cover"]
        np.fill((20,20,25))
        self.rain_step += 1
        self.cloud_cycle += 1
        self.cloud_shift_step += 1
        self.cloud_step += 1


        if self.rain_step >= self.raindrop_target_step:
            rang = range(1,9,2) if self.rain_odd else range(2,10,2)
            for i in rang:
                self.raindrops.append({
                    "x": self.cloud["offset_x"]+ i + 1,
                    "y": self.cloud["offset_y"]+4,
                })
            self.rain_odd = not self.rain_odd
            self.rain_step = 0

        #print(self.raindrops)
        for drop in [r for r in self.raindrops]:
            drop["y"] += 1
            if drop["y"] >= 16:
                self.raindrops.remove(drop)
            else:
                np[get_led(drop["x"], drop["y"])] = (167, 199, 255)


        # background clouds
        if self.cloud_step >= self.cloud_shift_target_step * 14:
            self.cloud_step = 0
            
            w = 16
            h = 5
            new_cloud = Cloud(w,h)

            self.bg_clouds.append({
                "shape": new_cloud.shape,
                "offset_x": 16,
                "offset_y": 0,
            })

        shift = False
        if self.cloud_shift_step == self.cloud_shift_target_step:
            shift = True
            self.cloud_shift_step = 0

        for cloud in [i for i in self.bg_clouds]:
            if shift:
                cloud["offset_x"] -= 1
                if cloud["offset_x"] < -len(cloud["shape"][0]):
                    self.bg_clouds.remove(cloud)
            for y in range(len(cloud["shape"])):
                for x in range(len(cloud["shape"][y])):
                    if cloud["shape"][y][x] == 1:
                        if x + cloud["offset_x"] < 16 and x + cloud["offset_x"] >= 0:
                            np[get_led(cloud["offset_x"] + x, y)] = (75,75,75)


        # foreground cloud
        if self.cloud_cycle == self.target_cycle:
            rand_x = random.randint(-1, 1)
            rand_y = random.randint(-1, 1)
            self.cloud["offset_x"] = self.cloud["offset_x"] + rand_x
            self.cloud["offset_y"] = self.cloud["offset_y"] + rand_y

            # cloud bound checking
            if self.cloud["offset_y"] > self.cloud["max_offset"]:
                self.cloud["offset_y"] = self.cloud["max_offset"]
            elif self.cloud["offset_y"] < -self.cloud["max_offset"]:
                self.cloud["offset_y"] = -self.cloud["max_offset"]
            if self.cloud["offset_x"] > self.cloud["max_offset"]:
                self.cloud["offset_x"] = self.cloud["max_offset"]
            elif self.cloud["offset_x"] < -self.cloud["max_offset"]:
                self.cloud["offset_x"] = -self.cloud["max_offset"]
            
            self.cloud_cycle = 0
            self.target_cycle = random.randint(15, 30)
        
        for i in range(len(self.cloud["shape"])):
            for j in range(len(self.cloud["shape"][i])):
                if self.cloud["shape"][i][j] == 1:
                    if self.cloud["offset_x"] + j + self.cloud["anchor"][0] >= 0 and self.cloud["offset_y"] + i + self.cloud["anchor"][1] < 16:
                        color = (150, 150, 150)
                        if not day:
                            color = (50, 50, 50)
                        np[get_led(self.cloud["offset_x"] + j + self.cloud["anchor"][0], self.cloud["offset_y"] + i + self.cloud["anchor"][1])] = color


        