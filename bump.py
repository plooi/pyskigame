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
        ang = get_angle(z, x, self.args["model_z"], self.args["model_x"]) - self.args["rotation"]
        dist = ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5
        if (
            normal.angle_distance(ang, 0) < collision_angle or
            normal.angle_distance(ang, math.pi/2) < collision_angle or
            normal.angle_distance(ang, math.pi) < collision_angle or
            normal.angle_distance(ang, 3*math.pi/2) < collision_angle):#only check for collision at full distance if player is at a right angle with the bump's model, where the bump is longest
            
            if dist < 2.4:
                return True
        elif dist < 1.9:
            return True
        return False
    def touching_player_consequence(self):
        if self.world.properties["momentum"] >= constants["crash_speed"]:
            self.world.game_ui.falling = True
            

class NaturalBump(WorldObject):
    def __init__(self, **args):
        default(args, "model", bump_model_4)
        default(args, "model_type", "tex")
        default(args, "do_lighting", False)
        default(args, "rotation", args["world"].get_rotation(int(args["z"]), int(args["x"]))[0])
        default(args, "model_args", {
                "sun_is_to_the_left" : is_a_left_of_b(args["world"].properties["sun_angle"], args["rotation"]),
                "angle_distance_from_sun" : normal.angle_distance(args["world"].properties["sun_angle"], args["rotation"])})
        
        
        super().__init__(**args)
    def touching(self, x, y, z):
        ang = get_angle(z, x, self.args["model_z"], self.args["model_x"]) - self.args["rotation"]
        dist = ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5
        if (
            normal.angle_distance(ang, 0) < collision_angle or
            normal.angle_distance(ang, math.pi/2) < collision_angle or
            normal.angle_distance(ang, math.pi) < collision_angle or
            normal.angle_distance(ang, 3*math.pi/2) < collision_angle):#only check for collision at full distance if player is at a right angle with the bump's model, where the bump is longest
            
            if dist < 2.4:
                return True
        elif dist < 1.9:
            return True
        return False
    def touching_player_consequence(self):
        if self.world.properties["momentum"] >= constants["crash_speed"]:
            self.world.game_ui.falling = True
    def update_object_account(self):
        #natural bumps aren't saved. they're created by the seed
        pass
    def delete(self):
        self.remove_fixed_model()
