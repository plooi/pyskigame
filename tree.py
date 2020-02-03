import math
from random import random
from model_3d import *
from util import *
from models import *

from pylooiengine import *

class Tree:
    def __init__(self, z, x, world, darkness_factor=1.5, design_function=tree_design_1, rotation=None):
        
        self.z=z
        self.x=x
        self.world = world
        self.y = (
            self.world.get_elevation(z, x, scaled=True) + 
            self.world.get_elevation(z+1, x, scaled=True) + 
            self.world.get_elevation(z+1, x+1, scaled=True) + 
            self.world.get_elevation(z, x+1, scaled=True))/4
            
            
        #for obj in world.quads[z][x].containedObjects:#if there's already another tree in this spot, just forget it. DOnt add this tree
        #    if isinstance(obj, Tree):
        #        return
        if len(world.quads[z][x].containedObjects) > 0:
            return
            
            
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
                self.design[i][0] -= darkness*darkness_factor
                if self.design[i][0] < 0: self.design[i][0] = 0
                self.design[i][1] -= darkness*darkness_factor
                if self.design[i][1] < 0: self.design[i][1] = 0
                self.design[i][2] -= darkness*darkness_factor
                if self.design[i][2] < 0: self.design[i][2] = 0
        self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self)
        
        self.add_object_account()
    def add_object_account(self):
        
        #object account
        self.world.add_object_account(self, "Tree(%d, %d, world, %f, %s, %f)"%(self.z, self.x, self.darkness_factor, find_name(self.design_function), self.rotation ))
        
        
        
        
        
    def delete(self):
        rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
        self.world.delete_object_account(self)
        

    
        
        
