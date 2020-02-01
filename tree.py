import math
from random import random
from model_3d import *
from util import *
def tree_design_1():
    tree_width = 2
    tree_height = 9
    color1 = [0,1,0]
    color2 = [0,.9,0]
    
    
    return [
    [-tree_width/2,0,0], [tree_width/2,0,0], [0,tree_height,0], [0,tree_height,0], color1,
    [0,0,-tree_width/2], [0,0,tree_width/2], [0,tree_height,0], [0,tree_height,0], color2,
    
    
    ]
class Tree:
    def __init__(self, z, x, world, darkness_factor=2, design_function=tree_design_1):
        self.z=z
        self.x=x
        self.world = world
        self.y = self.world.get_elevation(z, x, scaled=True)
        self.darkness_factor = darkness_factor
        self.design_function = design_function
        self.design = design_function()
        horizontal_rotate_model_around_origin(self.design, random()*math.pi)
        move_model(self.design, self.x * self.world.properties["horizontal_stretch"], self.y, self.z * self.world.properties["horizontal_stretch"])
        
        for i in range(len(self.design)):
            if i%5 == 4:
                brightness = self.world.get_proper_floor_color(z, x)[0]
                darkness = 1-brightness
                self.design[i][1] -= darkness*darkness_factor
                if self.design[i][1] < 0: self.design[i][1] = 0
        self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self)
        
        

    
        
        
