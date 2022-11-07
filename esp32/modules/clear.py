import random

from customLED import np
import _g
from utils import *
from modules.shapes import shapes

class Clear:
    def __init__(self):
        self.id = "clear"

        self.sun = shapes.sun
        self.moon = shapes.moon
        self.star = shapes.star 

        self.stars = []
        self.star_step = 0
        self.target_star_step = 20


    def step(self, day, **kwargs):
        if day:
            np.fill((28, 159, 189))

            for i in range(0, 12):
                for j in range(0, 12):
                    if math.sqrt(i**2 + j**2) < 8:
                        np[get_led(i, j)] = (201, 197, 109)

            for i in self.sun["gaps"]:
                np[get_led(i[1], i[0])] = (40, 40, 40)

            for i in self.sun["rays"]:
                np[get_led(i[1], i[0])] = (201, 197, 109)
                np[get_led(i[0], i[1])] = (201, 197, 109)

        else:
            np.fill((0, 0, 0))
                    
            # star y range is [0, 9]
            if self.star_step == self.target_star_step:
                self.stars.append({
                    "x": random.randint(0, 15),
                    "y": random.randint(0, 15),
                    "brightness": 0,
                    "fade_in": True,
                })
                self.star_step = 0
                self.target_star_step = random.randint(10, 50)

            star_color = (255, 243, 161)

            for star in [i for i in self.stars]:
                factor = 0
                if star["brightness"] >= 1:
                    # only delete the stars immediately sometimes, creates a shimmering star effect
                    if random.randint(0, 5) == 0:
                        star["fade_in"] = False
                    else:
                        star["brightness"] = star["brightness"] - 0.1 
                if star["fade_in"] == True:
                    factor = random.randint(20, 40)/1000 # random between .02 and .04
                else: 
                    factor = -.1

                star["brightness"] = star["brightness"] + factor

                if star["brightness"] < 0:
                    self.stars.remove(star) 
                    continue  

                np[get_led(star["x"], star["y"])] = (int(star_color[0] * star["brightness"]), int(star_color[1] * star["brightness"]), int(star_color[2] * star["brightness"]))

            self.star_step += 1 

            # draw moon over any stars jic
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.moon[i][j] == 1:
                        np[get_led(i, j)] = (135,136,156) 