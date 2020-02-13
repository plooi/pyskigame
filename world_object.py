from pylooiengine import *
import math
from random import random
from model_3d import *
import models
import PySimpleGUI as sg

class WorldObject(LooiObject):
    """
    required args
        world
        z (anchor_z)
        x (anchor_x))
    optional args
        y (unscaled_y)
        
        model_x
        model_y
        model_z
        model
        model_type
        model_args
        do_lighting
        
        active
    """
    def __init__(self, **args):
        super().__init__(active=False)
        self.args = args
        self.world = args["world"]
        self.h = self.world.properties["horizontal_stretch"]
        self.v = self.world.properties["vertical_stretch"]
        self.vertex_handler_pointers = None
        
        
        
        
        default(args, "rotation", 0)
        
        
        #z and x are the non scaled coordinates of the world object. Quad z x is where this object is pinned
        self.set_anchor(args["z"], args["x"], relocate_model=False)
        
        #move y up to the floor's elevation
        default(args, "y", self.world.get_elevation_continuous(args["z"], args["x"]))
        
        
        #set the position and add the model
        if "model" in args:
            check("model_type" in args and (args["model_type"] == "std" or args["model_type"] == "grad"))
            
            default(args, "model_z", args["z"]*self.h)
            default(args, "model_x", args["x"]*self.h)
            default(args, "model_y", args["y"]*self.v)
            
            default(args, "do_lighting", True)
            
            self.set_model_position(args["model_x"], args["model_y"], args["model_z"])
        
        
        
        #active can be "always" "never" "line_of_sight" "texture_distance"
        #right now, only "always" and "never" works
        default(args, "active", "never")
        if args["active"] == "always":
            self.activate()
            
        
        self.update_object_account()
        
        
    def get_recreate_string(self):
        recreate_string = type(self).__name__ + "(" 
        for key in self.args:
            if key == "world": continue
            value = self.args[key]
            if not(
                    isinstance(value, int) or
                    isinstance(value, float) or
                    isinstance(value, str) or
                    isinstance(value, list) or
                    isinstance(value, tuple) or
                    isinstance(value, dict) or 
                    callable(value)):
                raise Exception("Key %s has a value of type %s which is not an allowed type for serialization" % (key, type(value)))
            if callable(value):
                value = models.find_name(value)
                recreate_string += key + "=" + value +","
            else:
                recreate_string += key + "=" + repr(value) +","
        recreate_string += "world=world)"
        return recreate_string
    def update_object_account(self):
        self.world.add_object_account(self, self.get_recreate_string())
        
    def set_model_position(self, x, y, z):
        #remove the old model
        self.remove_fixed_model()
        
        self.args["model_x"] = x
        self.args["model_y"] = y
        self.args["model_z"] = z
        
        self.add_fixed_model()
    
    """
    do_lighting
    
    modifies the model that it is given to 
    #you can override this one if you want differnt lighting
    """
    def do_lighting(self, model, min_brightness=.4):
        
        brightness = self.world.get_proper_floor_color(self.args["z"], self.args["x"])[0]
        if brightness < min_brightness: brightness = min_brightness
        
        
        if self.args["model_type"] == "grad":
            for i in range(len(model)):
                if i%8 >= 4:
                    
                    model[i][0] *= brightness
                    model[i][1] *= brightness
                    model[i][2] *= brightness
        else:
            for i in range(len(model)):
                if i%5 == 4:
                    
                    model[i][0] *= brightness
                    model[i][1] *= brightness
                    model[i][2] *= brightness
        
        
        
    def set_anchor(self, z, x, relocate_model=True):
        if not self.world.valid_floor(z, x):
            raise Exception("Invalid z and x position " + str(x) + " " + str(z) + ". World dimensions are h%d w%d" % (self.world.get_height_floors(), self.world.get_width_floors()))
        if relocate_model:
            self.remove_fixed_model()
        self.args["z"] = z
        self.args["x"] = x
        if relocate_model:
            self.add_fixed_model()
        self.update_object_account()
        
        
        
    def remove_fixed_model(self):
        if self.vertex_handler_pointers != None:
            rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.args["z"], self.args["x"], self)
        self.vertex_handler_pointers = None
        
        
        
    def add_fixed_model(self):
        check(self.vertex_handler_pointers == None)
        if "model_args" in self.args: model = self.args["model"](**self.args["model_args"])
        else: model = self.args["model"]()
        
        
        gm = True if self.args["model_type"] == "grad" else False
        horizontal_rotate_model_around_origin(model, self.args["rotation"], gradient_model=gm)
        move_model(model, self.args["model_x"], self.args["model_y"], self.args["model_z"],gradient_model=gm)
        
        if self.args["do_lighting"]:
            self.do_lighting(model)
        
        self.vertex_handler_pointers = add_model_to_world_fixed(model, self.world, self.args["z"], self.args["x"], self,gradient_model=gm)
        
        
        
    def open_menu(self):
        layout = [
            [sg.Button("Delete")],
        ]
        
        
        window = sg.Window(type(self).__name__, layout, size=(500,800))
        event, values = window.Read()
        
        if event == "Delete":
            self.delete()
        window.close()
    """
    is point x,y,z touching this object?
    
    x,y,z is in real space
    """
    def touching(self, x, y, z):
        return False
    def touching_player_consequence(self):
        self.world.ui.falling = True
        
        
    def delete(self):
        self.remove_fixed_model()
        try:
            self.world.delete_object_account(self)
        except Exception as e:
            sg.Popup(str(e))
def default(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
