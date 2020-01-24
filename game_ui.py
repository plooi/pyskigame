import math
from pylooiengine import *




class UI(LooiObject):
    def __init__(self, world):
        super().__init__(active=False)
        self.world = world
        self.crosshairs = False
        self.crosshair_length = 30
        self.mode = "game"
        
    def step(self):
        if self.mode == "game":
            if self.key("a", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot + math.pi/2, self.world.view.speed)
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("d", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot - math.pi/2, self.world.view.speed)
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("w", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot, self.world.view.speed)
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("s", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot + math.pi, self.world.view.speed)
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("space", "down"):
                self.world.view.y += self.world.view.speed
            if self.key("lshift", "down"):
                self.world.view.y -= self.world.view.speed
            rel = pygame.mouse.get_rel()
            self.world.view.hor_rot += -(rel[0])*self.world.view.rot_spd
            self.world.view.vert_rot += -(rel[1])*self.world.view.rot_spd
        
            
            
        
        
        
        if self.world.view.vert_rot > self.world.view.max_vert_rot:
            self.world.view.vert_rot = self.world.view.max_vert_rot
        if self.world.view.vert_rot < -self.world.view.max_vert_rot:
            self.world.view.vert_rot = -self.world.view.max_vert_rot
            
            
        self.world.add_mobile_quad([0,0,-5],[1,0,-5],[1,1,-5],[0,1,-5], [0,0,0])
    def convert_to_x_z(self, hor_rot, magnitude):
        z = -math.sin(hor_rot)*magnitude
        x = math.cos(hor_rot)*magnitude
        return x,z
    def paint(self):
        self.draw_text(0,150, "%f %f %f %f %f" % (self.world.view.x, self.world.view.y, self.world.view.z, self.world.view.hor_rot, self.world.view.vert_rot))
        internal_size = self.get_my_window().get_internal_size()
        
        if self.crosshairs:
            self.draw_line(
                            internal_size[0]/2, 
                            internal_size[1]/2-self.crosshair_length/2, 
                            internal_size[0]/2, 
                            internal_size[1]/2+self.crosshair_length/2,
                            black)
            self.draw_line(
                            internal_size[0]/2-self.crosshair_length/2, 
                            internal_size[1]/2, 
                            internal_size[0]/2+self.crosshair_length/2, 
                            internal_size[1]/2,
                            black)
    
    def enable_crosshairs(self, crosshairs):
        self.crosshairs = crosshairs
    
def set_mouse_mode(mode):
    if mode == "3D":
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    if mode == "normal":
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
