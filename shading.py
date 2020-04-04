import normal
import math


#maps 0-1 to 87-255 in intervals of 4
#what is the point of this u may ask?
#because the snow textures are 87-255 in intervals of 4
def conv_87_255(x):
    
    if x > 1 or x < 0: raise Exception()
    
    rang = 255-87
    x = 87 + int((x*rang)/4)*4
    
    if x < 91:
        x = 91#just don't return the darkest one either
    if x >= 251:
        x = 251#just please don't return the white square
    return x

#0-255
#scale only specifies the range of the RETURN value
#the INPUT must be 0-255
def apply_color(shade, scale="0-255"):
    r = shade
    g = shade
    b = shade
    
    g += -(((shade-87)/(256-87)-.5)*2)*8#make it a bit orange instead of pure yellow :)
    #b += -(((shade-87)/(256-87)-.5)*2-.6)*22#for the yellow-blue transition
    b += -(((shade-87)/(256-87)-.5)*2-.6)*28#for the yellow-blue transition
    
    
    if r > 255: r = 255
    if r < 0: r = 0
    if g > 255: g = 255
    if g < 0: g = 0
    if b > 255: b = 255
    if b < 0: b = 0
    
    if scale == "0-255":
        return [int(r),int(g),int(b)]
    elif scale == "0-1":
        return [r/255,g/255,b/255]
        
        
        
        
#return 0 to 1
#0 maps to the lowest hill shade texture (91/255) and 1 maps to the highest (251/255)
#so no, 0 is not black, but close to black
def shade_hill(hr, vr, sun_angle):
    def stretch(_0_to_1,min, max):
        return _0_to_1 * (max-min)+min
    sun = sun_angle
    angle_distance_from_sun = normal.angle_distance(hr, sun)/math.pi
    inverse_angle_distance_from_sun = 1 - angle_distance_from_sun
    inverse_angle_distance_from_sun_m1_to_p1 = inverse_angle_distance_from_sun*2-1
    
    vertical_rotation_0_to_1 = vr/(math.pi/2)
    inverse_vertical_rotation_0_to_1 = 1 - vertical_rotation_0_to_1
    
    neutral_floor_color = .5
    extremity = 1
    
    color_value = neutral_floor_color + inverse_angle_distance_from_sun_m1_to_p1*inverse_vertical_rotation_0_to_1*extremity#original shader that doesn't give enough contrast

    if color_value > 1: color_value = 1
    if color_value < 0: color_value = 0
    color_value = stretch(color_value, 0, 1)
    return color_value

#0-1
def hill_shade_to_shadow_color(hill_shade):
    hill_shade = conv_87_255(hill_shade)
    hill_color = apply_color(hill_shade,"0-1")
    for i in range(3):
        hill_color[i] *= .68
    return hill_color
    
    
    
