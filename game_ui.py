import math
from pylooiengine import *
import map_edit_menu
import ski_menu
import lift
from normal import *
import ski_draw
from random import random
from constants import x as constants

class UI(LooiObject):
    def __init__(self, world, game_mode):
        super().__init__(active=False)
        self.set_layer(100)
        self.world = world
        self.crosshairs = False
        self.crosshair_length = 30
        self.interface_mode = "game"#"game" or "menu" or "can_move_temporarily"
        self.game_mode = game_mode#"map editor" or "ski" or ski test
        
        self.menu = None
        
        #for chairlift riding
        self.my_lift = None
        self.my_chair = None
        self.can_load = False
        self.load_icon = image("Chair Load Icon.png")
        
        self.chair_sit_forward_distance = 0
    def chairlift_ride(self):
        self.can_load = False
        chair_ride_distance = constants["chair_ride_distance"]
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
                            i = len(cp)-1-i
                            if ( (cp[i][0]-x)**2 + (cp[i][1]-constants["chair_sit_under_distance"]-y)**2 + (cp[i][2]-z)**2 )**.5 < chair_ride_distance:#if a chair is close
                                self.can_load = True
                                if self.key("r", "pressed"):
                                    self.my_lift = chairlift
                                    self.my_chair = i
                                    self.my_lift.player_riding = i
                                    return
                    else:#if currently riding
                        if self.key("r", "pressed"):
                            self.my_lift.player_riding = None
                            self.my_lift = None
                            self.my_chair = None
                            
        if self.my_lift != None and self.my_chair != None:
            self.world.view.x = self.my_lift.chair_positions[self.my_chair][0] + math.cos(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.view.y = self.my_lift.chair_positions[self.my_chair][1] - constants["chair_sit_under_distance"]
            self.world.view.z = self.my_lift.chair_positions[self.my_chair][2] - math.sin(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.properties["ski_direction"] = self.my_lift.chair_angles[self.my_chair]
            if self.game_mode == "map editor":
                if self.key("r", "pressed"):#this should only be available in map editor!!!!!!!!!!!!!!!!!!
                    self.my_lift = None
                    self.my_chair = None
            return True
        return False
        
    def step(self):
        self.look_around()
        self.e_key()
        if not self.chairlift_ride():
            
            if self.game_mode == "map editor": self.map_editor_move()
            if self.game_mode == "ski" or self.game_mode == "ski test":self.ski_mode_move()
            
                    
        if self.game_mode.startswith("ski"): ski_draw.draw_skis(self, ski_draw.models[self.world.properties["ski_model"]])
        
        if self.key("t", "pressed"):
            if self.game_mode == "map editor": self.game_mode = "ski test"
            elif self.game_mode == "ski test": self.game_mode = "map editor"
            
    
    
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
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot + math.pi/2, constants["ski_mode_walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("d", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot - math.pi/2, constants["ski_mode_walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("w", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot, constants["ski_mode_walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
            if self.key("s", "down"):
                d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot + math.pi, constants["ski_mode_walk_speed"])
                self.world.view.x += d_x
                self.world.view.z += d_z
                
                
            
            g = .1
            ski_g = .1
            
            max_speed = .5
            
            friction_coefficient = .05
            min_friction = .006#should i change to .01
            
            
            if self.mouse("left", "down") and self.mouse("right", "down"):
                pass
            elif self.mouse("left", "down") or self.key("q", "down"):
                
                turn = angle_distance(self.world.properties["ski_direction"], self.world.view.hor_rot)
                self.world.properties["ski_direction"] = self.world.view.hor_rot
                
                p1,p2,p3 = self.xyz_of_current_triangle(v.z, v.x)
                floor_hr, floor_vr = get_plane_rotation(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
                
                if floor_vr < 0:
                    floor_vr = -floor_vr
                    floor_hr += math.pi
                
                floor_slope = math.pi/2 - floor_vr
                
                resistance = angle_distance(self.world.properties["ski_direction"], floor_hr)   
                
                equivalent_floor_slope = math.cos(resistance) * floor_slope
                
                f_parallel = ski_g * math.sin(equivalent_floor_slope)
                
                fhorizontal = f_parallel * math.cos(equivalent_floor_slope)
                
                self.world.properties["momentum"] += fhorizontal
                self.world.properties["momentum_direction"] = self.world.properties["ski_direction"]
                
                if turn > math.pi/4:
                    turn = math.pi/4
                    
                turn = (turn) ** 1.2
                
                #print(turn)
                self.world.properties["momentum"] *= (1 - turn/(math.pi/4))
                friction = friction_coefficient * self.world.properties["momentum"]**2
                if friction < min_friction:
                    friction = min_friction
                self.world.properties["momentum"] -= friction
                if self.world.properties["momentum"] > max_speed:
                    self.world.properties["momentum"] = max_speed
                
                
                if self.world.properties["momentum"] < 0:
                    self.world.properties["momentum"] = 0
                #bump = 0
                #if self.world.properties["momentum"] / max_speed > .8:
                #    bump = random() * (self.world.properties["momentum"] / max_speed) ** 4 * .2
                #    self.world.view.vert_rot += (random()*2-1) * (self.world.properties["momentum"] / max_speed) ** 4 * math.pi/40
                
                v.x += self.world.properties["momentum"] * math.cos(self.world.properties["momentum_direction"])
                v.z += self.world.properties["momentum"] * -math.sin(self.world.properties["momentum_direction"])
                v.y = self.get_elevation_continuous(v.z, v.x)*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]# + bump

            elif self.mouse("right", "down"):
                pass
            else:
                self.world.properties["momentum"] = 0
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
                    if self.menu != None:# and self.menu.current_action == None:
                        self.menu.deactivate()
                        self.menu = None
                    set_mouse_mode("3D")
            elif self.game_mode.startswith("ski"):
                if self.interface_mode == "game":
                    self.interface_mode = "menu"
                    self.menu = ski_menu.Menu(self)
                    set_mouse_mode("normal")
                
                elif self.interface_mode == "menu":
                    self.interface_mode = "game"
                    if self.menu != None:# and self.menu.current_action == None:
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
        if self.interface_mode == "menu":
            self.draw_text(0,100,"FPS: " + str(self.world.fps.fps))
        if self.can_load:
            self.draw_image(950, 900, 1050, 1000,self.load_icon)
        #self.draw_text(0,50, "%f %f %f %f %f" % (self.world.view.x, self.world.view.y, self.world.view.z, self.world.view.hor_rot, self.world.view.vert_rot))
        self.draw_text(0,600,str(self.world.properties["momentum"]))
        #self.draw_text(0,600,str(self.game_mode))
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
def abs(x):
    if x >= 0:
        return x
    return -x
def set_mouse_mode(mode):
    if mode == "3D":
        pygame.mouse.get_rel()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    if mode == "normal":
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
