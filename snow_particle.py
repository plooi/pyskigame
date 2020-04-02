
from pylooiengine import *
from random import random
from math import *


class SnowParticle(LooiObject):
    """
    mh is horizontal momentum
    mhr is horizontal direction (momentum horizontal rotation)
    mv is vertical momentum
    """
    def __init__(self, world, x, y, z, mh, mhr, mv, size=.05, color=white, g=.01, friction = 1, despawn_chance=.04):
        super().__init__()
        self.x=x
        self.y=y
        self.z=z
        self.size=size
        self.color=color
        self.world=world
        self.despawn_chance=despawn_chance
        
        self.friction=friction
        self.mh = mh
        self.mhr = mhr
        self.mv = mv
        self.g=g
        
    def step(self):
        if random() < self.despawn_chance:
            self.deactivate()
            return
        h = self.world.properties["horizontal_stretch"]
        v = self.world.properties["vertical_stretch"]
        
        self.x += self.mh*cos(self.mhr)
        self.z -= self.mh*sin(self.mhr)
        
        self.mv -= self.g
        self.y += self.mv
        
        self.mh /= self.friction
        self.mv /= self.friction
        
        
        unscaled_x = self.x/h
        unscaled_z = self.z/h
        unscaled_y = self.y/v
        
        if self.x < 0 or self.z < 0 or not self.world.valid_point(int(unscaled_z), int(unscaled_x)):
            self.deactivate()
        if self.world.get_elevation_continuous(unscaled_z,unscaled_x) > unscaled_y+.1:
            self.deactivate()
        
        
    def paint(self):
        s2 = self.size/2
        self.world.add_mobile_quad([self.x-s2,self.y,self.z],[self.x,self.y+s2,self.z],[self.x+s2,self.y,self.z],[self.x,self.y-s2,self.z],[self.color.r,self.color.g,self.color.b])
        self.world.add_mobile_quad([self.x,self.y,self.z-s2],[self.x,self.y+s2,self.z],[self.x,self.y,self.z+s2],[self.x,self.y-s2,self.z],[self.color.r,self.color.g,self.color.b])
        
