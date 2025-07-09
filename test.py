import math
from ex5_helper import *


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    y_floor = math.floor(y)
    y_ceil = math.ceil(y)
    x_floor = math.floor(x)
    x_ceil = math.ceil(x)
    a = image[y_floor][x_floor]
    b = image[y_ceil][x_floor]
    c = image[y_floor][x_ceil]
    d = image[y_ceil][x_ceil]
    delta_x = x - x_floor
    delta_y = y - y_floor
    return round(a * (1 - delta_x) * (1 - delta_y) +
                 b * delta_y * (1 - delta_x) + c * delta_x * (1 - delta_y) +
                 d * delta_x * delta_y)
print (bilinear_interpolation([[0, 64, 6], [8, 128, 255], [5,3,2]], 2.5, 1.5))