
import lift_util
import math

from model_3d import *
from models2 import *




def find_name(model):
    m = model
    if m is chair_model_1: return "chair_model_1"
    if m is chair_model_2: return "chair_model_2"
    if m is chair_model_3: return "chair_model_3"
    if m is chair_model_4: return "chair_model_4"
    
    if m is double_model_1: return "double_model_1"
    if m is double_model_2: return "double_model_2"
    if m is double_model_3: return "double_model_3"
    
    if m is triple_model_1: return "triple_model_1"
    if m is triple_model_2: return "triple_model_2"
    if m is triple_model_3: return "triple_model_3"
    
    if m is tbar_model_1: return "tbar_model_1"
    
    if m is sixpack_model_1: return "sixpack_model_1"
    if m is sixpack_model_2: return "sixpack_model_2"
    if m is sixpack_model_3: return "sixpack_model_3"
    
    if m is gondola_model_1: return "gondola_model_1"
    if m is gondola_model_2: return "gondola_model_2"
    if m is gondola_model_3: return "gondola_model_3"
    if m is gondola_model_4: return "gondola_model_4"
    
    if m is terminal_design_1: return "terminal_design_1"
    if m is terminal_design_2: return "terminal_design_2"
    
    if m is pole_design_1: return "pole_design_1"
    if m is pole_design_2: return "pole_design_2"
    
    if m is tree_design_1: return "tree_design_1"
    if m is tree_design_2: return "tree_design_2"
    if m is rock_design_1:return "rock_design_1"
    if m is rock_design_2:return "rock_design_2"
    
    if m is gondola_model_1_riding: return "gondola_model_1_riding"
    
    if m is cube_building_model: return "cube_building_model"
    if m is building_with_slanted_roof:return "building_with_slanted_roof"
    
    raise Exception("Cannot determine name of this model: " + str(model()))














"""
High speed quad chair models
"""
def chair_model_1():
    return [
        [0,-.5,-.5], [0,.5,-.5], [0,.5,.5], [0,-.5,.5], [0,0,0]
    ]
def chair_model_2(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    seat_back_color = [.1,.1,.1],
    seat_color = [.2,.2,.2],
    
    chair_width = 1.2,
    sub_hanger_height = .5,
    chair_slouch=.2,
    seat_width = .2,
    
    seat_back_height=.2,
    
    seat_tilt_up = .07):
    
    
    h_2 = hanger_width/2
    return [
        [0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        [0,-hanger_height,-chair_width/2], [0,-hanger_height,chair_width/2], [0,-hanger_height-hanger_width,chair_width/2], [0,-hanger_height-hanger_width,-chair_width/2], hanger_color,
        [0,-hanger_height-hanger_width,-chair_width/2], [0,-hanger_height-hanger_width,-chair_width/2+hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2+hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2], hanger_color,
        [0,-hanger_height-hanger_width,chair_width/2], [0,-hanger_height-hanger_width,chair_width/2-hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2-hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2], hanger_color,
        [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,chair_width/2], seat_back_color,
        [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,-chair_width/2], [seat_width,-hanger_height-hanger_width-sub_hanger_height-seat_back_height+seat_tilt_up,-chair_width/2], [seat_width,-hanger_height-hanger_width-sub_hanger_height-seat_back_height+seat_tilt_up,chair_width/2], seat_color
        
        
    ]
def chair_model_3(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    seat_back_color = [.1,.1,.1],
    seat_color = [.2,.2,.2],
    
    chair_width = 1.2,
    sub_hanger_height = .5,
    chair_slouch=.2,
    seat_width = .2,
    
    seat_back_height=.2,
    
    seat_tilt_up = .07):
    
    h_2 = hanger_width/2
    return [
        [0,-hanger_height,-chair_width/2], [0,-hanger_height,chair_width/2], [0,-hanger_height-hanger_width,chair_width/2], [0,-hanger_height-hanger_width,-chair_width/2], hanger_color,
        [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,chair_width/2], seat_back_color,

        
    ]
def chair_model_4(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    seat_back_color = [.1,.1,.1],
    seat_color = [.2,.2,.2],
    
    chair_width = 1.2,
    sub_hanger_height = .5,
    chair_slouch=.2,
    seat_width = .2,
    
    seat_back_height=.2,
    
    seat_tilt_up = .07):
    
    h_2 = hanger_width/2
    return [
        
        [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,chair_width/2], seat_back_color,

        
    ]
    
#Gondola  models

"""
          ___
depth/   /to/\
    /   /_p/  \
       /   \        |h1
      / door\       |
      \side /             |h2
       \___/              |
            
           __
           bulge
           
        ___
        width
        
    """
    
"""
    
                    ___________
                   /  /        \
                  /  /          \
                 /  /            \
                 \               /
                  \             /
                   \___________/
    
    
    
    
    
    """
def gondola_model_1(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    top_color = [.2,.3,.2],
    bottom_color =[.5,.5,.5],
    side_color = [.2,.3,.2],
    side_color_up = [.15,.15,.15],
    side_color_up2 = [.16,.16,.16],
    front_color = [.3,.4,.3],
    front_color_up = [.17,.17,.17],
    depth = 1,
    width = 1,
    bulge = .11,
    front_bulge = .11,
    h1 = .5,
    h2 = .5):
    
    
    
    h_2 = hanger_width/2
    return [
        [0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        [-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2,-hanger_height,depth/2], [-width/2,-hanger_height,depth/2], top_color,
        [-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,depth/2], [-width/2,-hanger_height-h1-h2,depth/2], bottom_color,
        
        [-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color_up,
        [-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color,
        
        [-width/2,-hanger_height,depth/2], [width/2,-hanger_height,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color_up2,
        [-width/2,-hanger_height-h1-h2,depth/2], [width/2,-hanger_height-h1-h2,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height-h1-h2, depth/2], [width/2,-hanger_height-h1-h2, -depth/2], front_color,
        [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height-h1-h2, depth/2], [-width/2,-hanger_height-h1-h2, -depth/2], front_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height, depth/2], [width/2,-hanger_height, -depth/2], front_color_up,
        [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height, depth/2], [-width/2,-hanger_height, -depth/2], front_color_up,
        
        
        
    ]
def gondola_model_1_riding(
    hanger_width = .05,
    hanger_height = .2,
    hanger_color = [.3,.3,.3],
    top_color = [.2,.3,.2],
    bottom_color =[.5,.5,.5],
    side_color = [.2,.3,.2],
    side_color_up = [.15,.15,.15],
    side_color_up2 = [.16,.16,.16],
    front_color = [.3,.4,.3],
    front_color_up = [.17,.17,.17],
    depth = 1,
    width = 1,
    bulge = .11,
    front_bulge = .11,
    h1 = .8,
    h2 = .5):
    
    
    
    h_2 = hanger_width/2
    return [
        [0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        #[-width/1.3,-hanger_height,-depth/1.3], [width/1.3,-hanger_height,-depth/1.3], [width/1.3,-hanger_height,depth/1.3], [-width/1.3,-hanger_height,depth/1.3], top_color,
        [-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,depth/2], [-width/2,-hanger_height-h1-h2,depth/2], bottom_color,
        
        #[-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color_up,
        [-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color,
        
        #[-width/2,-hanger_height,depth/2], [width/2,-hanger_height,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color_up2,
        [-width/2,-hanger_height-h1-h2,depth/2], [width/2,-hanger_height-h1-h2,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height-h1-h2, depth/2], [width/2,-hanger_height-h1-h2, -depth/2], front_color,
        [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height-h1-h2, depth/2], [-width/2,-hanger_height-h1-h2, -depth/2], front_color,
        
        #[width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height, depth/2], [width/2,-hanger_height, -depth/2], front_color_up,
        #[-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height, depth/2], [-width/2,-hanger_height, -depth/2], front_color_up,
        
        
        
    ]
def gondola_model_2(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    top_color = [.2,.3,.2],
    bottom_color =[.5,.5,.5],
    side_color = [.2,.3,.2],
    side_color_up = [.15,.15,.15],
    side_color_up2 = [.16,.16,.16],
    front_color = [.3,.4,.3],
    front_color_up = [.17,.17,.17],
    depth = 1,
    width = 1,
    bulge = .11,
    front_bulge = .11,
    h1 = .5,
    h2 = .5    ):
    
    h_2 = hanger_width/2
    return [
        #[0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        [-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2,-hanger_height,depth/2], [-width/2,-hanger_height,depth/2], top_color,
        [-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,depth/2], [-width/2,-hanger_height-h1-h2,depth/2], side_color,
        
        #[-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color_up,
        #[-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color,
        
        [-width/2,-hanger_height,depth/2], [width/2,-hanger_height,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color_up2,
        [-width/2,-hanger_height-h1-h2,depth/2], [width/2,-hanger_height-h1-h2,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height-h1-h2, depth/2], [width/2,-hanger_height-h1-h2, -depth/2], front_color,
        [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height-h1-h2, depth/2], [-width/2,-hanger_height-h1-h2, -depth/2], front_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height, depth/2], [width/2,-hanger_height, -depth/2], front_color_up,
        [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height, depth/2], [-width/2,-hanger_height, -depth/2], front_color_up,
        
        
        
    ]
    
def gondola_model_3(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    top_color = [.2,.3,.2],
    bottom_color =[.5,.5,.5],
    side_color = [.2,.3,.2],
    side_color_up = [.15,.15,.15],
    side_color_up2 = [.16,.16,.16],
    front_color = [.3,.4,.3],
    front_color_up = [.17,.17,.17],
    depth = 1,
    width = 1,
    bulge = .11,
    front_bulge = .11,
    h1 = .5,
    h2 = .5    ):
    
    h_2 = hanger_width/2
    return [
        #[0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        #[-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2,-hanger_height,depth/2], [-width/2,-hanger_height,depth/2], top_color,
        [-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,depth/2], [-width/2,-hanger_height-h1-h2,depth/2], side_color,
        
        #[-width/2,-hanger_height,-depth/2], [width/2,-hanger_height,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color_up,
        #[-width/2,-hanger_height-h1-h2,-depth/2], [width/2,-hanger_height-h1-h2,-depth/2], [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], side_color,
        
        [-width/2,-hanger_height,depth/2], [width/2,-hanger_height,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color_up2,
        [-width/2,-hanger_height-h1-h2,depth/2], [width/2,-hanger_height-h1-h2,depth/2], [width/2+bulge,-hanger_height-h1,depth/2+front_bulge], [-width/2-bulge,-hanger_height-h1,depth/2+front_bulge], side_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height-h1-h2, depth/2], [width/2,-hanger_height-h1-h2, -depth/2], front_color,
        #[-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height-h1-h2, depth/2], [-width/2,-hanger_height-h1-h2, -depth/2], front_color,
        
        [width/2+bulge,-hanger_height-h1,-depth/2-front_bulge], [width/2+bulge,-hanger_height-h1, depth/2+front_bulge], [width/2,-hanger_height, depth/2], [width/2,-hanger_height, -depth/2], front_color_up,
        #[-width/2-bulge,-hanger_height-h1,-depth/2-front_bulge], [-width/2-bulge,-hanger_height-h1, depth/2+front_bulge], [-width/2,-hanger_height, depth/2], [-width/2,-hanger_height, -depth/2], front_color_up,
        
        
        
    ]
    
def gondola_model_4(
    hanger_width = .05,
    hanger_height = .5,
    hanger_color = [.3,.3,.3],
    top_color = [.2,.3,.2],
    bottom_color =[.5,.5,.5],
    side_color = [.2,.3,.2],
    side_color_up = [.15,.15,.15],
    side_color_up2 = [.16,.16,.16],
    front_color = [.3,.4,.3],
    front_color_up = [.17,.17,.17],
    depth = 1,
    width = 1,
    bulge = .11,
    front_bulge = .11,
    h1 = .5,
    h2 = .5,
    blurry_color = [.16,.24,.16]
        ):
    
    h_2 = hanger_width/2
    return [
        [-width/2,-hanger_height, -depth/2], [width/2,-hanger_height, depth/2], [width/2,-hanger_height-h1-h2, depth/2], [-width/2,-hanger_height-h1-h2, -depth/2], blurry_color,
        [width/2,-hanger_height, -depth/2], [-width/2,-hanger_height, depth/2], [-width/2,-hanger_height-h1-h2, depth/2], [width/2,-hanger_height-h1-h2, -depth/2], blurry_color,
        
        
    ]
"""
Double chair models
"""
def double_model_1():
    return chair_model_2(chair_width = .72)
def double_model_2():
    return chair_model_3(chair_width = .72)
def double_model_3():
    return chair_model_4(chair_width = .72)
    
"""
Triple chair models

"""

def triple_model_1():
    return chair_model_2(chair_width = 1.0)
def triple_model_2():
    return chair_model_3(chair_width = 1.0)
def triple_model_3():
    return chair_model_4(chair_width = 1.0)

"""
Six chair models

"""

def sixpack_model_1():
    return chair_model_2(chair_width = 1.8)
def sixpack_model_2():
    return chair_model_3(chair_width = 1.8)
def sixpack_model_3():
    return chair_model_4(chair_width = 1.8)


"""
T bar models
"""

def tbar_model_1(
    hanger_width = .05,
    hanger_height = .7,
    hanger_color = [.3,.3,.3],
    seat_back_color = [.1,.1,.1],
    seat_color = [.2,.2,.2],
    
    t_width = 1.2,
    t_color = [1,.6,.27],
    t_thickness = .07
    ):
    
    
    h_2 = hanger_width/2
    return [
        [0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        [0,-hanger_height,-t_width/2], [0,-hanger_height,t_width/2], [0,-hanger_height-t_thickness,t_width/2], [0,-hanger_height-t_thickness,-t_width/2], t_color,
        
        
    ]


def terminal_design_1(
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
    bullwheel_distance_from_pole = 0,
    slow_down_segments = 15,
    bullwheel_segments = 55,
    
    terminal_roof_height = 1.5,
    terminal_roof_height2 = 1.2,
    
    bullwheel_color = [.2,.2,.2],
    
    distance_between_bullwheel_and_wheels = 1,
    graphical_bullwheel_segments = 25
    ):
    
    bullwheel_radius = terminal_roof_width/2-terminal_track_indent
    track = lift_util.Track()
    
    speed_diff = rope_speed-terminal_speed
    
    for x in range(0, slow_down_segments):
        percent_round_down = x/slow_down_segments
        percent_round_up = x/(slow_down_segments-1) if slow_down_segments > 1 else 1
        x_pos = (1 - percent_round_down) * distance_between_bullwheel_and_wheels
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
        x_pos = (percent_round_up) * distance_between_bullwheel_and_wheels
        vel = terminal_speed + (percent_round_up) * speed_diff
        track.add_point(lift_util.Point(x_pos, pole_height, terminal_roof_width/2-terminal_track_indent, vel))
    
    
    #draw bullwheel
    bullwheel = []
    segment_angle = 2*math.pi / graphical_bullwheel_segments
    for i in range(graphical_bullwheel_segments):
        theta1 = i*segment_angle
        theta2 = (i+1)*segment_angle
        bullwheel.append([0, pole_height, 0])
        bullwheel.append([0, pole_height, 0])
        bullwheel.append([math.cos(theta1) * bullwheel_radius, pole_height, -math.sin(theta1) * bullwheel_radius])
        bullwheel.append([math.cos(theta2) * bullwheel_radius, pole_height, -math.sin(theta2) * bullwheel_radius])
        bullwheel.append(bullwheel_color)
    
    
    return [
    [-pole_length/2,0,-pole_width/2], [pole_length/2,0,-pole_width/2], [pole_length/2,pole_height,-pole_width/2], [-pole_length/2,pole_height,-pole_width/2], pole_color,
    [-pole_length/2,0,pole_width/2], [pole_length/2,0,pole_width/2], [pole_length/2,pole_height,pole_width/2], [-pole_length/2,pole_height,pole_width/2], pole_color,
    [-pole_length/2,0,-pole_width/2], [-pole_length/2,0,pole_width/2], [-pole_length/2,pole_height,pole_width/2], [-pole_length/2,pole_height,-pole_width/2], pole_color,
    [pole_length/2,0,-pole_width/2], [pole_length/2,0,pole_width/2], [pole_length/2,pole_height,pole_width/2], [pole_length/2,pole_height,-pole_width/2], pole_color,
    
    
    
    ]+bullwheel, track



"""
Pole Models
"""


def pole_design_2():
    return pole_design_1(pole_height = 4)


"""
  c:_________
    b:_____
     a:___


    _________
     _\___/_        }h
        |
        |
        |
        |
"""
def pole_design_1(
        pole_width = .5,
        pole_height = 7,
        t_width = 3,
        t_height = .3,
        pole_color = [.2,.2,.2],
        t_color = [.6,.6,.6],
        
        
        
        h = 1.5,
        a = 1.4,
        b = 2.5,
        c = 4,
        v_depth = .25
        

        ):
    p_2 = pole_width/2
    v_2 = v_depth /2
    
    
    return [
    
    #The pole
    [-p_2/2,0,-p_2], [-p_2,0,p_2], [-p_2,pole_height,p_2], [-p_2,pole_height,-p_2], pole_color,
    [p_2/2,0,-p_2], [p_2,0,p_2], [p_2,pole_height,p_2], [p_2,pole_height,-p_2], pole_color,
    [-p_2/2,0,-p_2], [p_2/2,0,-p_2], [p_2,pole_height,-p_2], [-p_2,pole_height,-p_2], pole_color, 
    [-p_2/2,0,p_2], [p_2/2,0,p_2], [p_2,pole_height,p_2], [-p_2,pole_height,p_2], pole_color, 
    
    
    #The T
    [-p_2,pole_height,-t_width/2], [p_2,pole_height,-t_width/2], [p_2,pole_height,t_width/2], [-p_2,pole_height,t_width/2], t_color,
    [-p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,t_width/2], [-p_2,pole_height+t_height,t_width/2], t_color,
    [-p_2,pole_height,-t_width/2], [p_2,pole_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [-p_2,pole_height+t_height,-t_width/2], t_color,
    [-p_2,pole_height,t_width/2], [p_2,pole_height,t_width/2], [p_2,pole_height+t_height,t_width/2], [-p_2,pole_height+t_height,t_width/2], t_color,
    [-p_2,pole_height,-t_width/2], [-p_2,pole_height+t_height,-t_width/2], [-p_2,pole_height+t_height,t_width/2], [-p_2,pole_height,t_width/2],  t_color,
    [p_2,pole_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,t_width/2], [p_2,pole_height,t_width/2],  t_color,
    
    
    #The v
    [-p_2,pole_height + t_height,a/2-v_2], [p_2,pole_height + t_height,a/2-v_2], [p_2,pole_height + t_height + h,b/2-v_2], [-p_2,pole_height + t_height + h,b/2-v_2], t_color,
    [-p_2,pole_height + t_height,a/2+v_2], [p_2,pole_height + t_height,a/2+v_2], [p_2,pole_height + t_height + h,b/2+v_2], [-p_2,pole_height + t_height + h,b/2+v_2], t_color,
    [-p_2,pole_height + t_height,-a/2-v_2], [p_2,pole_height + t_height,-a/2-v_2], [p_2,pole_height + t_height + h,-b/2-v_2], [-p_2,pole_height + t_height + h,-b/2-v_2], t_color,
    [-p_2,pole_height + t_height,-a/2+v_2], [p_2,pole_height + t_height,-a/2+v_2], [p_2,pole_height + t_height + h,-b/2+v_2], [-p_2,pole_height + t_height + h,-b/2+v_2], t_color,
    
    [-p_2,pole_height + t_height,-a/2-v_2], [-p_2,pole_height + t_height,-a/2+v_2], [-p_2,pole_height + t_height + h,-b/2+v_2], [-p_2,pole_height + t_height + h,-b/2-v_2], t_color,
    [p_2,pole_height + t_height,-a/2-v_2], [p_2,pole_height + t_height,-a/2+v_2], [p_2,pole_height + t_height + h,-b/2+v_2], [p_2,pole_height + t_height + h,-b/2-v_2], t_color,
    [-p_2,pole_height + t_height,a/2-v_2], [-p_2,pole_height + t_height,a/2+v_2], [-p_2,pole_height + t_height + h,b/2+v_2], [-p_2,pole_height + t_height + h,b/2-v_2], t_color,
    [p_2,pole_height + t_height,a/2-v_2], [p_2,pole_height + t_height,a/2+v_2], [p_2,pole_height + t_height + h,b/2+v_2], [p_2,pole_height + t_height + h,b/2-v_2], t_color,
    
    #The bar on top of the V
    [-p_2, pole_height + t_height + h, -c/2], [p_2, pole_height + t_height + h, -c/2], [p_2, pole_height + t_height + h, c/2], [-p_2, pole_height + t_height + h, c/2], t_color,
    [-p_2, pole_height + t_height + h + t_height, -c/2], [p_2, pole_height + t_height + h + t_height, -c/2], [p_2, pole_height + t_height + h + t_height, c/2], [-p_2, pole_height + t_height + h + t_height, c/2], t_color,
    [-p_2,pole_height + t_height + h,-c/2], [p_2,pole_height + t_height + h,-c/2], [p_2,pole_height + t_height + h + t_height,-c/2], [-p_2,pole_height + t_height + h + t_height,-c/2], t_color,
    [-p_2,pole_height + t_height + h,c/2], [p_2,pole_height + t_height + h,c/2], [p_2,pole_height + t_height + h + t_height,c/2], [-p_2,pole_height + t_height + h + t_height,c/2], t_color,
    [-p_2,pole_height + t_height + h,-c/2], [-p_2,pole_height + t_height + h,c/2], [-p_2,pole_height + t_height + h + t_height,c/2], [-p_2,pole_height + t_height + h + t_height,-c/2], t_color,
    [p_2,pole_height + t_height + h,-c/2], [p_2,pole_height + t_height + h,c/2], [p_2,pole_height + t_height + h + t_height,c/2], [p_2,pole_height + t_height + h + t_height,-c/2], t_color,
    ],[0,pole_height,t_width/2], [0,pole_height,-t_width/2], 
    
    


"""
         u1    u2
          _____
         /|    |\
    l1  / |____| \   l2
       | /      \ |
       |/________\|   l3
       l4
    
"""
def rock_design_1(
    
    l1 = [-1,-.6,-1],
    l2 = [1.2,-.6,-1],
    l3 = [.9,-.6,1.2],
    l4 = [-.9,-.6,1.2],
    
    u1 = [-.5,.4,-.5],
    u2 = [.6,.4,-.5],
    u3 = [.45,.6,.6],
    u4 = [-.45,.4,.6],
    
    front=[.8,.8,.8],
    right=[.7,.7,.7],
    left=[.65,.65,.65],
    back=[.75,.75,.75],
    top = [.9,.9,.9] ):
    
    
    return [list(x) for x in [
    u1,u2,u3,u4,top,
    u1,u2,l2,l1,back,
    u3,u2,l2,l3,right,
    u3,u4,l4,l3,front,
    l1,u1,u4,l4,left
    
    
    ]]
    
    
def rock_design_2(
    
    l1 = [-14,-30,-16],
    l2 = [16,-30,-15.8],
    l3 = [18,-30,16],
    l4 = [-18,-30,16],
    
    u1 = [-5,0,-5],
    u2 = [6,0,-5],
    u3 = [4.5,0,6],
    u4 = [-4.5,0,6],
    
    front=[.8,.8,.8],
    right=[.7,.7,.7],
    left=[.65,.65,.65],
    back=[.75,.75,.75],
    top = [.9,.9,.9] ):
    
    
    return [list(x) for x in [
    u1,u2,u3,u4,top,
    u1,u2,l2,l1,back,
    u3,u2,l2,l3,right,
    u3,u4,l4,l3,front,
    l1,u1,u4,l4,left
    
    
    ]]
