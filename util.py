import math


def get_angle(z1, x1, z2, x2):
    if x2==x1:
        if z2 == z1: return 0
        if z2 > z1: return 3*math.pi/2
        if z2 < z1: return math.pi/2
    atan = -math.atan((z2-z1)/(x2-x1))
    if x2-x1 < 0:
        return atan + math.pi
    else:
        return atan
