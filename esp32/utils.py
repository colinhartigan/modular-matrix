import machine
import neopixel
import uasyncio as asyncio
import math
from collections import OrderedDict
import _g

led_map = [  # draw from top left as (0,0)
    [0, 31, 32, 63, 64, 95, 96, 127, 128, 159, 160, 191, 192, 223, 224, 255],
    [1, 30, 33, 62, 65, 94, 97, 126, 129, 158, 161, 190, 193, 222, 225, 254],
    [2, 29, 34, 61, 66, 93, 98, 125, 130, 157, 162, 189, 194, 221, 226, 253],
    [3, 28, 35, 60, 67, 92, 99, 124, 131, 156, 163, 188, 195, 220, 227, 252],
    [4, 27, 36, 59, 68, 91, 100, 123, 132, 155, 164, 187, 196, 219, 228, 251],
    [5, 26, 37, 58, 69, 90, 101, 122, 133, 154, 165, 186, 197, 218, 229, 250],
    [6, 25, 38, 57, 70, 89, 102, 121, 134, 153, 166, 185, 198, 217, 230, 249],
    [7, 24, 39, 56, 71, 88, 103, 120, 135, 152, 167, 184, 199, 216, 231, 248],
    [8, 23, 40, 55, 72, 87, 104, 119, 136, 151, 168, 183, 200, 215, 232, 247],
    [9, 22, 41, 54, 73, 86, 105, 118, 137, 150, 169, 182, 201, 214, 233, 246],
    [10, 21, 42, 53, 74, 85, 106, 117, 138, 149, 170, 181, 202, 213, 234, 245],
    [11, 20, 43, 52, 75, 84, 107, 116, 139, 148, 171, 180, 203, 212, 235, 244],
    [12, 19, 44, 51, 76, 83, 108, 115, 140, 147, 172, 179, 204, 211, 236, 243],
    [13, 18, 45, 50, 77, 82, 109, 114, 141, 146, 173, 178, 205, 210, 237, 242],
    [14, 17, 46, 49, 78, 81, 110, 113, 142, 145, 174, 177, 206, 209, 238, 241],
    [15, 16, 47, 48, 79, 80, 111, 112, 143, 144, 175, 176, 207, 208, 239, 240],
]

# super simple 3x3 font for testing
font_small = {
    "A": [
        [0, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "B": [
        [1, 1, 0],
        [1, 1, 1],
        [1, 1, 0],
    ],
    "C": [
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
    ],
    "D": [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 0],
    ],
    "E": [
        [1, 1, 1],
        [1, 1, 0],
        [1, 1, 1],
    ],
    "F": [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 0],
    ],
    "G": [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "H": [
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "I": [
        [1, 1, 1],
        [0, 1, 0],
        [1, 1, 1],
    ],
    "J": [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 0],
    ],
    "K": [
        [1, 0, 1],
        [1, 1, 0],
        [1, 0, 1],
    ],
    "L": [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "M": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "N": [
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "O": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "P": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 0],
    ],
    "Q": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ],
    "R": [
        [1, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "S": [
        [0, 1, 1],
        [0, 1, 0],
        [1, 1, 0],
    ],
    "T": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "U": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "V": [
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ],
    "W": [
        [1, 0, 1],
        [1, 1, 1],
        [1, 1, 1],
    ],
    "X": [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ],
    "Y": [
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 1],
    ],
    "1": [
        [1, 1, 0],
        [0, 1, 0],
        [1, 1, 1],
    ],
    "2": [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 1],
    ],
    "3": [
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 0],
    ],
    "4": [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
    ],
    "5": [
        [0, 1, 1],
        [0, 1, 0],
        [1, 1, 0],
    ],
    "6": [
        [1, 0, 0],
        [1, 1, 1],
        [1, 1, 1],
    ],
    "7": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    "8": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ],
    "9": [
        [1, 1, 1],
        [1, 1, 1],
        [0, 0, 1],
    ],
    "0": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    " ": [
        [0],
        [0],
        [0],
    ],
    ".": [
        [0],
        [0],
        [1],
    ],
    ",": [
        [0, 0],
        [0, 0],
        [1, 1],
    ],
    "!": [
        [1],
        [1],
        [1],
    ],
    "?": [
        [1, 1],
        [0, 1],
        [1, 0],
    ],
    ":": [
        [1],
        [0],
        [1],
    ],
    ";": [
        [1],
        [0],
        [1],
    ],
    "'": [
        [1],
        [0],
        [0],
    ],
    "$": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ],
    "-": [
        [0, 0],
        [1, 1],
        [0, 0],
    ],
    "%": [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ],
}

# 3x5 font thats more legible
font_large = {
    "A": [
        [0, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "B": [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 0],
    ],
    "C": [
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [0, 1, 1],
    ],
    "D": [
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
    ],
    "E": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "F": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
    ],
    "G": [
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ],
    "H": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "I": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 1],
    ],
    "J": [
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
    ],
    "K": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "L": [
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "M": [
        [1, 0, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "N": [
        [1, 0, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "O": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "P": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
    ],
    "Q": [
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ],
    "R": [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "S": [
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 0],
    ],
    "T": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "U": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
    ],
    "V": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "W": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "X": [
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
    ],
    "Y": [
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "Z": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "1": [
        [0, 1],
        [1, 1],
        [0, 1],
        [0, 1],
        [0, 1],
    ],
    "2": [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "3": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "4": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    "5": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "6": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "7": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "8": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    "9": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    "0": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    " ": [
        [0],
        [0],
        [0],
        [0],
        [0],
    ],
    ".": [
        [0],
        [0],
        [0],
        [0],
        [1],
    ],
    ",": [
        [0],
        [0],
        [0],
        [1],
        [1],
    ],
    "?": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 0],
        [0, 0, 0],
        [0, 1, 0],
    ],
    "!": [
        [1],
        [1],
        [1],
        [0],
        [1],
    ],
    ":": [
        [0],
        [1],
        [0],
        [1],
        [0],
    ],
    ";": [
        [0],
        [1],
        [0],
        [1],
        [1],
    ],
    "'": [
        [1],
        [1],
        [0],
        [0],
        [0],
    ],
    "$": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ],
    "-": [
        [0, 0],
        [0, 0],
        [1, 1],
        [0, 0],
        [0, 0],
    ],
    "%": [
        [1, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1],
    ],
}

# 5x7 font that's really big
font_xl = {
    "A": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "B": [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
    ],
    "C": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "D": [
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
    ],
    "E": [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    "F": [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
    "G": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "H": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "I": [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
    ],
    "J": [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
    ],
    "K": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "L": [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    "M": [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "N": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "O": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "P": [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
    "Q": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1],
    ],
    "R": [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "S": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "T": [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "U": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "V": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
    ],
    "W": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
    ],
    "X": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "Y": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "Z": [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    "1": [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    "2": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    "3": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "4": [
        [0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ],
    "5": [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "6": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "7": [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
    ],
    "8": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "9": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    "0": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    " ": [
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
    ],
    ".": [
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [1],
    ],
    ",": [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 1],
        [1, 0],
    ],
    "!": [
        [1],
        [1],
        [1],
        [1],
        [1],
        [0],
        [1],
    ],
    "?": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    ":": [
        [0],
        [1],
        [0],
        [0],
        [0],
        [1],
        [0],
    ],
    ";": [
        [0, 0],
        [1, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 1],
        [1, 0],
    ],
    "'": [
        [0, 1],
        [0, 1],
        [1, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ],
    "$": [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1],
        [1, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 1],
        [1, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ],
    "-": [
        [0, 0],
        [0, 0],
        [0, 0],
        [1, 1],
        [0, 0],
        [0, 0],
        [0, 0],
    ],
    "%": [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ],    

}

font_small = OrderedDict(sorted(font_small.items(), key=lambda t: t[0]))
font_large = OrderedDict(sorted(font_large.items(), key=lambda t: t[0]))
font_xl = OrderedDict(sorted(font_xl.items(), key=lambda t: t[0]))
font_lookup = [font_small, font_large, font_xl]


# globals
def get_led(x, y): return led_map[y][x]
scroll_tasks = []
np = _g.np


# utility functions
def clear_row(minY, maxY):
    for x in range(0, 16):
        for y in range(minY, maxY+1):
            np[get_led(x,y)] = (0,0,0)

def clear_area(minX, maxX, minY, maxY):
    for x in range(minX, maxX+1):
        for y in range(minY, maxY+1):
            np[get_led(x,y)] = (0,0,0)

def generate_word_offsets(word, startX=0, startY=0, font=1):
    output = []
    offsetX = 0
    font = font_lookup[font]
    for letter in word:
        font_code = font[letter.upper()]
        for y, row in enumerate(font_code):
            for x, pixel in enumerate(row):
                if pixel:
                    output.append((startX + x + offsetX, startY + y))
        offsetX += len(font_code[0]) + 1
    
    overflow = offsetX > 16

    return output, overflow

def write_word(offsets, color=(5, 5, 5), clear=True):
    if clear:
        minX = min(offsets, key=lambda x: x[0])[0]
        maxX = max(offsets, key=lambda x: x[0])[0]
        minY = min(offsets, key=lambda x: x[1])[1]
        maxY = max(offsets, key=lambda x: x[1])[1]
        clear_area(minX, maxX, minY, maxY)
    for x, y in offsets:
        np[get_led(x,y)] = color

async def scroll_loop():
    # wait until all tasks are done scrolling before repeatinga
    while True:
        
        enabled_tasks = [task for task in scroll_tasks if task["enabled"]]
        if len(enabled_tasks) == 0:
            for task in scroll_tasks:
                task["enabled"] = True
            await _g.scroll_complete_callback()

        task_copy = [i for i in scroll_tasks if i["enabled"]]
        for task in task_copy:
            clear_row(task["attrs"]["minY"], task["attrs"]["maxY"])
            new = [(x + task["offset"], y) for x, y in task["offsets"]]
            for led in new:
                if led[0] >= 0 and led[0] < 16:
                    np[get_led(led[0], led[1])] = (20, 20, 20)
            task["offset"] -= 1
            if task["offset"] == task["endpoint"]:
                if not task["repeat"]:
                    scroll_tasks.remove(task)
                else:
                    task["offset"] = 17
                    task["enabled"] = False
        
        await asyncio.sleep(0.15)

def queue_scroll(offsets, id="", repeat=False):
    dupe = [i for i in scroll_tasks if i["id"] == id]
    
    if len(dupe) == 0:
        minX = min(offsets, key=lambda x: x[0])[0]
        maxX = max(offsets, key=lambda x: x[0])[0]
        minY = min(offsets, key=lambda x: x[1])[1]
        maxY = max(offsets, key=lambda x: x[1])[1]

        payload = {
            "offsets": offsets,
            "id": id,
            "endpoint": -(maxX + minX) - 2,
            "offset": 17,
            "repeat": repeat,
            "enabled": True,
            "attrs": {
                "minX": minX,
                "maxX": maxX,
                "minY": minY,
                "maxY": maxY,
            }
        }
        scroll_tasks.append(payload)