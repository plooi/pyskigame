import math
from random import random
from model_3d import *
from util import *
from models import *
from selectable import *
from stop_selecting_exception import StopSelectingException
from pylooiengine import *
import PySimpleGUI as sg

class Building(Selectable):
    
    def __init__(self, z, x, world, design_function, params, rotation):
        self.z=z
        self.x=x
        self.world = world
        self.design_function = design_function
        self.params = params#params for the design function
        self.design = None
        self.rotation = rotation
        self.vertex_handler_pointers = None
        
        
        self.reset(delete=False)
        
        
    def add_object_account(self):
        
        #object account
        self.world.add_object_account(self, "Building(%d, %d, world, %s, %s, %f)"%(self.z, self.x, find_name(self.design_function), str(self.params), self.rotation ))
        
        
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
        self.world.get_elevation(z, x+1, scaled=True))/4 + .2
        self.design = self.design_function(**self.params)
        horizontal_rotate_model_around_origin(self.design, self.rotation)
        move_model(self.design, (self.x+.5) * self.world.properties["horizontal_stretch"], self.y, (self.z+.5) * self.world.properties["horizontal_stretch"])
        
        self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self)
        self.add_object_account()
    def delete(self):
        rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
        self.world.delete_object_account(self)
        
    def open_menu(self):
        layout = [
            [sg.Button("Delete")],
            [sg.Text("X"), sg.Input(str(self.x))],
            [sg.Text("Y"), sg.Text(str(self.y))],
            [sg.Text("Z"), sg.Input(str(self.z))],
            [sg.Text("Rotation"), sg.Input(str(self.rotation))],
            [sg.OK()]
        ]
        
        
        window = sg.Window("Building: %s"%(find_name(self.design_function),), layout, size=(500,800))
        event, values = window.Read()
        
        if event == "Delete":
            self.delete()
        elif event == "OK":
            try:
                original_x = self.x
                original_z = self.z
                new_x = int(values[0])
                new_z = int(values[1])
                self.rotation = float(values[2])
                self.x = new_x
                self.z = new_z
                self.add_object_account()
                self.x = original_x
                self.z = original_z
                
            except Exception as e:
                sg.Popup(str(e))
            
            
            recreate = self.world.object_account[id(self)]
            self.delete()
            world=self.world
            eval(recreate)
            
        window.close()



        
