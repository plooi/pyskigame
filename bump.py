import math
from random import random
from model_3d import *
from util import *
from models import *
from selectable import *
from stop_selecting_exception import StopSelectingException
from pylooiengine import *
import PySimpleGUI as sg
import normal
class Bump:
    #darkness factor represents the minimum brightness that the object can have
    #scale parameter is currently not used
    def __init__(self, z, x, world,  design_function=bump_model_2, rotation=None, real_z=None, real_x=None):
       
            
        #self.scale=scale
        self.z=z
        self.x=x
        self.y = None
        self.world = world
        
        self.real_z = (self.z+random()) * self.world.properties["horizontal_stretch"] if real_z == None else real_z
        self.real_x = (self.x+random()) * self.world.properties["horizontal_stretch"] if real_x == None else real_x
        
        self.design_function = design_function
        self.design = None
        self.rotation = rotation
        
        
        
        self.reset(delete=False)
        print("bump")
        
    def add_object_account(self):
        
        #object account
        self.world.add_object_account(self, "Bump(%d, %d, world, %s, %f, %f, %f)"%(self.z, self.x, find_name(self.design_function), self.rotation, self.real_z, self.real_x))
        
        
    def reset(self, delete=True):
        z = self.z
        x = self.x
        
        if self.rotation == None:
            
            floor = self.world.quads[z][x]
            chunk = self.world.chunks[floor.my_chunk_z][floor.my_chunk_x]
            ul = chunk.vh.vertices[floor.floor_pointer]
            ur = chunk.vh.vertices[floor.floor_pointer+1]
            lr = chunk.vh.vertices[floor.floor_pointer+2]
            hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ur[0],ur[1],ur[2],lr[0],lr[1],lr[2])
            if vr < 0:
                vr = -vr
                hr = hr + math.pi
            self.rotation = hr
        
        
        
        
        
        if delete:
            self.delete()
        self.y = self.world.get_elevation_continuous(
                        self.real_z/self.world.properties["horizontal_stretch"],
                        self.real_x/self.world.properties["horizontal_stretch"])*self.world.properties["vertical_stretch"]
        
        self.design = self.design_function()
        
        horizontal_rotate_model_around_origin(self.design, self.rotation)
        move_model(self.design, self.real_x, self.y, self.real_z)
        
        brightness = self.world.get_proper_floor_color(z, x)[0]
        if brightness < .4: brightness = .4
        
        for i in range(len(self.design)):
            if i%5 == 4:
                
                self.design[i][0] *= brightness
                self.design[i][1] *= brightness
                self.design[i][2] *= brightness
        
        self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self)
        self.add_object_account()
    def delete(self):
        rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
        self.world.delete_object_account(self)
