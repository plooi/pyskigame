from tree import Tree
from models import *
from pylooiengine import *
from world_object import *
from model_3d import *
import util
import normal
import mission_center
import PySimpleGUI as sg
class Landmark(WorldObject):
    #required: x,z,world
    def __init__(self, **args):
        default(args, "model", landmark_model_1)
        default(args, "model_type", "grad")
        args["active"] = "always"
        super().__init__(**args)
        
        self.world.landmarks.append(self)
        self.showing = True
        self.beacon = beacon_model()
        move_model(self.beacon, self.args["model_x"], self.args["model_y"], self.args["model_z"])
        
    def hide(self):
        if self.showing:
            self.remove_fixed_model()
            self.showing = False
    def show(self):
        if not self.showing:
            self.add_fixed_model()
            self.showing = True
    def delete(self):
        super().delete()
        if self in self.world.landmarks:
            self.world.landmarks.remove(self)
        self.deactivate()
        
    def step(self):
        if self.world.game_ui.game_mode == "map editor":
            self.show()
        else:
            location_tuple = (self.args["z"], self.args["x"])
            if mission_center.is_in(location_tuple, self.world.properties["active_missions"]):
                self.show()
            else:
                self.hide()
        if self.showing and self.key("f", "down"):
            add_model_to_world_mobile(self.beacon, self.world)
    def paint(self):
        indicator_width = 10
        indicator_height = 50
        indicator_color = Color(1,0,0)
        if self.showing and self.key("f", "down"):
            half_screen = self.get_my_window().get_internal_size()[0]/2
            player_to_me = util.get_angle(self.world.view.z, self.world.view.x, self.args["model_z"], self.args["model_x"])
            diff = normal.angle_distance(self.world.view.hor_rot, player_to_me)
            if normal.angle_distance(self.world.view.hor_rot + .001, player_to_me) < normal.angle_distance(self.world.view.hor_rot - .001, player_to_me):
                #this landmark is left of the player
                x = diff/(math.pi/2)
                if x > 1:
                    x = 1
                x = half_screen - x*half_screen
            else:
                #this landmark is left of the player
                x = diff/(math.pi/2)
                if x > 1:
                    x = 1
                x = half_screen + x*half_screen
            self.draw_rect(x-indicator_width/2, 0, x+indicator_width/2, indicator_height, indicator_color)
    def touching(self, x, y, z):
        if ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5 < 1:
            return True
        return False
    def touching_player_consequence(self):
        for i in range(len(self.world.properties["active_missions"])):
            if self.world.properties["active_missions"][i][0] == (self.args["z"],self.args["x"]):
                mission_type = self.world.properties["active_missions"][i][1]
                self.world.properties["completed_missions"].append(self.world.properties["active_missions"][i])
                del self.world.properties["active_missions"][i]
                
                if mission_type == 1:
                    if len(self.world.properties["active_missions"]) == 0:
                        sg.Popup("Type 1 missions complete.")
                return
"""
def beacon_model():
    return [
        [-10,0,0], [10,0,0],[200,6000,0],[-200,6000,0],[.5,.5,.5],
        [0,0,-10], [0,0,10],[0,6000,200],[0,6000,-200],[.5,.5,.5],
    ]
"""
def beacon_model(
    width=3,
    height=1000):
    
    return [
        [-width/2,0,-width/2],[width/2,0,-width/2],[width/2,height,-width/2],[-width/2,height,-width/2],[.5,0,.5],
        [-width/2,0,width/2],[width/2,0,width/2],[width/2,height,width/2],[-width/2,height,width/2],[.5,0,.5],
        [-width/2,0,-width/2],[-width/2,0,width/2],[-width/2,height,width/2],[-width/2,height,-width/2],[.5,0,.5],
        [width/2,0,-width/2],[width/2,0,width/2],[width/2,height,width/2],[width/2,height,-width/2],[.5,0,.5],
        #[0,height-square_diagonal/2,0],[0,height,square_diagonal/2],[0,height+square_diagonal/2,0],[0,height,-square_diagonal/2],square_color,
    
    
    
    ]
    
