import math
from pylooiengine import *
import map_edit_menu
import lift
from normal import *

class UI(LooiObject):
    def __init__(self, world, game_mode):
        super().__init__(active=False)
        self.world = world
        self.crosshairs = False
        self.crosshair_length = 30
        self.interface_mode = "game"#"game" or "menu" or "can_move_temporarily"
        self.game_mode = game_mode#"map editor" or "ski"
        
        self.menu = None
        
        #for chairlift riding
        self.my_lift = None
        self.my_chair = None
        self.can_load = False
        self.load_icon = image("Chair Load Icon.png")
        
        self.chair_sit_under_distance = .6
        self.chair_sit_forward_distance = 0
    def chairlift_ride(self):
        self.can_load = False
        chair_ride_distance = self.world.properties["chair_ride_distance"]
        x = self.world.view.x
        y = self.world.view.y
        z = self.world.view.z
        
        
        for chairlift in lift.active_lifts:
            cp = chairlift.chair_positions
            #print(x,y,z,chairlift.start_terminal.real_x,chairlift.start_terminal.real_y,chairlift.start_terminal.real_z)
            for term in [chairlift.start_terminal, chairlift.end_terminal]:
                if ( (term.real_z-z)**2 + (term.real_y-y)**2 + (term.real_x-x)**2 )**.5 <= 10:#if close to a terminal
                    if self.my_lift == None and self.my_chair == None:#if not currently riding
                        for i in range(len(cp)):
                             
                            if ( (cp[i][0]-x)**2 + (cp[i][1]-self.chair_sit_under_distance-y)**2 + (cp[i][2]-z)**2 )**.5 < chair_ride_distance:#if a chair is close
                                self.can_load = True
                                if self.key("r", "pressed"):
                                    self.my_lift = chairlift
                                    self.my_chair = i
                                    return
                    else:#if currently riding
                        if self.key("r", "pressed"):
                            self.my_lift = None
                            self.my_chair = None
        if self.my_lift != None and self.my_chair != None:
            self.world.view.x = self.my_lift.chair_positions[self.my_chair][0] + math.cos(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.view.y = self.my_lift.chair_positions[self.my_chair][1] - self.chair_sit_under_distance
            self.world.view.z = self.my_lift.chair_positions[self.my_chair][2] - math.sin(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            if self.game_mode == "map editor":
                if self.key("r", "pressed"):#this should only be available in map editor!!!!!!!!!!!!!!!!!!
                    self.my_lift = None
                    self.my_chair = None
        
    def step(self):
        self.chairlift_ride()
        self.e_key()
        if self.game_mode == "map editor": self.map_editor_move()
        if self.game_mode == "ski":self.ski_mode_move()
        self.look_around()
                    
            
        if self.key("t", "pressed"):
            if self.game_mode == "map editor": self.game_mode = "ski"
            else: self.game_mode = "map editor"
            
    
    
    #input scaled position
    def get_elevation_continuous(self, z, x):
        
        
        
        #make z and x unscaled so we can call world.getelevation with them
        z /= self.world.properties["horizontal_stretch"]
        x /= self.world.properties["horizontal_stretch"]
        
        if not self.world.valid_floor(int(z), int(x)):
            return -9999
        
        
        #determine if we're in the upper left triangle, 
        #or the upper right triangle
        fracz = z % 1
        fracx = x % 1
        if fracz+fracx < 1:
            #upper left triangle
            ul = int(x), self.world.get_elevation(int(z),int(x)), int(z)
            ur = int(x)+1, self.world.get_elevation(int(z),int(x)+1), int(z)
            ll = int(x), self.world.get_elevation(int(z)+1,int(x)), int(z)+1
            xrise = ur[1] - ul[1]
            zrise = ll[1] - ul[1]
            
            y = fracx*xrise + fracz*zrise + ul[1]
            
        else:
            #upper right triangle
            lr = int(x)+1, self.world.get_elevation(int(z)+1,int(x)+1), int(z)+1
            ur = int(x)+1, self.world.get_elevation(int(z),int(x)+1), int(z)
            ll = int(x), self.world.get_elevation(int(z)+1,int(x)), int(z)+1
            
            
            xrise = ll[1] - lr[1]
            zrise = ur[1] - lr[1]
            
            y = (1-fracx)*xrise + (1-fracz)*zrise + lr[1]
        #print(ll,ur)
        return y
    def xyz_of_current_triangle(self, z, x):
        def scale(point):
            point[0] *= self.world.properties["horizontal_stretch"]
            point[1] *= self.world.properties["vertical_stretch"]
            point[2] *= self.world.properties["horizontal_stretch"]
            return point
        
        #make z and x unscaled so we can call world.getelevation with them
        z /= self.world.properties["horizontal_stretch"]
        x /= self.world.properties["horizontal_stretch"]
        
        if not self.world.valid_floor(int(z), int(x)):
            return [0,0,0],[0,0,0],[0,0,0]
        
        
        #determine if we're in the upper left triangle, 
        #or the upper right triangle
        fracz = z % 1
        fracx = x % 1
        if fracz+fracx < 1:
            #upper left triangle
            ul = [int(x), self.world.get_elevation(int(z),int(x)), int(z)]
            ur = [int(x)+1, self.world.get_elevation(int(z),int(x)+1), int(z)]
            ll = [int(x), self.world.get_elevation(int(z)+1,int(x)), int(z)+1]
            
            return (scale(ul),scale(ur),scale(ll))
            
        else:
            #upper right triangle
            lr = [int(x)+1, self.world.get_elevation(int(z)+1,int(x)+1), int(z)+1]
            ur = [int(x)+1, self.world.get_elevation(int(z),int(x)+1), int(z)]
            ll = [int(x), self.world.get_elevation(int(z)+1,int(x)), int(z)+1]
            
            
            return (scale(lr),scale(ur),scale(ll))
        
    def ski_mode_move(self):
        v = self.world.view
        if self.interface_mode == "game" or self.interface_mode == "can_move_temporarily":
            if self.key("a", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot + math.pi/2, self.world.properties["walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("d", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot - math.pi/2, self.world.properties["walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("w", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot, self.world.properties["walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("s", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot + math.pi, self.world.properties["walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
                
                
            margin = 0
            g = .1
                
            if self.mouse("left", "down") and self.mouse("right", "down"):
                self.world.properties["ski_direction"] = self.world.view.hor_rot
                ski_g = .7
                
                p1,p2,p3 = self.xyz_of_current_triangle(v.z, v.x)
                floor_hr, floor_vr = get_plane_rotation(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
                if floor_vr < 0:
                    floor_vr = -floor_vr
                    floor_hr += math.pi
                
                floor_slope = math.pi/2 - floor_vr
                
                
                
                resistance = angle_distance(self.world.properties["ski_direction"], floor_hr)   
                
                equivalent_floor_slope = math.cos(resistance) * floor_slope
                
                
                #print(p1,p2,p3)
                #print(floor_vr, floor_slope, equivalent_floor_slope/math.pi)
                
                f_parallel = ski_g * math.sin(equivalent_floor_slope)
                
                
                
                yforce = f_parallel * math.sin(equivalent_floor_slope)
                fhorizontal = f_parallel * math.cos(equivalent_floor_slope)
                
                
                #print(yforce, equivalent_floor_slope, resistance)
                
                
                
                #self.world.properties["x_momentum"] += fhorizontal * math.cos(self.world.properties["ski_direction"])
                #self.world.properties["y_momentum"] -= yforce
                #self.world.properties["z_momentum"] += fhorizontal * -math.sin(self.world.properties["ski_direction"])
                
                v.x += fhorizontal * math.cos(self.world.properties["ski_direction"])
                v.z += fhorizontal * -math.sin(self.world.properties["ski_direction"])
                v.y = self.get_elevation_continuous(v.z, v.x)*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
                
                #v.x += self.world.properties["x_momentum"]   
                #v.y += self.world.properties["y_momentum"]   
                #v.z += self.world.properties["z_momentum"]   
                
                
            else:
                
                elev = self.get_elevation_continuous(v.z, v.x)
                if v.y - self.world.properties["player_height"] < elev*self.world.properties["vertical_stretch"]:
                    v.y = elev*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
                    self.world.properties["y_momentum"] = 0
                elif v.y - self.world.properties["player_height"] > elev*self.world.properties["vertical_stretch"]:
                    self.world.properties["y_momentum"] -= g
                
                
                
                if self.my_lift != None:
                    self.world.properties["y_momentum"] = 0
                v.y += self.world.properties["y_momentum"]    
                
                #repeat again
                elev = self.get_elevation_continuous(v.z, v.x)
                if v.y - self.world.properties["player_height"] < elev*self.world.properties["vertical_stretch"]:
                    v.y = elev*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
                    self.world.properties["y_momentum"] = 0
                
                
                
                
            
                
                
                         
            
    def look_around(self):
        if self.interface_mode == "game" or self.interface_mode == "can_move_temporarily":
            rel = pygame.mouse.get_rel()
            self.world.view.hor_rot += -(rel[0])*self.world.view.rot_spd
            self.world.view.vert_rot += -(rel[1])*self.world.view.rot_spd
                
            
                
                
            
            
            
            if self.world.view.vert_rot > self.world.view.max_vert_rot:
                self.world.view.vert_rot = self.world.view.max_vert_rot
            if self.world.view.vert_rot < -self.world.view.max_vert_rot:
                self.world.view.vert_rot = -self.world.view.max_vert_rot
    def e_key(self):
        if self.key("e", "pressed"):
            if self.game_mode == "map editor":
                if self.interface_mode == "game":
                    self.interface_mode = "menu"
                    self.menu = map_edit_menu.Menu(self)
                    set_mouse_mode("normal")
                
                elif self.interface_mode == "menu":
                    self.interface_mode = "game"
                    if self.menu != None and self.menu.current_action == None:
                        self.menu.deactivate()
                        self.menu = None
                    set_mouse_mode("3D")
    def map_editor_move(self):
        
        if self.interface_mode == "game" or self.interface_mode == "can_move_temporarily":
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
            
    def convert_to_x_z(self, hor_rot, magnitude):
        z = -math.sin(hor_rot)*magnitude
        x = math.cos(hor_rot)*magnitude
        return x,z
    def paint(self):
        if self.can_load:
            self.draw_image(950, 900, 1050, 1000,self.load_icon)
        #self.draw_text(0,50, "%f %f %f %f %f" % (self.world.view.x, self.world.view.y, self.world.view.z, self.world.view.hor_rot, self.world.view.vert_rot))
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
        pygame.mouse.get_rel()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    if mode == "normal":
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
