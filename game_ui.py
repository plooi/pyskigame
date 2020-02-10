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
        
        #fall stuff
        self.fall_clock = 0
        self.falling = False
        self
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
                            return
        if self.my_lift != None and self.my_chair != None:
            self.world.view.x = self.my_lift.chair_positions[self.my_chair][0] + math.cos(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.view.y = self.my_lift.chair_positions[self.my_chair][1] - constants["chair_sit_under_distance"]
            self.world.view.z = self.my_lift.chair_positions[self.my_chair][2] - math.sin(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.properties["ski_direction"] = self.my_lift.chair_angles[self.my_chair]
            self.world.properties["do_floor_textures"] = False
            if self.game_mode == "map editor":
                if self.key("r", "pressed"):#this should only be available in map editor!!!!!!!!!!!!!!!!!!
                    self.my_lift = None
                    self.my_chair = None
            return True
        self.world.properties["do_floor_textures"] = True
        return False
        
    def step(self):
        self.look_around()
        self.e_key()
        
        if not self.chairlift_ride():
            
            if self.game_mode == "map editor": self.map_editor_move()
            if self.game_mode == "ski" or self.game_mode == "ski test":
                if self.falling:
                    self.fall()
                else:
                    self.ski_mode_move()
            
                    
        if self.game_mode.startswith("ski") and not self.falling: 
            ski_draw.draw_skis(self, ski_draw.models[self.world.properties["ski_model"]])
        
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
    def fall(self):
        if self.falling:
            if self.fall_clock == 0:
                self.original_pos = (self.world.view.x,self.world.view.y,self.world.view.z,self.world.view.hor_rot,self.world.view.vert_rot)
            elif self.fall_clock <= 15:
                fall_horizontal_distance = 1
                t = self.fall_clock/15
                self.world.view.x = self.original_pos[0] + t*fall_horizontal_distance*math.cos(self.original_pos[3])
                self.world.view.z = self.original_pos[2] - t*fall_horizontal_distance*math.sin(self.original_pos[3])
                self.world.view.y = self.original_pos[1] - t*(self.world.properties["player_height"]-.1)
                self.world.view.vert_rot = self.original_pos[4] + t*(-math.pi/2 - self.original_pos[4])
                self.world.view.hor_rot = self.original_pos[3]
            elif self.fall_clock <= 120:
                self.world.view.hor_rot = self.original_pos[3]
                self.world.view.vert_rot = -math.pi/2
                self.world.add_mobile_quad(
                                            [self.world.view.x-100,self.world.view.y-20,self.world.view.z-100],
                                            [self.world.view.x+100,self.world.view.y-20,self.world.view.z-100],
                                            [self.world.view.x+100,self.world.view.y-20,self.world.view.z+100],
                                            [self.world.view.x-100,self.world.view.y-20,self.world.view.z+100],
                                            [.5,0,0])
            elif self.fall_clock == 121:
                self.original_pos = (self.world.view.x,self.world.view.y,self.world.view.z,self.world.view.hor_rot,self.world.view.vert_rot)
            elif self.fall_clock < 180:
                t = (self.fall_clock-120)/(180-120)
                self.world.view.y = self.original_pos[1] + t*(self.world.properties["player_height"]-.1)
            elif self.fall_clock == 180:
                self.falling=False
                self.fall_clock = 0
                return
            else:
                raise Exception("No")
        self.fall_clock += 1
        
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
            
            
            if self.mouse("left", "down") or self.key("q", "down"):
                turn = angle_distance(self.world.properties["ski_direction"], self.world.view.hor_rot)
                #acc = .0065
                acc = .0085
                min_acc = .002
                slow_factor = 1.1
                self.world.properties["ski_direction"] = self.world.view.hor_rot
                self.world.properties["momentum_direction"] = self.world.properties["ski_direction"]
                
                p1,p2,p3 = self.xyz_of_current_triangle(v.z, v.x)
                floor_hr, floor_vr = get_plane_rotation(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
                
                if floor_vr < 0:
                    floor_vr = -floor_vr
                    floor_hr += math.pi
                
                floor_slope = math.pi/2 - floor_vr
                
                
                resistance = angle_distance(self.world.properties["ski_direction"], floor_hr)
                if resistance > math.pi/2.3: 
                    target_speed = 0
                else:
                    target_speed = 1.5 * ((math.cos(resistance)) * floor_slope/(math.pi/2)) if resistance > math.pi/4 else 9999999999999999999999999
                #fasteracc = acc * (floor_slope/(math.pi/2))**2*9
                acc = acc * (floor_slope/(math.pi/2))**2*9
                if acc < min_acc: acc = min_acc
                
                if self.world.properties["momentum"] < target_speed-acc:
                    self.world.properties["momentum"] += acc
                elif self.world.properties["momentum"] > target_speed+acc:
                    if turn > math.pi/40 and acc == min_acc:#for stopping on flats
                        self.world.properties["momentum"] -= .1
                        if self.world.properties["momentum"] < .04: self.world.properties["momentum"] = .04
                    else:#for decelerating on hills
                        minus = self.world.properties["momentum"] - acc
                        divide = 99999999#self.world.properties["momentum"] / slow_factor
                        self.world.properties["momentum"] = min([minus, divide])
                        
                else:
                    self.world.properties["momentum"] = target_speed
                
                v.x += self.world.properties["momentum"] * math.cos(self.world.properties["momentum_direction"])
                v.z += self.world.properties["momentum"] * -math.sin(self.world.properties["momentum_direction"])
                v.y = self.get_elevation_continuous(v.z, v.x)*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
                
                if self.world.properties["momentum"] > constants["fall_speed"]:
                    if random() < constants["fall_chance"]:
                        self.falling = True
                        self.world.properties["momentum"] = 0
                
            
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
        if self.game_mode.startswith("ski"):
            warning_light_x1 = 10
            warning_light_y1 = 10
            warning_light_x2 = 210
            warning_light_y2 = 210
            warning_light_x2_bad = 300
            warning_light_y2_bad = 300
            warning_light_precision = 15
            """
            if self.world.properties["momentum"] > constants["fall_speed"]:
                self.draw_circle(warning_light_x1,warning_light_y1,warning_light_x2_bad,warning_light_y2_bad,Color(1,0,0),precision=warning_light_precision)
            elif self.world.properties["momentum"] > constants["fall_speed"]*.70:
                self.draw_circle(warning_light_x1,warning_light_y1,warning_light_x2,warning_light_y2,Color(1,.6,0),precision=warning_light_precision)
            elif self.world.properties["momentum"] > constants["fall_speed"]*.40:
                self.draw_circle(warning_light_x1,warning_light_y1,warning_light_x2,warning_light_y2,Color(1,1,0),precision=warning_light_precision)
            else:
                self.draw_circle(warning_light_x1,warning_light_y1,warning_light_x2,warning_light_y2,Color(0,1,0),precision=warning_light_precision)
            """
            warning_margin = .85
            if self.world.properties["momentum"] > constants["fall_speed"]*warning_margin:
                self.draw_circle(warning_light_x1,warning_light_y1,warning_light_x2_bad,warning_light_y2_bad,Color(1,0,0),precision=warning_light_precision)
            else:
                self.draw_circle(warning_light_x1,warning_light_y1,warning_light_x2,warning_light_y2,Color((self.world.properties["momentum"]/(constants["fall_speed"]*warning_margin))**.3,(1-self.world.properties["momentum"]/(constants["fall_speed"]*warning_margin))**.3,0),precision=warning_light_precision)
        
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
