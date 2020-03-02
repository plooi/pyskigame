
import lift_util
import math
from random import random

from model_3d import *
import models
def tree_design_2():
    tree_width = 2
    tree_height = 9
    color1 = [0,1,0]
    color2 = [0,.9,0]
    
    
    return [
    [-tree_width/2,0,0], [tree_width/2,0,0], [0,tree_height,0], [0,tree_height,0], color1,
    [0,0,-tree_width/2], [0,0,tree_width/2], [0,tree_height,0], [0,tree_height,0], color2,
    
    
    ]
def tree_design_1(shade=.8,scale=1.4):
    bark = "Bark"
    trunk_width = .4*scale#.2
    tree_height = 10*scale#6.5
    t2 = trunk_width/2
    
    
    if shade < .75:
        tex="PineTexture1"
    elif shade < .83:
        tex = "PineTexture2"
    elif shade < .91:
        tex = "PineTexture3"
    else:
        tex="PineTexture4"
    
    leaf_color = tex
    
    #no alpha:
    #leaf_length=5*scale#4
    #leaf_width = 1*scale#.7
    
    #with alpha
    leaf_length = 7*scale
    leaf_width = 2*scale#.7
    
    
    
    
    #hr around the tree, vr up or down, length out, thickenss left to right, height up the tree
    def leaf(hr, vr, length, thickness, height):
        if height > tree_height:
            height = tree_height
        middle_to_corner = ((thickness/2)**2 + length**2)**.5
        angle_middle_to_corner = math.atan(thickness/2 / length)
        
        p = ((math.cos(vr)*length)**2 + (thickness/2)**2)**.5
        pangle = math.atan(thickness/2/(math.cos(vr)*length))
        return [
        
        [math.cos(hr-math.pi/2)*thickness/2, height, -math.sin(hr-math.pi/2)*thickness/2], 
        [math.cos(hr+math.pi/2)*thickness/2, height, -math.sin(hr+math.pi/2)*thickness/2],
        #[math.cos(vr)*math.cos(angle_middle_to_corner+hr)*middle_to_corner, height+sin(vr)*length, -math.cos(vr)*math.sin(angle_middle_to_corner+hr)*middle_to_corner],
        #[math.cos(vr)*math.cos(-angle_middle_to_corner+hr)*middle_to_corner, height+sin(vr)*length, -math.cos(vr)*math.sin(-angle_middle_to_corner+hr)*middle_to_corner],
        [p*cos(hr+pangle+math.pi/4),height+sin(vr)*length,-p*sin(hr+pangle+math.pi/4)],
        [p*cos(hr-pangle),height+sin(vr)*length,-p*sin(hr-pangle)]
        
        
        ]
    """
    leaf1 = leaf(0,-math.pi/3.7,leaf_length,leaf_width,4.5)
    leaf2 = leaf(math.pi/3,-math.pi/3.7,leaf_length,leaf_width,4.5)
    leaf3 = leaf(2*math.pi/3,-math.pi/3.7,leaf_length,leaf_width,4.5)
    leaf4 = leaf(3*math.pi/3,-math.pi/3.7,leaf_length,leaf_width,4.5)
    leaf5 = leaf(4*math.pi/3,-math.pi/3.7,leaf_length,leaf_width,4.5)
    leaf6 = leaf(5*math.pi/3,-math.pi/3.7,leaf_length,leaf_width,4.5)
    
    leaf11 = leaf(0,-math.pi/3.2,leaf_length*.8,leaf_width*.8,5.3)
    leaf12 = leaf(math.pi/3,-math.pi/3.2,leaf_length*.8,leaf_width*.8,5.3)
    leaf13 = leaf(2*math.pi/3,-math.pi/3.2,leaf_length*.8,leaf_width*.8,5.3)
    leaf14 = leaf(3*math.pi/3,-math.pi/3.2,leaf_length*.8,leaf_width*.8,5.3)
    leaf15 = leaf(4*math.pi/3,-math.pi/3.2,leaf_length*.8,leaf_width*.8,5.3)
    leaf16 = leaf(5*math.pi/3,-math.pi/3.2,leaf_length*.8,leaf_width*.8,5.3)
    
    leaf21 = leaf(0,-math.pi/3,leaf_length*.6,leaf_width*.6,6)
    leaf22 = leaf(math.pi/2,-math.pi/3,leaf_length*.6,leaf_width*.6,6)
    leaf23 = leaf(2*math.pi/2,-math.pi/3,leaf_length*.6,leaf_width*.6,6)
    leaf24 = leaf(3*math.pi/2,-math.pi/3,leaf_length*.6,leaf_width*.6,6)
    
    leaf31 = leaf(0,-math.pi/3,leaf_length*.4,leaf_width*.4,6.8)
    leaf32 = leaf(2*math.pi/3,-math.pi/3,leaf_length*.4,leaf_width*.4,6.8)
    leaf33 = leaf(4*math.pi/3,-math.pi/3,leaf_length*.4,leaf_width*.4,6.8)
    
    ret = [
        [t2,0,0],[.3*t2,0,-.95*t2],[0,tree_height,0],[0,tree_height,0], bark,
        [.3*t2,0,-.95*t2], [-.8*t2,0,-.58*t2], [0,tree_height,0],[0,tree_height,0], bark,
        [t2,0,0],[.3*t2,0,.95*t2],[0,tree_height,0],[0,tree_height,0], bark,
        [.3*t2,0,.95*t2], [-.8*t2,0,.58*t2], [0,tree_height,0],[0,tree_height,0], bark,
        [-.8*t2,0,-.58*t2], [-.8*t2,0,.58*t2],[0,tree_height,0], [0,tree_height,0], bark,
        ]
    """
    ret = [
    
    [t2,0,t2],[t2,0,-t2],[-t2,0,-t2],[0,tree_height*.7,0], bark,
    [t2,0,t2],[-t2,0,t2],[-t2,0,-t2],[0,tree_height*.7,0], bark,
    
    ]
    #n = 20
    n=13
    for i in range(n):
        #no alpha texture:
        #ret += leaf(i*2.333*math.pi/3,-math.pi/3 - ( (i/n)**2*.6+.4 )*math.pi/8,leaf_length - ( (i/n)*.6+.4 )*2, leaf_width - ( (i/n)*.6+.4 )*.6,( ((i/n)**2)*.5+.5 ) * (tree_height+1.5))
        
        #with alpha texture
        ret += leaf(random()*1000,-math.pi/3.6 - ( (i/n)**2*.6+.4 )*math.pi/8,leaf_length - ( (i/n)*.6+.4 )*2, leaf_width - ( (i/n)*.6+.4 )*.6,( ((i/n)**1.4)*.5+.5 ) * (tree_height+2.5))
        ret.append(leaf_color)
    return ret
        
        
        
        
        
    [
    leaf1[0], leaf1[1], leaf1[2], leaf1[3], leaf_color,
    leaf2[0], leaf2[1], leaf2[2], leaf2[3], leaf_color,
    leaf3[0], leaf3[1], leaf3[2], leaf3[3], leaf_color,
    leaf4[0], leaf4[1], leaf4[2], leaf4[3], leaf_color,
    leaf5[0], leaf5[1], leaf5[2], leaf5[3], leaf_color,
    leaf6[0], leaf6[1], leaf6[2], leaf6[3], leaf_color,
    
    leaf11[0], leaf11[1], leaf11[2], leaf11[3], leaf_color,
    leaf12[0], leaf12[1], leaf12[2], leaf12[3], leaf_color,
    leaf13[0], leaf13[1], leaf13[2], leaf13[3], leaf_color,
    leaf14[0], leaf14[1], leaf14[2], leaf14[3], leaf_color,
    leaf15[0], leaf15[1], leaf15[2], leaf15[3], leaf_color,
    leaf16[0], leaf16[1], leaf16[2], leaf16[3], leaf_color,
    
    leaf21[0], leaf21[1], leaf21[2], leaf21[3], leaf_color,
    leaf22[0], leaf22[1], leaf22[2], leaf22[3], leaf_color,
    leaf23[0], leaf23[1], leaf23[2], leaf23[3], leaf_color,
    leaf24[0], leaf24[1], leaf24[2], leaf24[3], leaf_color,
    
    leaf31[0], leaf31[1], leaf31[2], leaf31[3], leaf_color,
    leaf32[0], leaf32[1], leaf32[2], leaf32[3], leaf_color,
    leaf33[0], leaf33[1], leaf33[2], leaf33[3], leaf_color,
    
    ]
"""
def tree_design_1():
    bark = [.8,.4,0]
    trunk_width = .2
    tree_height = 9
    t2 = trunk_width/2
    
    leaf_color = [0,1,0]
    
    leaf_radius = .7
    leaf_height_up = 2
    
    
    
    return [
        [-t2,0,0],[t2,0,0],[0,tree_height,0],[0,tree_height,0], bark,
        [0,0,-t2],[0,0,t2],[0,tree_height,0],[0,tree_height,0], bark,
        
        [-leaf_radius,leaf_height_up,-leaf_radius],[0,tree_height,0],[leaf_radius,leaf_height_up,leaf_radius],[-leaf_radius,leaf_height_up,leaf_radius], leaf_color,
        [-leaf_radius,leaf_height_up,-leaf_radius],[0,tree_height,0],[leaf_radius,leaf_height_up,leaf_radius],[leaf_radius,leaf_height_up,-leaf_radius], leaf_color,
        
    
    ]
"""
def tree_design_3(shade=.8, scale = 1):
    
    
    
    """
       
       
       
         ___A
        _____B
          
          
       
         / \                |
        /___\               |
         / \          |     |
        /   \         |     |
       /_____\        |     |
         | |    |     |     |
         |_|    |h1   |h2   |h3
         
          _x
         
          
    """
    A=2.3 * scale
    B=2.7 * scale
    h1=1.3 * scale
    h2=6.5 * scale
    h3=12.5 * scale
    x=.7 * scale
    p=.16 * scale
    
    if shade < .75:
        tex="PineTexture1"
    elif shade < .83:
        tex = "PineTexture2"
    elif shade < .91:
        tex = "PineTexture3"
    else:
        tex="PineTexture4"
    
    
    return [
        [B/2,h1,-B/2],[B/2,h1,B/2],[-B/2,h1,B/2],[0,h3,0],tex,
        [B/2,h1,-B/2],[-B/2,h1,-B/2],[-B/2,h1,B/2],[0,h3,0],tex,
        [-A/2,h2,A/2],[A/2,h2,A/2],[A/2,h2,-A/2],[0,h3,0],tex,
        [-A/2,h2,A/2],[-A/2,h2,-A/2],[A/2,h2,-A/2],[0,h3,0],tex,
        
        
        
        #[-x/2,0,0],[x/2,0,0],[x/2,h1,p],[-x/2,h1,-p],bark,
        [-x/2,0,-x/2+p],[x/2,0,x/2],[-x/2+p,0,-x/2],[0,h3,0],"Bark",
        
    
    ]



def tree_design_2(scale = 1):
    
    
    
    """
       
       
       
         ___A
        _____B
          
          
       
         / \                |
        /___\               |
         / \          |     |
        /   \         |     |
       /_____\        |     |
         | |    |     |     |
         |_|    |h1   |h2   |h3
         
          _x
         
          
    """
    A=2.3 * scale
    B=2.7 * scale
    h1=1.3 * scale
    h2=5 * scale
    h3=9 * scale
    x=.7 * scale
    p=.16 * scale
    
    #leaf_color=[0,.95,.45]
    #leaf_color_bot=[0,.92,.42]
    #leaf_color=[.62,.89,.27]
    #leaf_color_bot=[.52,.79,.17]
    leaf_color=[.62,.99,.27]
    leaf_color_bot=[.52,.89,.17]
    bark = [.6,.3,0]
    
    return [
        [-B/2,h1,-B/2],[-B/2,h1,B/2],[B/2,h1,B/2],[0,h3,0],leaf_color_bot,
        [-B/2,h1,-B/2],[B/2,h1,-B/2],[B/2,h1,B/2],[0,h3,0],leaf_color_bot,
        [-A/2,h2,-A/2],[-A/2,h2,A/2],[A/2,h2,A/2],[0,h3,0],leaf_color,
        [-A/2,h2,-A/2],[A/2,h2,-A/2],[A/2,h2,A/2],[0,h3,0],leaf_color,
        #[-x/2,0,0],[x/2,0,0],[x/2,h1,p],[-x/2,h1,-p],bark,
        [-x/2,0,-x/2+p],[x/2,0,x/2],[-x/2+p,0,-x/2],[0,h3,0],bark,
        
    
    ]














def remove_faces(model, faces):
    for face in faces:
        model[face*5] = [0,0,0]
        model[face*5+1] = [0,0,0]
        model[face*5+2] = [0,0,0]
        model[face*5+3] = [0,0,0]
        model[face*5+4] = [0,0,0]
    return model

"""
BUILDING MODELS
"""
building_models =["cube_building_model","building_with_slanted_roof"]

def cube_building_model(
        scale = 1,
        hscale = 1,
        length = 10,
        width = 10,
        height = 4,
        wall_color1 = [.5,.5,.5],
        wall_color2 = [.6,.6,.6],
        floor_color = [.4,.4,.4],
        roof_color = [.7,.7,.7],
        door_color = [.34,.26,.21],
        door_width = .9,
        door_height = 2,
        door_sep = .1,
        door_bulge = .05,
        face_remove = [],

    ):
        wall_color1 = list(wall_color1)
        wall_color2 = list(wall_color2)
        floor_color = list(floor_color)
        roof_color = list(roof_color)
        door_color = list(door_color)
        length *= scale*hscale
        width *= scale*hscale
        height *= scale
        return remove_faces([
            [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,0,width/2],[-length/2,0,width/2],floor_color,
            [-length/2,height,-width/2],[length/2,height,-width/2],[length/2,height,width/2],[-length/2,height,width/2],roof_color,
            [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,height,-width/2],[-length/2,height,-width/2],wall_color1,
            [-length/2,0,width/2],[length/2,0,width/2],[length/2,height,width/2],[-length/2,height,width/2],wall_color1,
            [-length/2,0,-width/2],[-length/2,0,width/2],[-length/2,height,width/2],[-length/2,height,-width/2],wall_color2,
            [length/2,0,-width/2],[length/2,0,width/2],[length/2,height,width/2],[length/2,height,-width/2],wall_color2,
            [-door_sep/2,0,-door_bulge+width/2],[-door_sep/2-door_width,0,-door_bulge+width/2],[-door_sep/2-door_width,door_height,-door_bulge+width/2],[-door_sep/2,door_height,-door_bulge+width/2],door_color,
            [door_sep/2,0,-door_bulge+width/2],[door_sep/2+door_width,0,-door_bulge+width/2],[door_sep/2+door_width,door_height,-door_bulge+width/2],[door_sep/2,door_height,-door_bulge+width/2],door_color,
            [-door_sep/2,0,door_bulge+width/2],[-door_sep/2-door_width,0,door_bulge+width/2],[-door_sep/2-door_width,door_height,door_bulge+width/2],[-door_sep/2,door_height,door_bulge+width/2],door_color,
            [door_sep/2,0,door_bulge+width/2],[door_sep/2+door_width,0,door_bulge+width/2],[door_sep/2+door_width,door_height,door_bulge+width/2],[door_sep/2,door_height,door_bulge+width/2],door_color,
            ], face_remove)
        
def default(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
def building_with_slanted_roof_tex(**args):
    default(args, "wall_color1", "BuildingStoneTexture")
    default(args, "wall_color2", "BuildingStoneTexture")
    default(args, "floor_color", "BuildingWoodTexture")
    default(args, "roof_color1", "BuildingWoodTexture2")
    default(args, "roof_color2", "BuildingWoodTexture2")
    default(args, "sub_roof_wall_color", "BuildingWoodTexture")
    default(args, "door_color", "DoorTexture")
    return building_with_slanted_roof(**args)
def building_with_slanted_roof(
        scale = 1,
        hscale = 1,
        length = 10,
        width = 10,
        height = 4,
        roof_height = 6,
        roof_overhang_front = 1,
        roof_overhang_side = 1,
        wall_color1 = [.5,.5,.5],
        wall_color2 = [.6,.6,.6],
        floor_color = [.4,.45,.4],
        roof_color1 = [.7,.7,.7],
        roof_color2 = [.55,.55,.55],
        sub_roof_wall_color=[.5,.5,.52],
        door_color = [.34,.26,.21],
        door_width = .9,
        door_height = 2,
        door_sep = .1,
        door_bulge = .05,
        face_remove = [],

    ):
        length *= scale*hscale
        width *= scale*hscale
        height *= scale
        
        m = (height-roof_height)/(-length/2-0)
        b = roof_height
        x = -roof_overhang_side - length/2
        height_roof_overhang_side = m*x + b
        #print(height_roof_overhang_side)
        if isinstance(wall_color1, list):
            wall_color1 = list(wall_color1)
            wall_color2 = list(wall_color2)
            floor_color = list(floor_color)
            roof_color1 = list(roof_color1)
            roof_color2 = list(roof_color2)
            sub_roof_wall_color=list(sub_roof_wall_color)
            door_color = list(door_color)
        
        if len(face_remove) == 0:
            return [
                [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,0,width/2],[-length/2,0,width/2],floor_color,
                [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,height,-width/2],[-length/2,height,-width/2],wall_color1,
                [-length/2,0,width/2],[length/2,0,width/2],[length/2,height,width/2],[-length/2,height,width/2],wall_color1,
                [-length/2,0,-width/2],[-length/2,0,width/2],[-length/2,height,width/2],[-length/2,height,-width/2],wall_color2,
                [length/2,0,-width/2],[length/2,0,width/2],[length/2,height,width/2],[length/2,height,-width/2],wall_color2,
                [-length/2-roof_overhang_side, height_roof_overhang_side, -width/2-roof_overhang_front],[-length/2-roof_overhang_side, height_roof_overhang_side, width/2+roof_overhang_front],[0,roof_height,width/2+roof_overhang_front],[0,roof_height,-width/2-roof_overhang_front],roof_color1,
                [length/2+roof_overhang_side, height_roof_overhang_side, -width/2-roof_overhang_front],[length/2+roof_overhang_side, height_roof_overhang_side, width/2+roof_overhang_front],[0,roof_height,width/2+roof_overhang_front],[0,roof_height,-width/2-roof_overhang_front],roof_color1,
                [-length/2,height,-width/2],[length/2,height,-width/2],[0,roof_height,-width/2],[0,roof_height,-width/2],sub_roof_wall_color,
                [-length/2,height,width/2],[length/2,height,width/2],[0,roof_height,width/2],[0,roof_height,width/2],sub_roof_wall_color,
                [-door_sep/2,0,-door_bulge+width/2],[-door_sep/2-door_width,0,-door_bulge+width/2],[-door_sep/2-door_width,door_height,-door_bulge+width/2],[-door_sep/2,door_height,-door_bulge+width/2],door_color,
                [door_sep/2,0,-door_bulge+width/2],[door_sep/2+door_width,0,-door_bulge+width/2],[door_sep/2+door_width,door_height,-door_bulge+width/2],[door_sep/2,door_height,-door_bulge+width/2],door_color,
                [-door_sep/2,0,door_bulge+width/2],[-door_sep/2-door_width,0,door_bulge+width/2],[-door_sep/2-door_width,door_height,door_bulge+width/2],[-door_sep/2,door_height,door_bulge+width/2],door_color,
                [door_sep/2,0,door_bulge+width/2],[door_sep/2+door_width,0,door_bulge+width/2],[door_sep/2+door_width,door_height,door_bulge+width/2],[door_sep/2,door_height,door_bulge+width/2],door_color,
            ]
        else:
            return remove_faces([
                [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,0,width/2],[-length/2,0,width/2],floor_color,
                [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,height,-width/2],[-length/2,height,-width/2],wall_color1,
                [-length/2,0,width/2],[length/2,0,width/2],[length/2,height,width/2],[-length/2,height,width/2],wall_color1,
                [-length/2,0,-width/2],[-length/2,0,width/2],[-length/2,height,width/2],[-length/2,height,-width/2],wall_color2,
                [length/2,0,-width/2],[length/2,0,width/2],[length/2,height,width/2],[length/2,height,-width/2],wall_color2,
                [-length/2-roof_overhang_side, height_roof_overhang_side, -width/2-roof_overhang_front],[-length/2-roof_overhang_side, height_roof_overhang_side, width/2+roof_overhang_front],[0,roof_height,width/2+roof_overhang_front],[0,roof_height,-width/2-roof_overhang_front],roof_color1,
                [length/2+roof_overhang_side, height_roof_overhang_side, -width/2-roof_overhang_front],[length/2+roof_overhang_side, height_roof_overhang_side, width/2+roof_overhang_front],[0,roof_height,width/2+roof_overhang_front],[0,roof_height,-width/2-roof_overhang_front],roof_color1,
                [-length/2,height,-width/2],[length/2,height,-width/2],[0,roof_height,-width/2],[0,roof_height,-width/2],sub_roof_wall_color,
                [-length/2,height,width/2],[length/2,height,width/2],[0,roof_height,width/2],[0,roof_height,width/2],sub_roof_wall_color,
                [-door_sep/2,0,-door_bulge+width/2],[-door_sep/2-door_width,0,-door_bulge+width/2],[-door_sep/2-door_width,door_height,-door_bulge+width/2],[-door_sep/2,door_height,-door_bulge+width/2],door_color,
                [door_sep/2,0,-door_bulge+width/2],[door_sep/2+door_width,0,-door_bulge+width/2],[door_sep/2+door_width,door_height,-door_bulge+width/2],[door_sep/2,door_height,-door_bulge+width/2],door_color,
                [-door_sep/2,0,door_bulge+width/2],[-door_sep/2-door_width,0,door_bulge+width/2],[-door_sep/2-door_width,door_height,door_bulge+width/2],[-door_sep/2,door_height,door_bulge+width/2],door_color,
                [door_sep/2,0,door_bulge+width/2],[door_sep/2+door_width,0,door_bulge+width/2],[door_sep/2+door_width,door_height,door_bulge+width/2],[door_sep/2,door_height,door_bulge+width/2],door_color,
            ], face_remove)











def bump_model_1(
            diagonal_length=15,
            diagonal_depth=22,
            height = 1.1,
            base=-4.6,
            downhill_height = -6.5,
            uphill_height = 1.4,
            angle_distance_from_sun = 0,
            sun_is_to_the_left = True,
            ):
    if angle_distance_from_sun < math.pi/5:
        tex1 = "BumpTextureL"
        tex2 = "BumpTextureL"
    elif angle_distance_from_sun < 4*math.pi/5:
        if sun_is_to_the_left:
            tex1 = "BumpTextureL"
            tex2 = "BumpTextureD"
        else:
            tex1 = "BumpTextureD"
            tex2 = "BumpTextureL"
    else:
        tex1 = "BumpTextureD"
        tex2 = "BumpTextureD"
        
    
    d = diagonal_length
    dd = diagonal_depth
    return [
            [-d/2, uphill_height, 0],[0, base, -dd/2],[d/2, downhill_height, 0],[0,height,0],tex1,
            [-d/2, uphill_height, 0],[0, base, dd/2],[d/2, downhill_height, 0],[0,height,0],tex2,
            [0,height,0],[-.1,height,0],[-.1,height+.4,0],[0,height+.4,0],"White",
            ]
def bump_model_4(
            diagonal_length=15,
            diagonal_depth=22,
            height = 1.1,
            base=-4.6,
            downhill_height = -6.5,
            uphill_height = 1.4,
            angle_distance_from_sun = 0,
            sun_is_to_the_left = True,
            ):
    if angle_distance_from_sun < math.pi/5:
        tex1 = "BumpTextureL"
        tex2 = "BumpTextureL"
    elif angle_distance_from_sun < 4*math.pi/5:
        if sun_is_to_the_left:
            tex1 = "BumpTextureL"
            tex2 = "BumpTextureD"
        else:
            tex1 = "BumpTextureD"
            tex2 = "BumpTextureL"
    else:
        tex1 = "BumpTextureD"
        tex2 = "BumpTextureD"
        
    
    d = diagonal_length
    dd = diagonal_depth
    return [
            [-d/2, uphill_height, 0],[0, base, -dd/2],[d/2, downhill_height, 0],[0,height,0],tex1,
            [-d/2, uphill_height, 0],[0, base, dd/2],[d/2, downhill_height, 0],[0,height,0],tex2,
            ]
def bump_model_3(
            diagonal_length=12,
            height = 1.1,
            base=-4.6,
            downhill_height = -4.9,
            uphill_height = 1.1,
            angle_distance_from_sun = 0,
            sun_is_to_the_left = True,
            ):
    if angle_distance_from_sun < math.pi/5:
        tex1 = "MinecraftSnow-lighting-243"
        tex2 = "MinecraftSnow-lighting-243"
    elif angle_distance_from_sun < 4*math.pi/5:
        if sun_is_to_the_left:
            tex1 = "MinecraftSnow-lighting-231"
            tex2 = "MinecraftSnow-lighting-211"
        else:
            tex1 = "MinecraftSnow-lighting-211"
            tex2 = "MinecraftSnow-lighting-231"
    else:
        tex1 = "MinecraftSnow-lighting-223"
        tex2 = "MinecraftSnow-lighting-223"
        
    
    d = diagonal_length
    return [
            [-d/2, uphill_height, 0],[0, base, -d/2],[d/2, downhill_height, 0],[0,height,0],tex1,
            [-d/2, uphill_height, 0],[0, base, d/2],[d/2, downhill_height, 0],[0,height,0],tex2,
            ]

#original model, just exists for backward compatibility purposes
def bump_model_2(
            diagonal_length=12,
            height = 1.1,
            base=-4.6,
            downhill_height = -4.9,
            uphill_height = 1.1
            ):
    color1 = [.95,.95,.95]
    color2 = [.91,.91,.91]
    d = diagonal_length
    return [
            [-d/2, uphill_height, 0],[0, base, -d/2],[d/2, downhill_height, 0],[0,height,0],color1,
            [-d/2, uphill_height, 0],[0, base, d/2],[d/2, downhill_height, 0],[0,height,0],color2,
            
        ]




def landmark_model_1(
    width=.4,
    height=14,
    square_diagonal = 2.2):
    pole_color = [0,0,0]
    square_color = [0,.9,0]
    
    return [
        [-width/2,0,-width/2],[width/2,0,-width/2],[width/2,height,-width/2],[-width/2,height,-width/2],[1,1,1],[1,1,1],[.5,0,.5],[.5,0,.5],
        [-width/2,0,width/2],[width/2,0,width/2],[width/2,height,width/2],[-width/2,height,width/2],[1,1,1],[1,1,1],[.5,0,.5],[.5,0,.5],
        [-width/2,0,-width/2],[-width/2,0,width/2],[-width/2,height,width/2],[-width/2,height,-width/2],[1,1,1],[1,1,1],[.5,0,.5],[.5,0,.5],
        [width/2,0,-width/2],[width/2,0,width/2],[width/2,height,width/2],[width/2,height,-width/2],[1,1,1],[1,1,1],[.5,0,.5],[.5,0,.5],
        #[0,height-square_diagonal/2,0],[0,height,square_diagonal/2],[0,height+square_diagonal/2,0],[0,height,-square_diagonal/2],square_color,
    
    
    
    ]
    
"""
def terminal_design_2(
    pole_length = 1,
    pole_width = .6,
    pole_height = 2,
    pole_color = [.3,.3,.3],
    
    terminal_roof_width = 4,
    terminal_roof_length = 7,
    terminal_track_indent = .5,
    terminal_belly_color = [.8,.7,.5],
    terminal_roof_color = [.4,.4,.8],
    terminal_wall_color = [.2,.2,.8],
    
    rope_speed = 3,
    terminal_speed = 1,
    bullwheel_distance_from_pole = 2,
    slow_down_segments = 15,
    bullwheel_segments = 55,
    
    terminal_roof_height = 1.5,
    terminal_roof_height2 = 1.2
    
    
    ):
    
    bullwheel_radius = terminal_roof_width/2-terminal_track_indent
    track = lift_util.Track()
    
    speed_diff = rope_speed-terminal_speed
    
    for x in range(0, slow_down_segments):
        percent_round_down = x/slow_down_segments
        percent_round_up = x/(slow_down_segments-1) if slow_down_segments > 1 else 1
        x_pos = (1 - percent_round_down) * terminal_roof_length/2 
        vel = terminal_speed + (1 - percent_round_up) * speed_diff
        track.add_point(lift_util.Point(x_pos, pole_height, -terminal_roof_width/2+terminal_track_indent, vel))
    for bws in range(0, bullwheel_segments+1):
        theta = bws / bullwheel_segments * math.pi + math.pi/2
        z = -math.sin(theta) * bullwheel_radius
        x = math.cos(theta) * bullwheel_radius
        x -= bullwheel_distance_from_pole
        track.add_point(lift_util.Point(x, pole_height, z, terminal_speed))
    for x in range(0, slow_down_segments):
        percent_round_down = x/slow_down_segments
        percent_round_up = x/(slow_down_segments-1) if slow_down_segments > 1 else 1
        x_pos = (percent_round_up) * terminal_roof_length/2 
        vel = terminal_speed + (percent_round_up) * speed_diff
        track.add_point(lift_util.Point(x_pos, pole_height, terminal_roof_width/2-terminal_track_indent, vel))
    #WORKING HERE
    return [
    [-pole_length/2,0,-pole_width/2], [pole_length/2,0,-pole_width/2], [pole_length/2,pole_height,-pole_width/2], [-pole_length/2,pole_height,-pole_width/2], pole_color,
    [-pole_length/2,0,pole_width/2], [pole_length/2,0,pole_width/2], [pole_length/2,pole_height,pole_width/2], [-pole_length/2,pole_height,pole_width/2], pole_color,
    [-pole_length/2,0,-pole_width/2], [-pole_length/2,0,pole_width/2], [-pole_length/2,pole_height,pole_width/2], [-pole_length/2,pole_height,-pole_width/2], pole_color,
    [pole_length/2,0,-pole_width/2], [pole_length/2,0,pole_width/2], [pole_length/2,pole_height,pole_width/2], [pole_length/2,pole_height,-pole_width/2], pole_color,
    
    [-terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height, terminal_roof_width/2], [-terminal_roof_length/2, pole_height, terminal_roof_width/2], terminal_belly_color,
    
    [-terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + terminal_roof_width/5], terminal_roof_color,
    [-terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 2*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 2*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + terminal_roof_width/5], terminal_roof_color,
    [-terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 2*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 2*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 3*terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 3*terminal_roof_width/5], terminal_roof_color,
    [-terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + 4*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + 4*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 3*terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2 + 3*terminal_roof_width/5], terminal_roof_color,
    [-terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + 4*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2 + 4*terminal_roof_width/5], [terminal_roof_length/2, pole_height, terminal_roof_width/2], [-terminal_roof_length/2, pole_height, terminal_roof_width/2], terminal_roof_color,
    
    [-terminal_roof_length/2, pole_height, -terminal_roof_width/2], [-terminal_roof_length/2, pole_height, terminal_roof_width/2], [-terminal_roof_length/2, pole_height+terminal_roof_height2, terminal_roof_width/2-terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2+terminal_roof_width/5], terminal_wall_color,
    [-terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2+2*terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height, terminal_roof_width/2-2*terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height2, terminal_roof_width/2-terminal_roof_width/5], [-terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2+terminal_roof_width/5], terminal_wall_color,
    [terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height, terminal_roof_width/2], [terminal_roof_length/2, pole_height+terminal_roof_height2, terminal_roof_width/2-terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2+terminal_roof_width/5], terminal_wall_color,
    [terminal_roof_length/2, pole_height+terminal_roof_height, -terminal_roof_width/2+2*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height, terminal_roof_width/2-2*terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height2, terminal_roof_width/2-terminal_roof_width/5], [terminal_roof_length/2, pole_height+terminal_roof_height2, -terminal_roof_width/2+terminal_roof_width/5], terminal_wall_color,
    ], track
    
    
"""
