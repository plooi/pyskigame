
import lift_util
import math

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
def tree_design_3():
    bark = [.6,.3,0]
    trunk_width = .2
    tree_height = 6.5
    t2 = trunk_width/2
    leaf_color = [0,1,0]
    
    leaf_length = 2
    leaf_width = .7
    
    
    
    #hr around the tree, vr up or down, length out, thickenss left to right, height up the tree
    def leaf(hr, vr, length, thickness, height):
        middle_to_corner = ((thickness/2)**2 + length**2)**.5
        angle_middle_to_corner = math.atan(thickness/2 / length)
        
        p = ((math.cos(vr)*length)**2 + (thickness/2)**2)**.5
        pangle = math.atan(thickness/2/(math.cos(vr)*length))
        return [
        
        [math.cos(hr-math.pi/2)*thickness/2, height, -math.sin(hr-math.pi/2)*thickness/2], 
        [math.cos(hr+math.pi/2)*thickness/2, height, -math.sin(hr+math.pi/2)*thickness/2],
        #[math.cos(vr)*math.cos(angle_middle_to_corner+hr)*middle_to_corner, height+sin(vr)*length, -math.cos(vr)*math.sin(angle_middle_to_corner+hr)*middle_to_corner],
        #[math.cos(vr)*math.cos(-angle_middle_to_corner+hr)*middle_to_corner, height+sin(vr)*length, -math.cos(vr)*math.sin(-angle_middle_to_corner+hr)*middle_to_corner],
        [p*cos(hr+pangle),height+sin(vr)*length,-p*sin(hr+pangle)],
        [p*cos(hr-pangle),height+sin(vr)*length,-p*sin(hr-pangle)]
        
        
        ]
    leaf1 = leaf(0,-math.pi/4,leaf_length,leaf_width,4.5)
    leaf2 = leaf(math.pi/3,-math.pi/4,leaf_length,leaf_width,4.5)
    leaf3 = leaf(2*math.pi/3,-math.pi/4,leaf_length,leaf_width,4.5)
    leaf4 = leaf(3*math.pi/3,-math.pi/4,leaf_length,leaf_width,4.5)
    leaf5 = leaf(4*math.pi/3,-math.pi/4,leaf_length,leaf_width,4.5)
    leaf6 = leaf(5*math.pi/3,-math.pi/4,leaf_length,leaf_width,4.5)
    
    leaf11 = leaf(0,-math.pi/4,leaf_length*.8,leaf_width*.8,5.3)
    leaf12 = leaf(math.pi/3,-math.pi/4,leaf_length*.8,leaf_width*.8,5.3)
    leaf13 = leaf(2*math.pi/3,-math.pi/4,leaf_length*.8,leaf_width*.8,5.3)
    leaf14 = leaf(3*math.pi/3,-math.pi/4,leaf_length*.8,leaf_width*.8,5.3)
    leaf15 = leaf(4*math.pi/3,-math.pi/4,leaf_length*.8,leaf_width*.8,5.3)
    leaf16 = leaf(5*math.pi/3,-math.pi/4,leaf_length*.8,leaf_width*.8,5.3)
    
    leaf21 = leaf(0,-math.pi/4,leaf_length*.6,leaf_width*.6,6)
    leaf22 = leaf(math.pi/2,-math.pi/4,leaf_length*.6,leaf_width*.6,6)
    leaf23 = leaf(2*math.pi/2,-math.pi/4,leaf_length*.6,leaf_width*.6,6)
    leaf24 = leaf(3*math.pi/2,-math.pi/4,leaf_length*.6,leaf_width*.6,6)
    
    leaf31 = leaf(0,-math.pi/3,leaf_length*.4,leaf_width*.4,6.8)
    leaf32 = leaf(2*math.pi/3,-math.pi/3,leaf_length*.4,leaf_width*.4,6.8)
    leaf33 = leaf(4*math.pi/3,-math.pi/3,leaf_length*.4,leaf_width*.4,6.8)
    
    return [
        [t2,0,0],[.3*t2,0,-.95*t2],[0,tree_height,0],[0,tree_height,0], bark,
        [.3*t2,0,-.95*t2], [-.8*t2,0,-.58*t2], [0,tree_height,0],[0,tree_height,0], bark,
        [t2,0,0],[.3*t2,0,.95*t2],[0,tree_height,0],[0,tree_height,0], bark,
        [.3*t2,0,.95*t2], [-.8*t2,0,.58*t2], [0,tree_height,0],[0,tree_height,0], bark,
        [-.8*t2,0,-.58*t2], [-.8*t2,0,.58*t2],[0,tree_height,0], [0,tree_height,0], bark,
        
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
def tree_design_1():
    
    
    
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
    A=2.3
    B=2.7
    h1=1.3
    h2=5
    h3=9
    x=.7
    p=.16
    
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
        roof_color = [.7,.7,.7]

    ):
        length *= scale*hscale
        width *= scale*hscale
        height *= scale
        return [
            [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,0,width/2],[-length/2,0,width/2],floor_color,
            [-length/2,height,-width/2],[length/2,height,-width/2],[length/2,height,width/2],[-length/2,height,width/2],roof_color,
            [-length/2,0,-width/2],[length/2,0,-width/2],[length/2,height,-width/2],[-length/2,height,-width/2],wall_color1,
            [-length/2,0,width/2],[length/2,0,width/2],[length/2,height,width/2],[-length/2,height,width/2],wall_color1,
            [-length/2,0,-width/2],[-length/2,0,width/2],[-length/2,height,width/2],[-length/2,height,-width/2],wall_color2,
            [length/2,0,-width/2],[length/2,0,width/2],[length/2,height,width/2],[length/2,height,-width/2],wall_color2,
            
            ]
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
        roof_color1 = [.8,.8,.8],
        roof_color2 = [.9,.9,.9],
        sub_roof_wall_color=[.5,.5,.52],

    ):
        length *= scale*hscale
        width *= scale*hscale
        height *= scale
        
        m = (height-roof_height)/(-length/2-0)
        b = roof_height
        x = -roof_overhang_side - length/2
        height_roof_overhang_side = m*x + b
        #print(height_roof_overhang_side)
        
        
        
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
        
        
        ]

