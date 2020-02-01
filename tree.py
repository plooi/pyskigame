import math
from random import random
from model_3d import *
from util import *

from pylooiengine import *
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
    def __init__(self, z, x, world, darkness_factor=2, design_function=tree_design_1, rotation=None):
        
        self.z=z
        self.x=x
        self.world = world
        self.y = (
            self.world.get_elevation(z, x, scaled=True) + 
            self.world.get_elevation(z+1, x, scaled=True) + 
            self.world.get_elevation(z+1, x+1, scaled=True) + 
            self.world.get_elevation(z, x+1, scaled=True))/4
        self.darkness_factor = darkness_factor
        self.design_function = design_function
        self.design = design_function()
        self.rotation = random()*math.pi if rotation==None else rotation
        horizontal_rotate_model_around_origin(self.design, self.rotation)
        move_model(self.design, (self.x+.5) * self.world.properties["horizontal_stretch"], self.y, (self.z+.5) * self.world.properties["horizontal_stretch"])
        
        for i in range(len(self.design)):
            if i%5 == 4:
                brightness = self.world.get_proper_floor_color(z, x)[0]
                darkness = 1-brightness
                self.design[i][1] -= darkness*darkness_factor
                if self.design[i][1] < 0: self.design[i][1] = 0
        self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self)
        
        
        
        
        #object account
        world.add_object_account(self, "Tree(%d, %d, world, %f, %s, %f)"%(z, x, self.darkness_factor, "tree_design_1" if self.design_function is tree_design_1 else fail("unknown function"), self.rotation ))
        
        
        
    def delete(self):
        rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
        self.world.delete_object_account(self)
        

    
        
        
