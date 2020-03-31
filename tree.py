import math
from random import random
from model_3d import *
from util import *
from models import *
from selectable import *
from stop_selecting_exception import StopSelectingException
from pylooiengine import *
import PySimpleGUI as sg
from world_object import *
from constants import x as constants
import shadow_map



class Tree(WorldObject):
    #darkness factor represents the minimum brightness that the object can have
    #scale parameter is currently not used
    def __init__(self, **args):
        args["model"] = tree_design_1
        #default(args, "model", tree_design_1)
        hr,vr = args["world"].get_rotation(int(args["z"]),int(args["x"]))
        if vr < 0:
            vr = -vr
            hr += math.pi
            
        
        if args["z"]%1==0 and args["x"]%1==0:#if z and x are at the corner of the square
            args["z"] = args["z"]+random()#put them in the middle of square with random deviation
            args["x"] = args["x"]+random()
        shade = args["world"].calculate_floor_color_single(hr,vr)
        args["model_args"] = {"shade":shade, "height":8+random()*4}
        default(args, "model_type", "tex")
        default(args, "do_lighting", False)
        default(args, "rotation", random()*math.pi)
        default(args, "remove_shadow", True)#this property indicates whether to remove shadow when deleted
        
        for obj in args["world"].quads[int(args["z"])][int(args["x"])].containedObjects:
            if isinstance(obj, WorldObject):
                return
        
        
        
        
        super().__init__(**args)
        self.args["has_shadow"] = False
        #self.add_shadow()
        
        
    
    def get_shadow_pos(self):
        if "height" not in self.args["model_args"]: self.args["model_args"]["height"] = 10#for backwared compatibility
        
        
        s_base = 3*shadow_map.D#actually equal to base over 2, the real base of the triangle is sbase * 2
        
        s_height = 15*self.args["model_args"]["height"]/10  *shadow_map.D#12
        sa = self.world.properties["sun_angle"]
        hs = self.world.properties["horizontal_stretch"]
        
        
        x1 = s_base*math.cos(sa+math.pi/2)
        z1 = s_base*-math.sin(sa+math.pi/2)
        
        x2 = s_base*math.cos(sa-math.pi/2)
        z2 = s_base*-math.sin(sa-math.pi/2)
        
        x3 = s_height*math.cos(sa+math.pi)
        z3 = s_height*-math.sin(sa+math.pi)
        
        
        z_offset = self.args["z"]*hs*shadow_map.D
        x_offset = self.args["x"]*hs*shadow_map.D
        
        z1+= z_offset
        x1+= x_offset
        z2+= z_offset
        x2+= x_offset
        z3+= z_offset
        x3+= x_offset
        
        return z1,x1,z2,x2,z3,x3
    def add_shadow(self):
        if "has_shadow" in self.args and self.args["has_shadow"]==False:
            z1,x1,z2,x2,z3,x3=self.get_shadow_pos()
            self.world.shadow_map.add_triangle_shadow(z1,x1,z2,x2,z3,x3,self,cut_outside=True)
            self.args["has_shadow"] = True
    def remove_shadow(self):
        z1,x1,z2,x2,z3,x3=self.get_shadow_pos()
        self.world.shadow_map.remove_triangle_shadow(z1,x1,z2,x2,z3,x3,self)
    def touching(self, x, y, z): return (((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5 < 1.4) and y<self.args["model_y"]+6
    def touching_player_consequence(self): 
        if self.world.properties["momentum"] >= constants["crash_speed"]:
            self.world.game_ui.falling = True
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
    def delete(self):
        super().delete()
        
        if "remove_shadow" in self.args and self.args["remove_shadow"]: self.remove_shadow()
        
        
