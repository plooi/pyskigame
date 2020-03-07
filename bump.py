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
from world_object import *
from constants import x as constants

collision_angle = math.pi/10

class Bump(WorldObject):
    def __init__(self, **args):
        default(args, "model", bump_model_1)
        default(args, "model_type", "tex")
        default(args, "do_lighting", False)
        default(args, "rotation", args["world"].get_rotation(int(args["z"]), int(args["x"]))[0])
        default(args, "model_args", {
                "sun_is_to_the_left" : is_a_left_of_b(args["world"].properties["sun_angle"], args["rotation"]),
                "angle_distance_from_sun" : normal.angle_distance(args["world"].properties["sun_angle"], args["rotation"])})
        
        super().__init__(**args)

    def touching(self, x, y, z):
        dist = ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5
        if dist < constants["bump_collision_radius"] and y<self.args["model_y"]+3.5:
            return True
        return False
    def touching_player_consequence(self):
        if self.world.properties["momentum"] >= constants["crash_speed"]:
            self.world.game_ui.falling = True
            

#repurposed into a naturally occurring rock, but i don't want to change everything so Ill just keep it like this
class NaturalBump(WorldObject):
    def __init__(self, **args):
        default(args, "model", rock_design_3)
        default(args, "model_type", "tex")
        default(args, "do_lighting", False)
        default(args, "rotation", random()*math.pi*2)
        
        
        super().__init__(**args)
    """
    def touching(self, x, y, z):
        dist = ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5
        if dist < constants["bump_collision_radius"] and y<self.args["model_y"]+3.5:
            return True
        return False
    def touching_player_consequence(self):
        if self.world.properties["momentum"] >= constants["crash_speed"]:
            self.world.game_ui.falling = True
    
    """
    def touching(self, x, y, z):
        #numbers 14 and 5 are from the model dimensions 
        dist_under = self.args["model_y"] - (y - self.world.properties["player_height"])
        r = 2.5 + (11-2.5)*dist_under/15#depending on how far down you are, the rock is a different width that can be modeled by a linear equation
        
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
        ret = ((((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2)**.5) < d) and (dist_under > 0) and (dist_under < 15)
        
        #d_top_square = 5/math.sin(math.pi/2 - alpha)
        #self.inside_top_square = (((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2)**.5) < d_top_square
        
        return ret
    def touching_player_consequence(self): 
        dist_under = self.args["model_y"] - (self.world.view.y - self.world.properties["player_height"])
        if dist_under < .6:# and self.inside_top_square:
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
    
    
    
    
    
    def delete(self):
        self.remove_fixed_model()
