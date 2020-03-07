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

from util import *

class Rock(WorldObject):
    def __init__(self, **args):
        default(args, "model", rock_design_1)
        default(args, "model_type", "tex")
        default(args, "rotation", random()*math.pi)
        super().__init__(**args)
    def touching(self, x, y, z): return ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) < 1
    def touching_player_consequence(self): 
        if self.world.properties["momentum"] >= constants["crash_speed"]: self.world.game_ui.falling = True

class BigRock(Rock):
    def __init__(self, **args):
        default(args, "model", rock_design_2)
        default(args, "model_type", "tex")
        super().__init__(**args)
        #self.inside_top_square = False
    def touching(self, x, y, z):
        #numbers 14 and 5 are from the model dimensions 
        dist_under = self.args["model_y"] - (y - self.world.properties["player_height"])
        r = 5 + (14-5)*dist_under/30#depending on how far down you are, the rock is a different width that can be modeled by a linear equation
        
        theta = self.args["rotation"]
        phi = get_angle(self.args["model_z"], self.args["model_x"], z, x)
        
        phi -= theta
        
        while phi < 0:phi += math.pi*2
        while phi >= math.pi*2:phi -= math.pi*2
        
        if   phi < 1*math.pi/4: alpha = phi
        elif phi < 2*math.pi/4: alpha = math.pi/2 - phi
        elif phi < 3*math.pi/4: alpha = phi - math.pi/2
        elif phi < 4*math.pi/4: alpha = math.pi - phi
        elif phi < 5*math.pi/4: alpha = phi - math.pi
        elif phi < 6*math.pi/4: alpha = 3*math.pi/2 - phi
        elif phi < 7*math.pi/4: alpha = phi - 3*math.pi/2
        else:                    alpha = 2*math.pi-phi
        
        d = r/math.sin(math.pi/2 - alpha)
        ret = ((((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2)**.5) < d) and (dist_under > 0) and (dist_under < 30)
        
        #d_top_square = 5/math.sin(math.pi/2 - alpha)
        #self.inside_top_square = (((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2)**.5) < d_top_square
        
        return ret
    def touching_player_consequence(self): 
        dist_under = self.args["model_y"] - (self.world.view.y - self.world.properties["player_height"])
        if dist_under < 1:# and self.inside_top_square:
            self.world.game_ui.modified_floor_y = self.args["model_y"]-.01
            self.world.game_ui.modified_floor_slope = math.pi/20
        else:
            if not self.world.game_ui.jumping:#so if you're jumping, you can have a bit more margin
                if self.world.properties["momentum"] >= constants["crash_speed"]: 
                    if self.world.properties["momentum"] >= .4:
                        self.world.game_ui.falling = 2
                    else:
                        self.world.game_ui.falling = 1
                else:
                    angle = get_angle(self.args["model_z"], self.args["model_x"], self.world.view.z, self.world.view.x)
                    self.world.view.z -= .8*math.sin(angle)
                    self.world.view.x += .8*math.cos(angle)
            else:
                self.world.game_ui.modified_floor_y = self.args["model_y"]-.01
                self.world.game_ui.modified_floor_slope = math.pi/20
def angle_in_between(a1, x, a2):
    da1 = angle_distance(x, a1)
    da2 = angle_distance(x, a2)
    x_ = x+.000001
    da1_plus = angle_distance(x_, a1)
    da2_plus = angle_distance(x_, a2)
    x_ = x-.000001
    da1_minus = angle_distance(x_, a1)
    da2_minus = angle_distance(x_, a2)
    
    return ((da1_plus>da1 and da2_plus<da2)or(da1_plus<da1 and da2_plus>da2)) and ((da1_minus>da1 and da2_minus<da2)or(da1_minus<da1 and da2_minus>da2))
    
