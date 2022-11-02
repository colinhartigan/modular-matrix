import _g 
from utils import *

states = {
    "clear_weather": {
        "cloud": {
            "width": 8,
            "height": 8,
            "offset": -8,
        }
    }
}

def clear_weather():
    _g.np.fill((28//4, 159//4, 189//4)) # implement something that automtically does this
    
    # draw a quarter-circle in the upper left corner
    for i in range(0, 8):
        for j in range(0, 8):
            if math.sqrt(i**2 + j**2) < 8:
                _g.np[get_led(i, j)] = (201//4, 197//4, 109//4)

    # cloud updating
    cloud = states["clear_weather"]["cloud"]
    cloud["offset"] += 1
    # cloud can only go from [8,15]

async def run():
    conditions = {
        "clear_weather": clear_weather,
    }

    condition = "clear_weather"

    while True:
        task = conditions[condition]()

        temp = "69F"
        temp_offsets, _ = generate_word_offsets(temp, 4, 10, font=1)
        write_word(temp_offsets, clear=False, color=(252, 251, 220))
        await asyncio.sleep(1)