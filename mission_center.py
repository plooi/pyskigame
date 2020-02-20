from tree import Tree
from models import *
from pylooiengine import *
from world_object import *
from model_3d import *
import util
import normal
from random import random
import PySimpleGUI as sg
from constants import x as constants


mission_accept_icon = image("textures/Landmark Icon.png")



def find_closest_mission_center(lz, lx):
    closest = None
    distance = 999999999999999999999999999
    for mc in active_mission_centers:
        this_distance = ((mc.args["z"]-lz)**2 + (mc.args["x"]-lx)**2)**.5
        if this_distance < distance:
            closest = mc
            distance = this_distance
    return closest
    
        

def check_reset_missions():
    for mc in active_mission_centers:
        landmarks = list(mc.world.landmarks)
        
        #remove all the landmarks not closest to this mission center
        i = 0
        while i < len(landmarks):
            lz, lx = (landmarks[i].args["z"], landmarks[i].args["x"])
            
            closest = find_closest_mission_center(lz, lx)
            if not (closest is mc):
                del landmarks[i]
                i -= 1
                
            i += 1
        
        #remove all the completed missions
        i = 0
        while i < len(landmarks):
            landmark_tuple = (landmarks[i].args["z"], landmarks[i].args["x"])
            if is_in(landmark_tuple, mc.world.properties["completed_missions"]):
                del landmarks[i]
                i -= 1
            i += 1
            
        if len(landmarks) >= 4:
            #this mission center has missions
            return
    #no mission centers have missions. Reset
    mc.world.properties["completed_missions"] = []
    mc.world.properties["active_missions"] = []#just to make sure

def is_in(landmark_tuple, array_of_missions):
    for mission in array_of_missions:
        if mission[0] == landmark_tuple:
            return True
    return False
    

def randomly_select(n, array):
    check(len(array) >= n)
    
    ret = []
    for i in range(n):
        index = int(random() * len(array))
        ret.append(array[index])
        del array[index]
    return ret

active_mission_centers = []

class MissionCenter(WorldObject):
    def __init__(self, **args):
        default(args, "model", building_with_slanted_roof)
        default(args, "model_type", "std")
        default(args, "model_args", {"length" : 4, "width" : 4})
        default(args, "do_lighting", False)
        default(args, "y", args["world"].get_elevation_continuous(args["z"], args["x"]) + .2)
        args["active"] = "always"
        
        super().__init__(**args)
        
        self.beacon = beacon_model()
        move_model(self.beacon, self.args["model_x"], self.args["model_y"], self.args["model_z"])
        self.draw_icon = False
    def step(self):
        if len(self.world.properties["active_missions"]) == 0:
            if self.key(constants["find_key"], "down"):
                add_model_to_world_mobile(self.beacon, self.world)
    def paint(self):
        indicator_width = 10
        indicator_height = 50
        indicator_color = Color(0,0,0)
        
        if len(self.world.properties["active_missions"]) == 0 and self.key(constants["find_key"], "down"):
            half_screen = self.get_my_window().get_internal_size()[0]/2
            player_to_me = util.get_angle(self.world.view.z, self.world.view.x, self.args["model_z"], self.args["model_x"])
            diff = normal.angle_distance(self.world.view.hor_rot, player_to_me)
            if normal.angle_distance(self.world.view.hor_rot + .001, player_to_me) < normal.angle_distance(self.world.view.hor_rot - .001, player_to_me):
                #this mission center is left of the player
                x = diff/(math.pi/2)
                if x > 1:
                    x = 1
                x = half_screen - x*half_screen
            else:
                #this mission centre is left of the player
                x = diff/(math.pi/2)
                if x > 1:
                    x = 1
                x = half_screen + x*half_screen
            self.draw_rect(x-indicator_width/2, 0, x+indicator_width/2, indicator_height, indicator_color)
        if self.draw_icon:
            self.draw_image(950, 890, 1050, 990,mission_accept_icon)
            self.draw_icon = False
    def touching(self, x, y, z):
        if ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5 < 2:
            return True
        return False
    def touching_player_consequence(self):
        
        if len(self.world.properties["active_missions"]) == 0:
            self.draw_icon = True
            if self.key(constants["interact_key"], "pressed"):
                landmarks = list(self.world.landmarks)
                
                #remove all the landmarks not closest to this mission center
                i = 0
                while i < len(landmarks):
                    lz, lx = (landmarks[i].args["z"], landmarks[i].args["x"])
                    
                    closest = find_closest_mission_center(lz, lx)
                    if not (closest is self):
                        del landmarks[i]
                        i -= 1
                        
                    i += 1
                
                #remove all the completed missions
                i = 0
                while i < len(landmarks):
                    landmark_tuple = (landmarks[i].args["z"], landmarks[i].args["x"])
                    if is_in(landmark_tuple, self.world.properties["completed_missions"]):
                        del landmarks[i]
                        i -= 1
                    i += 1
                
                
                if len(landmarks) < 4:
                    sg.Popup("No more missions from this mission center. You can find more missions at other mission centers. \n\n(enter to close).")
                    return#you need 4 or more landmarks to make up a mission
                    #or you need to complete all missions from all other mission centers to reset this mission center
                
                x = randomly_select(3, landmarks)
                for lm in x:
                    self.world.properties["active_missions"].append([(lm.args["z"], lm.args["x"]), 1])
        else:
            self.draw_icon = False
    def activate(self):
        super().activate()
        if self not in active_mission_centers:
            active_mission_centers.append(self)
    def deactivate(self):
        super().deactivate()
        if self in active_mission_centers:
            active_mission_centers.remove(self)
def beacon_model(
    width=3,
    height=1000):
    
    return [
        [-width/2,0,-width/2],[width/2,0,-width/2],[width/2,height,-width/2],[-width/2,height,-width/2],[.5,.5,.5],
        [-width/2,0,width/2],[width/2,0,width/2],[width/2,height,width/2],[-width/2,height,width/2],[.5,.5,.5],
        [-width/2,0,-width/2],[-width/2,0,width/2],[-width/2,height,width/2],[-width/2,height,-width/2],[.5,.5,.5],
        [width/2,0,-width/2],[width/2,0,width/2],[width/2,height,width/2],[width/2,height,-width/2],[.5,.5,.5],
        #[0,height-square_diagonal/2,0],[0,height,square_diagonal/2],[0,height+square_diagonal/2,0],[0,height,-square_diagonal/2],square_color,
    
    
    
    ]
