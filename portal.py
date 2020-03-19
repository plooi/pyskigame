import math
from random import random
from model_3d import *

from tree import Tree
from models import *
from pylooiengine import *
import PySimpleGUI as sg
from normal import *
from world_object import *
from constants import x as constants
import world_save
import rooms

from util import *
class Portal(WorldObject):
    def __init__(self, **args):
        default(args, "model", portal_model_1)
        default(args, "model_type", "grad")
        super().__init__(**args)
        
        
        
        check(isinstance(args["destination_world"], str))
        check(isinstance(args["destination_x"], int) or isinstance(args["destination_x"], float))
        check(isinstance(args["destination_z"], int) or isinstance(args["destination_z"], float))
    def touching(self, x, y, z): return ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) < 1
    def touching_player_consequence(self):     
        
        def job():
            
            if self.world.game_ui.game_mode == "map editor" or self.world.game_ui.game_mode == "ski test":
                world_save.write(self.world)
                the_world = world_save.read("../worlds/"+self.args["destination_world"])
                rooms.init_game_room(the_world)
                the_world.game_ui.game_mode = self.world.game_ui.game_mode
            elif self.world.game_ui.game_mode == "ski":
                world_save.write(self.world, writepath="../saves/")
                the_world = world_save.read("../worlds/"+self.args["destination_world"])
                rooms.init_ski_room(the_world)
                the_world.properties["name"] = self.world.properties["name"]
            else:
                fail("???")
            the_world.view.x = self.args["destination_x"]
            the_world.view.z = self.args["destination_z"]
        
        rooms.LoadingScreen(job)
        

