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

eat_icon = image("textures/Eat Icon.png")

class Lodge(WorldObject):
    def __init__(self, **args):
        default(args, "model", building_with_slanted_roof)
        default(args, "model_type", "std")
        default(args, "model_args", {"length" : 8, "width" : 8, "height": 6, "roof_height":8, "wall_color1": [.82,.7,.54], "wall_color2": [.77,.65,.49]})
        default(args, "do_lighting", False)
        default(args, "active", "always")
        default(args, "y", args["world"].get_elevation_continuous(args["z"], args["x"]) + .2)
        super().__init__(**args)
        
        self.draw_icon = False
        self.set_layer(None)
    def step(self):
        pass
    def paint(self):
        if self.draw_icon:
            self.draw_image(950, 890, 1050, 990,eat_icon)
            self.draw_icon = False
    def touching(self, x, y, z):
        if ((x-self.args["model_x"])**2 + (z-self.args["model_z"])**2) ** .5 < 2:
            return True
        return False
    def touching_player_consequence(self):
        if self.world.properties["health"] < 99:
            self.draw_icon = True
            if self.key(constants["interact_key"], "pressed"):
                self.world.game_ui.health(100,animate=True,relative=False)


class Hut(Lodge):
    def __init__(self, **args):
        default(args, "model_args", {"length" : 4, "width" : 4, "height": 4, "roof_height":6,"wall_color1": [.82,.7,.54], "wall_color2": [.77,.65,.49]})
        super().__init__(**args)
    def touching_player_consequence(self):
        if self.world.properties["health"] < 69:
            self.draw_icon = True
            if self.key(constants["interact_key"], "pressed"):
                self.world.game_ui.health(70,animate=True,relative=False)
