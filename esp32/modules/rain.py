import random

from customLED import np
import _g
from utils import *
from modules.shapes import shapes
from modules.proc_cloud import Cloud
    
class Rain():
    def __init__(self):
        self.id = "rain"

        self.raindrops = []
        
        self.clouds = []

        self.c = Cloud(6, 4)
        self.cloud = self.c.shape
        self.cloud_offset_x = 0
        self.cloud_step = 139

        self.cloud_shift_step = 0
        self.cloud_shift_target_step = 10

    
    def step(self, day, **kwargs):
        cloud_cover = kwargs["cloud_cover"]
        np.fill((20,20,25))
        self.cloud_step += 1
        self.cloud_shift_step += 1

        if self.cloud_step >= self.cloud_shift_target_step * 14:
            self.cloud_step = 0
            
            w = 16
            h = 5
            new_cloud = Cloud(w,h)

            self.clouds.append({
                "shape": new_cloud.shape,
                "offset_x": 16,
                "offset_y": 0,
            })

        shift = False
        if self.cloud_shift_step == self.cloud_shift_target_step:
            shift = True
            self.cloud_shift_step = 0

        for cloud in [i for i in self.clouds]:
            if shift:
                cloud["offset_x"] -= 1
                if cloud["offset_x"] < -len(cloud["shape"][0]):
                    self.clouds.remove(cloud)
            for y in range(len(cloud["shape"])):
                for x in range(len(cloud["shape"][y])):
                    if cloud["shape"][y][x] == 1:
                        if x + cloud["offset_x"] < 16 and x + cloud["offset_x"] >= 0:
                            np[get_led(cloud["offset_x"] + x, y)] = (150, 150, 150)