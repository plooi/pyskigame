import numpy as np
import math




#for z going down
def get_plane_rotation(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    
    v1_x = x3-x1
    v1_y = y3-y1
    v1_z = z3-z1
    
    v2_x = x2-x1
    v2_y = y2-y1
    v2_z = z2-z1
    
    
    #cp_1 = v1_y*v2_z - v1_z*v2_y
    #cp_2 = v1_z*v2_x - v1_x*v2_z
    #cp_3 = v1_x*v2_y - v1_y*v2_x
    
    x = v1_y*v2_z - v1_z*v2_y
    y = v1_z*v2_x - v1_x*v2_z
    z = v1_x*v2_y - v1_y*v2_x
    
    #a = cp_1
    #b = cp_2
    #c = cp_3
    
    #x = a
    #y = b
    #z = c
    
    hr = get_angle(0,0,x,z)
    
    horizontal_distance = (x**2 + z**2)**.5
    if horizontal_distance == 0:
        if y == 0:
            vr = 0
        elif y > 0:
            vr = math.pi/2
        elif y < 0:
            vr = -math.pi/2
    else:
        vr = math.atan(y/horizontal_distance)
    return -hr, vr



#for z going up
def get_plane_rotation_standard(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    
    v1_x = x3-x1
    v1_y = y3-y1
    v1_z = z3-z1
    
    v2_x = x2-x1
    v2_y = y2-y1
    v2_z = z2-z1
    
    
    #cp_1 = v1_y*v2_z - v1_z*v2_y
    #cp_2 = v1_z*v2_x - v1_x*v2_z
    #cp_3 = v1_x*v2_y - v1_y*v2_x
    
    x = v1_y*v2_z - v1_z*v2_y
    y = v1_z*v2_x - v1_x*v2_z
    z = v1_x*v2_y - v1_y*v2_x
    
    #a = cp_1
    #b = cp_2
    #c = cp_3
    
    #x = a
    #y = b
    #z = c
    
    hr = get_angle(0,0,x,z)
    
    horizontal_distance = (x**2 + z**2)**.5
    if horizontal_distance == 0:
        if y == 0:
            vr = 0
        elif y > 0:
            vr = math.pi/2
        elif y < 0:
            vr = -math.pi/2
    else:
        vr = math.atan(y/horizontal_distance)
    return hr, vr
def abs(x):
    return x if x >= 0 else -x
def angle_distance(angle1, angle2):
    ret = abs(angle1 - angle2)
    while ret >= math.pi*2:
        ret = ret - math.pi*2
    if ret > math.pi:
        ret = 2*math.pi - ret
    return ret
        
def main():
    hr,vr = get_plane_rotation(0,0,0, 1,0,0, 0,1,1)
    print(hr/math.pi)
    print(vr/math.pi)
def get_angle(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return 0
    elif x1 == x2:
        if y2 > y1:
            return math.pi/2
        else:
            return 3*math.pi/2
        
    ret = math.atan((y2-y1)/(x2-x1))
    if x2 < x1:
        ret = ret + math.pi
    return ret
if __name__ == "__main__": main()
