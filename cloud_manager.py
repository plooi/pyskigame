
from pylooiengine import *
from random import random
from math import *
from constants import x as constants
import texture


class CloudManager(LooiObject):
    def __init__(self, game_ui):
        super().__init__()
        self.game_ui = game_ui
        self.world = game_ui.world
        for i in range(constants["num_clouds"]):
            Cloud(self)
        self.clouds = texture.new_texture_handler()
         
    def step(self):
        pass
        
    def draw_heavenly_body(self):
        glAlphaFunc(GL_GREATER,.5)
            
        self.world.draw_tex(self.clouds.vertices, self.clouds.vertex_colors, self.world.get_setup_3d_far(translate=False), mipmap=False)
        self.clouds = texture.new_texture_handler()
        glAlphaFunc(GL_GREATER,.1)
        
class Cloud(LooiObject):
    def __init__(self, cm):
        super().__init__()
        self.cloud_manager = cm
        self.init()
        self.progress = random()*constants["cloud_travel_distance"]
    def init(self):
        self.sideways = (random()*2-1)*(constants["cloud_spawn_length"]/2)
        self.progress = random()*constants["max_cloud_initial_head_start"]
        self.height = random()*(constants["max_cloud_height"] - constants["min_cloud_height"]) + constants["min_cloud_height"]#height above ground
        self.width = random()*(constants["max_cloud_width"]-constants["min_cloud_width"]) + constants["min_cloud_width"]#width of image
        self.length = random()*(constants["max_cloud_length"]-constants["min_cloud_length"]) + constants["min_cloud_length"]#length of image
        
        
        self.tex = ["Cloud1","Cloud2","Cloud3"]
        self.tex = self.tex[int(random()*len(self.tex))]
        
    def step(self):
        self.progress += constants["cloud_move_speed"]
        if self.progress >= constants["cloud_travel_distance"]:
            self.init()
    def draw_heavenly_body(self):
        angle = self.cloud_manager.world.properties["sun_angle"] + pi/2
        offset = self.progress-constants["cloud_travel_distance"]/2
        x = offset*cos(angle)   + self.sideways*cos(angle+pi/2)
        z = -offset*sin(angle)   - self.sideways*sin(angle+pi/2)
        y = self.height
        
        
        
        texture.add_image_to_vertex_handler(
            self.cloud_manager.clouds,
            [x-self.length/2,y,z-self.width/2],
            [x+self.length/2,y,z-self.width/2],
            [x+self.length/2,y,z+self.width/2],
            [x-self.length/2,y,z+self.width/2],self.tex)
        
        
        
        
        
        
