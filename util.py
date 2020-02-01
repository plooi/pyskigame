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



#makes x more extremely towards 1 or 0
#x must be between 0 and 1 duh
def extreme(x, degree=1):
    for i in range(degree):
        if x == .5:
            return .5
        elif x > .5:
            x = x**.5
        elif x < .5:
            x = 1-x
            x = x**.5
            x = 1-x
    return x
        
