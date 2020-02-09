import math
from random import random
from model_3d import *
from util import *
from models import *
from selectable import *
from stop_selecting_exception import StopSelectingException
from pylooiengine import *
import PySimpleGUI as sg

class Tree(Selectable):
    #darkness factor represents the minimum brightness that the object can have
    def __init__(self, z, x, world, darkness_factor=.4, design_function=tree_design_1, rotation=None):
        if len(world.quads[z][x].containedObjects) > 0:
            return
            
        
        self.z=z
        self.x=x
        self.world = world
        if darkness_factor > 1: darkness_factor = 1
        self.darkness_factor = darkness_factor
        self.design_function = design_function
        self.design = None
        self.rotation = random()*math.pi if rotation==None else rotation
        
        
        self.reset(delete=False)
        
        
    def add_object_account(self):
        
        #object account
        self.world.add_object_account(self, "Tree(%d, %d, world, %f, %s, %f)"%(self.z, self.x, self.darkness_factor, find_name(self.design_function), self.rotation ))
        
        
    #UNTESTED
    def reset(self, delete=True):
        z = self.z
        x = self.x
        if delete:
            self.delete()
        self.y = (
        self.world.get_elevation(z, x, scaled=True) + 
        self.world.get_elevation(z+1, x, scaled=True) + 
        self.world.get_elevation(z+1, x+1, scaled=True) + 
        self.world.get_elevation(z, x+1, scaled=True))/4
        self.design = self.design_function()
        horizontal_rotate_model_around_origin(self.design, self.rotation)
        move_model(self.design, (self.x+.5) * self.world.properties["horizontal_stretch"], self.y, (self.z+.5) * self.world.properties["horizontal_stretch"])
        
        for i in range(len(self.design)):
            if i%5 == 4:
                brightness = self.world.get_proper_floor_color(z, x)[0]
                if brightness < self.darkness_factor: brightness = self.darkness_factor
                self.design[i][0] *= brightness
                self.design[i][1] *= brightness
                self.design[i][2] *= brightness
                
        self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self)
        self.add_object_account()
    def delete(self):
        rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
        self.world.delete_object_account(self)
        
    def open_menu(self):
        layout = [
            [sg.Button("Delete")],
            [],
            [],
            [],
            [],
            [],
            [sg.Button("!")]
        ]
        
        
        window = sg.Window("Tree", layout, size=(500,800))
        event, values = window.Read()
        
        if event == "Delete":
            self.delete()
        if event == "!":
            window.close()
            raise StopSelectingException()
        window.close()

        
        
