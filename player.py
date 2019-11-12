from pylooiengine import *
import math


class Player(LooiObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.hor_rot = math.pi/2
        self.vert_rot = 0
        self.speed = 4
        self.rot_spd = math.pi/20
        self.line_of_sight = 80 #IN NUMBER OF BLOCKS (not opengl space) #the radius
    
    def step(self):
        
        if self.key("a", "down"):
            d_x, d_z = self.convert_to_x_z(self.hor_rot + math.pi/2, self.speed)
            self.x += d_x
            self.z += d_z
        if self.key("d", "down"):
            d_x, d_z = self.convert_to_x_z(self.hor_rot - math.pi/2, self.speed)
            self.x += d_x
            self.z += d_z
        if self.key("w", "down"):
            d_x, d_z = self.convert_to_x_z(self.hor_rot, self.speed)
            self.x += d_x
            self.z += d_z
        if self.key("s", "down"):
            d_x, d_z = self.convert_to_x_z(self.hor_rot + math.pi, self.speed)
            self.x += d_x
            self.z += d_z
        if self.key("space", "down"):
            self.y += self.speed
        if self.key("lshift", "down"):
            self.y -= self.speed
        if self.key("left", "down"):
            self.hor_rot += self.rot_spd
        if self.key("right", "down"):
            self.hor_rot -= self.rot_spd
        if self.key("up", "down"):
            self.vert_rot += self.rot_spd
        if self.key("down", "down"):
            self.vert_rot -= self.rot_spd
            
    def convert_to_x_z(self, hor_rot, magnitude):
        z = -math.sin(hor_rot)*magnitude
        x = math.cos(hor_rot)*magnitude
        return x,z
    def paint(self):
        #self.draw_text(0,150, "%f %f %f %f %f" % (self.x, self.y, self.z, self.hor_rot, self.vert_rot))
        pass
    
    
        
            
