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



class Tree(WorldObject):
    #darkness factor represents the minimum brightness that the object can have
    #scale parameter is currently not used
    def __init__(self, **args):
        default(args, "model", tree_design_1)
        hr,vr = args["world"].get_rotation(int(args["z"]),int(args["x"]))
        if vr < 0:
            vr = -vr
            hr += math.pi
            
            
        if args["z"]%1==0 and args["x"]%1==0:#if z and x are pointing toward the corner of the square
            args["z"] = args["z"]+.5#put them in the middle of square
            args["x"] = args["x"]+.5#middle of square
        shade = args["world"].calculate_floor_color_single(hr,vr)
        args["model_args"] = {"shade":shade}
        default(args, "model_type", "tex")
        default(args, "do_lighting", False)
        default(args, "rotation", random()*math.pi)
        
        for obj in args["world"].quads[int(args["z"])][int(args["x"])].containedObjects:
            if isinstance(obj, WorldObject):
                return
        
        super().__init__(**args)
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

        
        
