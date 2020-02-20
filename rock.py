import math
from random import random
from model_3d import *
from util import *
from tree import Tree
from models import *
from pylooiengine import *
import PySimpleGUI as sg

from world_object import *
from constants import x as constants



class Rock(WorldObject):
    def __init__(self, **args):
        default(args, "model", rock_design_1)
        default(args, "model_type", "std")
        default(args, "do_lighting", True)
        default(args, "rotation", random()*math.pi)
        super().__init__(**args)
    def touching(self, x, y, z): return ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) < 1
    def touching_player_consequence(self): 
        if self.world.properties["momentum"] >= constants["crash_speed"]: self.world.game_ui.falling = True

class BigRock(Rock):
    def __init__(self, **args):
        default(args, "model", rock_design_2)
        super().__init__(**args)
    def touching(self, x, y, z): 
        dist_under = self.args["model_y"] - (y - self.world.properties["player_height"])
        return ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2)**.5 < 21 and dist_under > 0
