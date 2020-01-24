from pylooiengine import *
import math
import pyautogui
import pygame
import map_edit_menu
import pylooiengine
class Player(LooiObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.hor_rot = math.pi/2
        self.vert_rot = 0
        self.speed = 4
        self.rot_spd = .001
        self.line_of_sight = 10 #IN NUMBER OF CHUNKS (not opengl space) #the radius
        self.world = None
        
        self.max_vert_rot = math.pi/2.3
        
        
        self.crosshairs = False
        self.crosshair_length = 30
        
        self.menu = map_edit_menu.Menu(self)
    
    def step(self):
        if self.mode == "game":
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
            rel = pygame.mouse.get_rel()
            self.hor_rot += -(rel[0])*self.rot_spd
            self.vert_rot += -(rel[1])*self.rot_spd
        
            
            
        
        
        
        if self.vert_rot > self.max_vert_rot:
            self.vert_rot = self.max_vert_rot
        if self.vert_rot < -self.max_vert_rot:
            self.vert_rot = -self.max_vert_rot
            
    def convert_to_x_z(self, hor_rot, magnitude):
        z = -math.sin(hor_rot)*magnitude
        x = math.cos(hor_rot)*magnitude
        return x,z
    def paint(self):
        #self.draw_text(0,150, "%f %f %f %f %f" % (self.x, self.y, self.z, self.hor_rot, self.vert_rot))
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
    
            
        
class MapEditorPlayer(Player):
    def __init__(self):
        super().__init__()
        self.mode = "game"
    def step(self):
        super().step()
        if self.key("r", "released"):
            if self.mode == "game":
                
                self.start_menu()
                
                
            elif self.mode == "menu":
                
                self.end_menu()
                
        """
        floor_pointed_at = self.world.get_player_pointing()
        #print(floor_pointed_at)
        if floor_pointed_at != None:
            
            world = self.world
            color = [1,0,0]
            
            z = floor_pointed_at[0]
            x = floor_pointed_at[1]
            
            world.vertex_handler.rm_vertex(world.grid[z][x].floor_vert_handler_index)
            world.vertex_handler.rm_vertex(world.grid[z][x].floor_vert_handler_index+1)
            world.vertex_handler.rm_vertex(world.grid[z][x].floor_vert_handler_index+2)
            world.vertex_handler.rm_vertex(world.grid[z][x].floor_vert_handler_index+3)

            world.grid[z][x].floor_vert_handler_index = world.vertex_handler.add_vertex(
                            [x*world.unit_length, 
                            world.vertical_stretch * world.get_elevation(z,x),
                            z*world.unit_length]
                            , color) 
            _should_be_previous_plus_1 = world.vertex_handler.add_vertex(
                [(x+1)*world.unit_length, 
                world.vertical_stretch * world.get_elevation(z,x+1),
                z*world.unit_length]
                , color) 
            _should_be_last_plus_2 = world.vertex_handler.add_vertex(
                [(x+1)*world.unit_length, 
                world.vertical_stretch * world.get_elevation(z+1,x+1),
                (z+1)*world.unit_length]
                , color) 
            _should_be_plus_3 = world.vertex_handler.add_vertex(
                [(x)*world.unit_length, 
                world.vertical_stretch * world.get_elevation(z+1,x),
                (z+1)*world.unit_length]
                , color) 
        """
    def start_menu(self):
        self.menu.activate()
        pylooiengine.main_window.set_fps(60)
        set_mouse_mode("normal")
        self.mode = "menu"
    def end_menu(self):
        self.menu.deactivate()
        pygame.mouse.get_rel()
        pylooiengine.main_window.set_fps(15)
        self.mode = "game"
        set_mouse_mode("3D")
def set_mouse_mode(mode):
    if mode == "3D":
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    if mode == "normal":
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
