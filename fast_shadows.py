import numpy as np
from numba import jit
import shading
import shadow_map
import math
import loading
#adds shadows of all the trees in trees array to the given world
def add_shadows(world, trees):
    loading.progress_bar("Loading terrain...")
    loading.update(1)
    
    
    elevations = []
    
    hs = world.properties["horizontal_stretch"]
    vs = world.properties["vertical_stretch"]
    sa = world.properties["sun_angle"]
    #print("start")
    for z in range(world.get_height_points()):
        row = []
        for x in range(world.get_width_points()):
            row.append(world.get_elevation(z,x))
        elevations.append(row)
    elevations = np.array(elevations)
    
    
    #print("stop")
    
    
    trees_num_arr = []
    
    for tree in trees:
        trees_num_arr.append([tree.args["model_z"],tree.args["model_x"],tree.args["model_args"]["height"]])
    trees_num_arr = np.array(trees_num_arr)
    
    
    #print(elevations)
    #print(elevations.shape)
    
    #print(trees_num_arr)
    #print(trees_num_arr.shape)
    
    
    shadow_additions = get_shadow_additions(elevations, trees_num_arr, hs, vs, world.properties["sun_angle"])
    
    if len(shadow_additions) != len(trees):
        raise ("wtf")
    
    for i in range(len(shadow_additions)):
        tree = trees[i]
        tree.add_shadow(shadow_additions[i][0], shadow_additions[i][1])
#args
#    elevations (in the form of a 2d array, where elevations[z][x] = the world's unscaled elevation at point z,x 
#    trees_num_arr where each element of the array is a 3 length array denoting the real_z(scaled) and real_x(scaled) position and height of the tree
#    hs, vs is horizontal stretch and vertical stretch
#    must be numpy arrays
#this function returns a list where each element is a 2 length tuple, where the first is a numpy
#array of vertices and the second is a numpy array of colors
#the vertices and colors of element i is the ith tree's shadow vertices and colors
def main():
    from time import time
    e = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
    x = (get_shadow_additions(e, np.array([[2,2,10],[3,3,10],[4,4,10],[2,1,10],[1,4,10]]), 1,1,0))
    start = time()
    x = (get_shadow_additions(e, np.array([[2,2,10],[3,3,10],[4,4,10],[2,1,10],[1,4,10]]*1000), 1,1,0))
    print("took",time() - start)
    #print(x)
    #print(get_elevation_continuous(e, .99,.99,1,.1))

def get_shadow_additions(elevations, trees_num_arr, hs, vs, sun_angle):
    
    
    ret = []
    
    sa = sun_angle
    
    
    
    
    for i in range(len(trees_num_arr)):
        
        
        
        zxheight = trees_num_arr[i]
        z = zxheight[0]
        x = zxheight[1]
        height = zxheight[2]
        
        
        
        #calculate the triangle that the shadow exists in
        s_base = 3*shadow_map.D
        s_height = 12*height/10  *shadow_map.D#
        
        x1 = s_base*math.cos(sa+math.pi/2)
        z1 = s_base*-math.sin(sa+math.pi/2)
        
        x2 = s_base*math.cos(sa-math.pi/2)
        z2 = s_base*-math.sin(sa-math.pi/2)
        
        x3 = s_height*math.cos(sa+math.pi)
        z3 = s_height*-math.sin(sa+math.pi)
        
        z_offset = z*shadow_map.D
        x_offset = x*shadow_map.D
        
        z1+= z_offset
        x1+= x_offset
        z2+= z_offset
        x2+= x_offset
        z3+= z_offset
        x3+= x_offset
        
        #triangle now exists as x1z1,x2z2,x3z3
        
        
        
        
        #NEXT PART: add a shadow according to that triangle
        
        #find min and max, z and x    
        min_z = int(mn(z1,z2,z3))
        min_x = int(mn(x1,x2,x3))
        max_z = int(mx(z1,z2,z3))
        max_x = int(mx(x1,x2,x3))
        #print(min_z, max_z)
        #print(x1,x2,x3)
        #print(max_x,min_x)
        num_shadows = 0
        #count how many shadows in the triangle
        for shadow_z in range(min_z, max_z):
            for shadow_x in range(min_x, max_x):
                if is_inside(shadow_z,shadow_x,z1,x1,z2,x2,z3,x3):
                    num_shadows += 1
        
        vertices = np.empty((num_shadows*4,3))#xyz
        colors = np.empty((num_shadows*4,3))#rgb
        
        
        add_triangle_shadow(min_z,max_z,min_x,max_x,z1,x1,z2,x2,z3,x3,hs,vs,vertices,colors,elevations,sun_angle)
        #add_triangle_shadow(min_z,max_z,min_x,max_x,z1,x1,z2,x2,z3,x3,hs,vs,vertices,colors,elevations,sa):
        
        #print("ret",ret)
        #print("vert",vertices)
        ret.append((vertices,colors))
        
        if i %5 == 0:
            loading.update(i/len(trees_num_arr) * 100)
        
    loading.update(100)
    return ret
@jit
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
@jit
def get_plane_rotation(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    
    v1_x = x3-x1
    v1_y = y3-y1
    v1_z = z3-z1
    
    v2_x = x2-x1
    v2_y = y2-y1
    v2_z = z2-z1
    
    x = v1_y*v2_z - v1_z*v2_y
    y = v1_z*v2_x - v1_x*v2_z
    z = v1_x*v2_y - v1_y*v2_x
    
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
@jit
def angle_distance(angle1, angle2):
    ret = abs(angle1 - angle2)
    while ret >= math.pi*2:
        ret = ret - math.pi*2
    if ret > math.pi:
        ret = 2*math.pi - ret
    return ret
@jit
def shade_hill(hr, vr, sun_angle):
    def stretch(_0_to_1,min, max):
        return _0_to_1 * (max-min)+min
    sun = sun_angle
    angle_distance_from_sun = angle_distance(hr, sun)/math.pi
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
@jit
def apply_color(shade):
    r = shade
    g = shade
    b = shade
    b -= 20 * ((shade)/255)**3
    b += 45 * ((255-shade)/255)**2#42 * ((255-shade)/255)**3
    r -= 15 * ((255-shade)/255)**2
    
    if r > 255: r = 255
    if r < 0: r = 0
    if g > 255: g = 255
    if g < 0: g = 0
    if b > 255: b = 255
    if b < 0: b = 0
    ret = np.empty((3,))
    ret[0]=r/255
    ret[1]=g/255
    ret[2]=b/255
    return ret
@jit
def conv_87_255(x):
    rang = 255-87
    x = 87 + int((x*rang)/4)*4
    
    if x < 91:
        x = 91#just don't return the darkest one either
    if x >= 251:
        x = 251#just please don't return the white square
    return x
@jit
def hill_shade_to_shadow_color(hill_shade):
    hill_shade = conv_87_255(hill_shade)
    hill_color = apply_color(hill_shade)
    for i in range(3):
        hill_color[i] *= .68
    return hill_color
@jit
def add_triangle_shadow(min_z,max_z,min_x,max_x,z1,x1,z2,x2,z3,x3,hs,vs,vertices,colors,elevations,sa):
    #for each shadow in this tree
    
    height = elevations.shape[0]
    width = elevations.shape[1]
    
    
    j = 0
    for shadow_z in range(min_z, max_z):
        for shadow_x in range(min_x, max_x):
            if is_inside(shadow_z,shadow_x,z1,x1,z2,x2,z3,x3):
                #add a shadow to vertices and colors for shadow_z and shadow_x
                real_z1 = shadow_z/shadow_map.D
                real_x1 = shadow_x/shadow_map.D
                real_z2 = real_z1 + 1/shadow_map.D
                real_x2 = real_x1 + 1/shadow_map.D
                
                #print("a")
                unscaled_z = int((real_z1+real_z2)/2/hs)
                unscaled_x = int((real_x1+real_x2)/2/hs)
                #print("b")
                #calculate shadow color
                
                
                
                
                if unscaled_z+1 < height and unscaled_x+1 < width:
                    y1 = elevations[unscaled_z][unscaled_x]*vs
                    y2 = elevations[unscaled_z][unscaled_x+1]*vs
                    y3 = elevations[unscaled_z+1][unscaled_x+1]*vs
                    y4 = elevations[unscaled_z+1][unscaled_x]*vs
                    
                    #print("c")
                    
                    
                    shadow_color = hill_shade_to_shadow_color(shade_hill(*get_plane_rotation(0,y1,0,hs,y2,0,0,y4,hs),sa))
                    
                    #shadow_color = np.zeros(3)#hill_shade_to_shadow_color(shade_hill(*get_plane_rotation(0,y1,0,hs,y2,0,0,y4,hs),sa))
                    
                    
                    #shadow_color = #shadow_colors[unscaled_z][unscaled_x]#np.copy(shadow_colors[unscaled_z][unscaled_x])
                    
                    
                    
                    #print("d")
                    
                    
                    #add shadow to vertices and colors
                    vertices[j][0] = real_x1
                    vertices[j][1] = get_elevation_continuous(elevations, real_z1, real_x1, hs, vs) + shadow_map.shadow_margin
                    vertices[j][2] = real_z1
                    colors[j][0] = shadow_color[0]
                    colors[j][1] = shadow_color[1]
                    colors[j][2] = shadow_color[2]
                    
                    j+=1
                    vertices[j][0] = real_x2
                    vertices[j][1] = get_elevation_continuous(elevations, real_z1, real_x2, hs, vs) + shadow_map.shadow_margin
                    vertices[j][2] = real_z1
                    colors[j][0] = shadow_color[0]
                    colors[j][1] = shadow_color[1]
                    colors[j][2] = shadow_color[2]
                    
                    j+=1
                    vertices[j][0] = real_x2
                    vertices[j][1] = get_elevation_continuous(elevations, real_z2, real_x2, hs, vs) + shadow_map.shadow_margin
                    vertices[j][2] = real_z2
                    colors[j][0] = shadow_color[0]
                    colors[j][1] = shadow_color[1]
                    colors[j][2] = shadow_color[2]
                    
                    j+=1
                    vertices[j][0] = real_x1
                    vertices[j][1] = get_elevation_continuous(elevations, real_z2, real_x1, hs, vs) + shadow_map.shadow_margin
                    vertices[j][2] = real_z2
                    colors[j][0] = shadow_color[0]
                    colors[j][1] = shadow_color[1]
                    colors[j][2] = shadow_color[2]
                    
                    j+=1
                    #print("e")
@jit
def get_elevation_continuous(unscaled_elevations, real_z, real_x, hs, vs):
    
    
    z = real_z/hs#unscaled, but fractional
    x = real_x/hs
    
    shape = unscaled_elevations.shape
    if z < 0 or z >= shape[0]-1 or x < 0 or x >= shape[1]-1: return -9999999
    
    fracz = z % 1
    fracx = x % 1
    if fracz+fracx < 1:
        #upper left triangle
        ul = int(x), unscaled_elevations[int(z)][int(x)], int(z)
        ur = int(x)+1, unscaled_elevations[int(z)][int(x)+1], int(z)
        ll = int(x), unscaled_elevations[int(z)+1][int(x)], int(z)+1
        xrise = ur[1] - ul[1]
        zrise = ll[1] - ul[1]
        
        y = fracx*xrise + fracz*zrise + ul[1]
        
    else:
        #upper right triangle
        lr = int(x)+1, unscaled_elevations[int(z)+1][int(x)+1], int(z)+1
        ur = int(x)+1, unscaled_elevations[int(z)][int(x)+1], int(z)
        ll = int(x), unscaled_elevations[int(z)+1][int(x)], int(z)+1
        
        
        xrise = ll[1] - lr[1]
        zrise = ur[1] - lr[1]
        
        y = (1-fracx)*xrise + (1-fracz)*zrise + lr[1]
    return y * vs
@jit
def mn(a,b,c):
    if a <= b and a <= c: return a
    if b <= a and b <= c: return b
    return c
@jit
def mx(a,b,c):
    if a >= b and a >= c: return a
    if b >= a and b >= c: return b
    return c
@jit
def about(a,b):
    return a + .01 > b and a - .01 < b
@jit
def abs(x):return x if x > 0 else -x
@jit
def area(z1,x1,z2,x2,z3,x3):
    return abs( (z1*(x2-x3) + z2*(x3-x1) + z3*(x1-x2))/2 )
@jit
def is_inside(x,y,x1,y1,x2,y2,x3,y3):
    A = area (x1, y1, x2, y2, x3, y3) 
    A1 = area (x, y, x2, y2, x3, y3) 
    A2 = area (x1, y1, x, y, x3, y3)
    A3 = area (x1, y1, x2, y2, x, y)
    return about(A , (A1 + A2 + A3))
    
    
if __name__ == "__main__": main()
    
    

    
    
    
    
    
    
