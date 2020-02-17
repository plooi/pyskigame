import math
from pylooiengine import *
import map_edit_menu
import ski_menu
import lift
from normal import *
import ski_draw
from random import random
from constants import x as constants
from tree import Tree
from rock import Rock
import models
from lift import Pole
from bump import Bump
from world_object import WorldObject
import mission_center
import model_3d
import pylooiengine







class UI(LooiObject):
    def __init__(self, world, game_mode):
        super().__init__(active=False)
        self.set_layer(100)
        self.world = world
        world.game_ui = self
        self.crosshairs = False
        self.crosshair_length = 30
        self.interface_mode = "game"#"game" or "menu" or "can_move_temporarily"
        self.game_mode = game_mode#"map editor" or "ski" or ski test
        
        self.skis = "on"
        self.ski_put_on_timer = 0
        self.skis_changing = False
        
        self.clock = 0
        self.menu = None
        self.slope = 0
        
        #for chairlift riding
        self.my_lift = None
        self.my_chair = None
        self.can_load = False
        self.can_unload = False
        self.load_icon = image("textures/Chair Load Icon.png")
        self.unload_icon = image("textures/Chair Unload Icon.png")
        
        
        self.chair_sit_forward_distance = 0
        
        #fall stuff
        self.fall_clock = 0
        self.falling = False
        
        self.slipping = False
        
        self.health_timer = 0#time how long you want to show the health bar
        self.health_target = self.world.properties["health"]
        
        
        
        self.wind_vol = 0
        self.lift_vol = 0
        self.swish_timer = 0
        
        self.wind_sound = self.new_sound("sounds/Wind.ogg",volume=0)
        self.wind_sound.play(loops = 9999999) #9999 loops is 20 days straight. I think nobody is going to play for 20 days straight so it's basically forever eh
        
        
        self.lift_sound = self.new_sound("sounds/ChairliftTerminal.ogg",volume=0)
        self.lift_sound.play(loops = 9999999)#63 years about. We should be okay
        
        
        self.swish_sound = self.new_sound("sounds/SkiSwish4.ogg", volume=1)
        
        
        self.fall_sound = self.new_sound("sounds/Fall.ogg",volume=.9)
        
        self.pole_sound_obj = self.new_sound("sounds/PoleBump1.ogg",volume=.4)
        
        self.no_look = 0
        
        
        
        
    def stop_sounds(self):
        self.wind_sound.stop()
        self.lift_sound.stop()
    def chairlift_ride(self):
        self.can_load = False
        self.can_fix = False
        self.can_unload = False
        chair_ride_distance = constants["chair_ride_distance"]
        x = self.world.view.x
        y = self.world.view.y
        z = self.world.view.z
        
        
        
        for chairlift in lift.active_lifts:
            if chairlift.broken: continue
            cp = chairlift.chair_positions
            for term in [chairlift.start_terminal, chairlift.end_terminal]:
                dist = ( (term.real_z-z)**2 + (term.real_y-y)**2 + (term.real_x-x)**2 )**.5
                if dist <= 10:#if close to a terminal
                    if self.my_lift == None and self.my_chair == None:#if not currently riding
                        for i in range(len(cp)):
                            i = len(cp)-1-i
                            if ( (cp[i][0]-x)**2 + (cp[i][1]-constants["chair_sit_under_distance"]-y)**2 + (cp[i][2]-z)**2 )**.5 < chair_ride_distance:#if a chair is close
                            
                                self.can_load = True
                                if self.key(constants["interact_key"], "pressed"):
                                    
                                    self.my_lift = chairlift
                                    self.my_chair = i
                                    self.my_lift.player_riding = i
                                    self.world.properties["momentum"] = 0
                                    #return
                    else:#if currently riding
                        self.can_unload = True
                        if self.key(constants["interact_key"], "pressed"):
                            self.my_lift.player_riding = None
                            self.my_lift = None
                            self.my_chair = None
                            #return
        
        
        
        
        
        if self.my_lift != None and self.my_chair != None:
            self.world.view.x = self.my_lift.chair_positions[self.my_chair][0] + math.cos(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.view.y = self.my_lift.chair_positions[self.my_chair][1] - constants["chair_sit_under_distance"]
            self.world.view.z = self.my_lift.chair_positions[self.my_chair][2] - math.sin(self.my_lift.chair_angles[self.my_chair]) * self.chair_sit_forward_distance
            self.world.properties["ski_direction"] = self.my_lift.chair_angles[self.my_chair]
            self.world.properties["do_floor_textures"] = False
            if self.game_mode == "map editor":
                if self.key(constants["interact_key"], "pressed"):#this should only be available in map editor!!!!!!!!!!!!!!!!!!
                    self.my_lift = None
                    self.my_chair = None
            return True
        self.world.properties["do_floor_textures"] = True
        return False
    def put_on_or_take_off_skis(self):
        if self.skis_changing:
            if self.ski_put_on_timer == 0:
                self.world.view.vert_rot = 0
            elif self.ski_put_on_timer < 20:
                self.world.view.vert_rot -= math.pi/4/15
            elif self.ski_put_on_timer < 50:
                self.world.view.vert_rot -= math.pi/8/30
            elif self.ski_put_on_timer < 70:
                self.world.view.vert_rot -= math.pi/30/20
            elif self.ski_put_on_timer == 70:
                if self.skis == "on":
                    self.skis = "off"
                else:
                    self.skis = "on"
            elif self.ski_put_on_timer < 90:
                self.world.view.vert_rot += math.pi/30/20
            elif self.ski_put_on_timer < 120:
                self.world.view.vert_rot += math.pi/8/30
            elif self.ski_put_on_timer < 140:
                self.world.view.vert_rot += math.pi/4/15
            elif self.ski_put_on_timer == 140:
                self.skis_changing = False
                pygame.mouse.get_rel()
            self.ski_put_on_timer += 1
            
        if self.mouse("right", "down") and self.world.properties["momentum"]==0 and self.game_mode.startswith("ski") and self.skis_changing==False:
            self.skis_changing = True
            self.ski_put_on_timer = 0
    def do_health_step(self):
        self.health_timer -= 1
        if self.game_mode.startswith("ski"):
            self.health(-.00185,False)
        if self.key(constants["interact_key"], "down"):
            self.health(0)
        health_bar_speed = 2
        if self.world.properties["health"] < self.health_target - health_bar_speed:
            self.world.properties["health"] += health_bar_speed
        elif self.world.properties["health"] > self.health_target + health_bar_speed:
            self.world.properties["health"] -= health_bar_speed
        else:
            self.world.properties["health"] = self.health_target
    def pole_sound(self, x, y, z):
        dist = ( (x-self.world.view.x)**2 + (y-self.world.view.y)**2 + (z-self.world.view.z)**2 )**.5
        if dist < 20:
            self.pole_sound_obj.play(maxtime=1000)
            
    def sounds(self):
        self.clock += 1
        if self.clock > 10000000:
            self.clock = 0
        if self.swish_timer > 0:
            self.swish_timer -= 1
            
            
        #wind
        """
        if self.clock % 600 == 0:
            self.self.wind_sound.stop()
            self.self.wind_sound.play()
        """
        vol = 0
        if self.world.properties["momentum"] == 0:
            if self.my_lift != None:
                vol = .7
            else:
                vol = .1
        else:
            vol = self.world.properties["momentum"] / 1
        if vol>1:vol=1
        if vol < .17: vol=.17
        self.wind_sound.set_volume(vol)
        
        
        #lift
        """
        if self.clock % 160 == 0:
            self.lift_sound.stop()
            self.self.lift_sound.play()
        """
        x = self.world.view.x
        y = self.world.view.y
        z = self.world.view.z
        closest_chairlift_distance = 999999999999
        for chairlift in lift.active_lifts:
            if chairlift.broken: continue
            for term in [chairlift.start_terminal, chairlift.end_terminal]:
                dist = ( (term.real_z-z)**2 + (term.real_y-y)**2 + (term.real_x-x)**2 )**.5
                if dist < closest_chairlift_distance: closest_chairlift_distance = dist
                
            
        vol = 1 - closest_chairlift_distance/50
        vol /= 2.8
        if vol < 0: vol = 0
        self.set_lift_vol(vol)
        
        #swish
        if self.world.properties["momentum"] > .1 and self.swish_timer == 0 and angle_distance(self.world.view.hor_rot+self.no_look, self.world.properties["ski_direction"]) > math.pi/10:
            self.swish_sound.stop()
            self.swish_sound.play(maxtime=2000, fade_ms = 1000)
            self.swish_timer = 25
        if self.swish_timer == 15:
            self.swish_sound.fadeout(1000)
                
            
    def set_lift_vol(self, vol):
        self.lift_vol = vol
        self.lift_sound.set_volume(self.lift_vol)
        
        
        
            
    def step(self):
        if self.key("p", "pressed"):
            print("layered",self.get_my_window().layered_looi_objects)
            print("unlayered",self.get_my_window().unlayered_looi_objects)
        """
        if self.key("p", "pressed"):
            if self.world.properties["active_missions"]:
                self.world.view.x = self.world.properties["active_missions"][0][0][1] * self.world.properties["horizontal_stretch"]
                self.world.view.z = self.world.properties["active_missions"][0][0][0] * self.world.properties["horizontal_stretch"]
            else:
                mc = mission_center.active_mission_centers[int(random() * len(mission_center.active_mission_centers))]
                self.world.view.x = mc.args["model_x"]
                self.world.view.z = mc.args["model_z"]
        """
        
        self.sounds()
                    
        self.do_health_step()
        
        if not self.skis_changing:
            self.look_around()
        if (not self.falling) and (self.my_lift==None):
            self.put_on_or_take_off_skis()
        if not self.skis_changing:
            self.e_key()
        
        if (not self.chairlift_ride()) and (not self.skis_changing):
            
            if self.game_mode == "map editor": self.map_editor_move()
            if self.game_mode == "ski" or self.game_mode == "ski test":
                if self.skis == "on":
                    if self.falling or self.slipping:
                        self.fall()
                    else:
                        self.ski_mode_move()
                        self.collision_check()
                else:
                    self.walk()
                    self.collision_check()
            
                    
        if self.game_mode.startswith("ski") and not self.falling: 
            if self.skis == "on":
                ski_draw.draw_skis(self, ski_draw.models[self.world.properties["ski_model"]])
        
        if self.key("t", "pressed") and (not self.skis_changing):
            if self.game_mode == "map editor": self.game_mode = "ski test"
            elif self.game_mode == "ski test": self.game_mode = "map editor"
        
        
        #draw sun
        self.draw_sun()
    def draw_sun(self):
        model = models.sun_model_1()
        
        model_3d.vertical_rotate_model_around_x_eq_0(model, math.pi/10)
        model_3d.horizontal_rotate_model_around_origin(model, self.world.properties["sun_angle"])
        model_3d.move_model(model, self.world.view.x, self.world.view.y, self.world.view.z)
        model_3d.add_model_to_world_mobile(model, self.world)
            
    def collision_check(self):
        hs = self.world.properties["horizontal_stretch"]
        vs = self.world.properties["vertical_stretch"]
        my_z = int(self.world.view.z/hs)
        my_x = int(self.world.view.x/hs)
        check_radius = 10
        
        if 1==1:
            real_x = self.world.view.x
            real_z = self.world.view.z
            real_y = self.world.view.y
            
            for z in range(my_z-check_radius, my_z+check_radius):
                for x in range(my_x-check_radius, my_x+check_radius):
                    if self.world.valid_floor(z,x):
                        for obj in self.world.quads[z][x].containedObjects:
                            if isinstance(obj, WorldObject):
                                if obj.touching(real_x, real_y, real_z):
                                    obj.touching_player_consequence()
                            if self.world.properties["momentum"] >= constants["crash_speed"]:
                                if isinstance(obj, Rock):
                                    if obj.design_function == models.rock_design_1:
                                        dist = (((obj.z+.5)*hs-real_z)**2 + ((obj.x+.5)*hs-real_x)**2)**.5
                                        if dist < 1:
                                            self.falling = True
                                            return
                                    elif obj.design_function == models.rock_design_2:
                                        dist = (((obj.z+.5)*hs-real_z)**2 + ((obj.x+.5)*hs-real_x)**2)**.5
                                        
                                        dist_under = obj.y - (real_y - self.world.properties["player_height"])
                                        
                                        
                                        #dist bottom = 21 dist top = 7 height 30
                                        m = -15/7
                                        b = 15
                                        height_of_rock_at_players_dist = m*dist + b
                                        
                                        if dist_under > 0 and dist <= 21:
                                            if -dist_under < height_of_rock_at_players_dist:
                                                self.falling = True
                                                return
                                elif isinstance(obj, Tree):
                                    dist = (((obj.z+.5)*hs-real_z)**2 + ((obj.x+.5)*hs-real_x)**2)**.5
                                    if dist < .85:
                                        self.falling = True
                                        return
                                elif isinstance(obj, Pole):
                                    dist = ((obj.real_z-real_z)**2 + (obj.real_x-real_x)**2)**.5
                                    if dist < .5:
                                        self.falling = True
                                        return
                            
                        
    
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
        if self.slipping:
            if self.fall_clock == 0:
                
                self.original_pos = (self.world.view.x,self.world.view.y,self.world.view.z,self.world.view.hor_rot,self.world.view.vert_rot)
            if self.fall_clock < 30:
                v = self.world.view
                #calculate floor slope
                p1,p2,p3 = self.xyz_of_current_triangle(v.z, v.x)
                floor_hr, floor_vr = get_plane_rotation(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
                
                if floor_vr < 0:
                    floor_vr = -floor_vr
                    floor_hr += math.pi
                self.world.properties["momentum_direction"] = floor_hr
                self.world.properties["momentum"] = .5
                
                v.x += self.world.properties["momentum"] * math.cos(self.world.properties["momentum_direction"])
                v.z += self.world.properties["momentum"] * -math.sin(self.world.properties["momentum_direction"])
                v.y = self.get_elevation_continuous(v.z, v.x)*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
                
                self.world.view.hor_rot = self.original_pos[3]
                self.world.view.vert_rot = self.original_pos[4]
                
            else:
                self.slipping = False
                self.falling = True
                self.fall_clock = 0
                    
                
        if self.falling:
            if self.fall_clock == 0:
                self.fall_sound.play(maxtime=1800)
                self.health(-20, animate=True)
                self.world.properties["momentum"] = 0
                self.original_pos = (self.world.view.x,self.world.view.y,self.world.view.z,self.world.view.hor_rot,self.world.view.vert_rot)
            elif self.fall_clock <= 16:
                fall_horizontal_distance = 4
                t = self.fall_clock/16
                
                
                
                
                
                self.world.view.x = self.original_pos[0] + t*fall_horizontal_distance*math.cos(self.original_pos[3])
                self.world.view.z = self.original_pos[2] - t*fall_horizontal_distance*math.sin(self.original_pos[3])
                
                
                
                hs = self.world.properties["horizontal_stretch"]
                vs = self.world.properties["vertical_stretch"]
                destination_x = self.original_pos[0] + fall_horizontal_distance*math.cos(self.original_pos[3])
                destination_z = self.original_pos[2] - fall_horizontal_distance*math.sin(self.original_pos[3])
                
                self.world.view.y = self.original_pos[1]*(1-t) + t*(self.world.get_elevation_continuous(destination_z/hs, destination_x/hs)*vs + .18)
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
    def walk(self):
        if self.interface_mode == "game" or self.interface_mode == "can_move_temporarily":
            
                
                
            p1,p2,p3 = self.xyz_of_current_triangle(self.world.view.z, self.world.view.x)
            floor_hr, floor_vr = get_plane_rotation(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
               
            if floor_vr < 0:
                floor_vr = -floor_vr
                floor_hr += math.pi
            floor_slope = math.pi/2 - floor_vr
            
            
            if self.key("w", "down"):
                if floor_slope < math.pi/6 or angle_distance(self.world.view.hor_rot, floor_hr) > math.pi/2:
                    d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot, constants["ski_mode_walk_speed"])
                    self.world.view.x += d_x
                    self.world.view.z += d_z
                    self.health(-.007,False)
            if self.key("a", "down"):
                if floor_slope < math.pi/6 or angle_distance(self.world.view.hor_rot+math.pi/2, floor_hr) > math.pi/2:
                    d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot+math.pi/2, constants["ski_mode_walk_speed"])
                    self.world.view.x += d_x
                    self.world.view.z += d_z
                    self.health(-.007,False)
            if self.key("d", "down"):
                if floor_slope < math.pi/6 or angle_distance(self.world.view.hor_rot-math.pi/2, floor_hr) > math.pi/2:
                    d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot-math.pi/2, constants["ski_mode_walk_speed"])
                    self.world.view.x += d_x
                    self.world.view.z += d_z
                    self.health(-.007,False)
            if self.key("s", "down"):
                if floor_slope < math.pi/6 or angle_distance(self.world.view.hor_rot-math.pi, floor_hr) > math.pi/2:
                    d_x, d_z = self.convert_to_x_z(self.world.view.hor_rot-math.pi, constants["ski_mode_walk_speed"])
                    self.world.view.x += d_x
                    self.world.view.z += d_z
                    self.health(-.007,False)
                
                
                
                
            v = self.world.view
            v.y = self.get_elevation_continuous(v.z, v.x)*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
    def health(self, value, timer = True, animate=False, relative=True):
        if relative:
            self.health_target = self.health_target + value
        else:
            self.health_target = value
        if self.health_target > 100: self.health_target = 100
        if self.health_target < 0: self.health_target = 0
        if timer:
            self.health_timer = 85
    def ski_mode_move(self):
        
        
        v = self.world.view
        if self.interface_mode == "game" or self.interface_mode == "can_move_temporarily":
            
                
            
            
            g = .1
            ski_g = .030
            
            fall_speed = constants["fall_speed"]
            
            
            if self.key("w", "down"):
                if not self.world.valid_floor(int(v.z/self.world.properties["horizontal_stretch"]), int(v.x/self.world.properties["horizontal_stretch"])):
                    return;
                is_ice = self.world.is_ice(int(v.z/self.world.properties["horizontal_stretch"]), int(v.x/self.world.properties["horizontal_stretch"]))
                
                
                #after you finish going through ice
                recovering_from_ice = False
                if not is_ice:
                        angle_inc = math.pi/50
                        if angle_distance(self.world.properties["ski_direction"], self.world.properties["momentum_direction"])>0 and self.world.properties["momentum"]>.01:
                            recovering_from_ice = True
                            if (angle_distance(self.world.properties["momentum_direction"]+angle_inc, self.world.properties["ski_direction"]) 
                                <
                                angle_distance(self.world.properties["momentum_direction"]-angle_inc, self.world.properties["ski_direction"]) 
                                ):
                                self.world.properties["momentum_direction"] += angle_inc
                            else:
                                self.world.properties["momentum_direction"] -= angle_inc
                
                
                
                #ski turns toward view, but lags behind view
                angle_d = angle_distance(self.world.properties["ski_direction"], self.world.view.hor_rot+self.no_look)
                angle_inc = math.pi/6.5 *angle_d/(math.pi/2)
                if angle_inc < math.pi/550:
                    angle_inc = math.pi/550
                if angle_d > angle_inc and self.world.properties["momentum"] > .05:
                    if (angle_distance(self.world.properties["ski_direction"]+angle_inc, self.world.view.hor_rot+self.no_look) 
                        <
                        angle_distance(self.world.properties["ski_direction"]-angle_inc, self.world.view.hor_rot+self.no_look) 
                        ):
                        self.world.properties["ski_direction"] += angle_inc
                    else:
                        self.world.properties["ski_direction"] -= angle_inc
                    
                else:
                    self.world.properties["ski_direction"] = self.world.view.hor_rot+self.no_look
            
                
                
                #calculate floor slope
                p1,p2,p3 = self.xyz_of_current_triangle(v.z, v.x)
                floor_hr, floor_vr = get_plane_rotation(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
                
                if floor_vr < 0:
                    floor_vr = -floor_vr
                    floor_hr += math.pi
                
                floor_slope = math.pi/2 - floor_vr
                self.slope = floor_slope
                
                
                #calculate force pulling down
                resistance = angle_distance(self.world.properties["ski_direction"], floor_hr)   
                
                if is_ice:
                    equivalent_floor_slope = floor_slope
                else:
                    equivalent_floor_slope = math.cos(resistance) * floor_slope
                
                f_parallel = ski_g * math.sin(equivalent_floor_slope)
                
                fhorizontal = f_parallel * math.cos(equivalent_floor_slope)
                
                self.world.properties["momentum"] += fhorizontal
                
                
                #slow down when pressing x
                if (self.mouse("left", "down")) and (not is_ice):
                    if equivalent_floor_slope < math.pi/12:
                        self.world.properties["momentum"] -= .021
                    else:
                        self.world.properties["momentum"] -= .021*(resistance/(math.pi/2))**.5
                
                
                #fall when it's steep
                if self.world.properties["momentum"] > fall_speed and floor_slope >= constants["fall_slope"]:
                    if random() < .04:
                        self.falling = True
                #fall when you have low health
                if self.world.properties["health"] <= 0:
                    if self.world.properties["momentum"] > .15:
                        if random() < .005:
                            self.falling = True
                
                #fall on ice
                #if is_ice and angle_distance(self.world.properties["momentum_direction"], floor_hr) > math.pi/4 and self.world.properties["momentum"]>.4:
                if is_ice and self.world.properties["momentum"] > constants["ice_fall_speed"]:
                    #fall unless youre pointed exactly downhill
                    if angle_distance(self.world.properties["momentum_direction"], floor_hr) > math.pi/15:
                        self.slipping = True
                #if is_ice and resistance > math.pi/2 and self.world.properties["momentum"] > 0:
                #    self.slipping = True
                
                
                #friction
                self.world.properties["momentum"] -= .0068 * self.world.properties["momentum"]**2
                
                
                
                
                #momentum direction
                if is_ice:#ice momentum
                    if self.world.properties["momentum"] < .2:
                        inc = 99999999999999
                    else:
                        inc = math.pi/100
                    target = self.world.properties["ski_direction"]
                    if angle_distance(target, floor_hr) > math.pi/6:
                        if angle_distance(target, floor_hr+math.pi/6)<angle_distance(target, floor_hr-math.pi/6):
                            target = floor_hr+math.pi/6
                        else:
                            target= floor_hr-math.pi/6
                    #target = angle_avg(self.world.properties["ski_direction"], floor_hr)
                    #print("floor hr",simp(floor_hr)/math.pi, "ski dir", simp(self.world.properties["ski_direction"])/math.pi,"target",simp(target)/math.pi)
                    if angle_distance(self.world.properties["momentum_direction"],target) < inc:
                        self.world.properties["momentum_direction"] = target
                    else:
                        if angle_distance(self.world.properties["momentum_direction"]+inc,target) < angle_distance(self.world.properties["momentum_direction"]-inc,target):
                            self.world.properties["momentum_direction"] += inc
                        else:
                            self.world.properties["momentum_direction"] -= inc
                else:#snow momentum
                    
                    if not recovering_from_ice:
                        self.world.properties["momentum_direction"] = self.world.properties["ski_direction"]
                    
                    
                
                #ice slowing down if skis perpendicular
                if is_ice:
                    
                    slow = (resistance/(math.pi/3))**2
                    if slow > 1:
                        slow = 1
                    slow *= .025
                    self.world.properties["momentum"] -= slow
                    if self.world.properties["momentum"] < .2:
                        self.world.properties["momentum"] = .2
                
                
                
                if floor_slope < math.pi/8 and self.world.properties["momentum"]<.025 and self.key("w","down") and not self.mouse("left","down"):
                    self.world.properties["momentum"]=.025
                
                
                #no going backwards
                if self.world.properties["momentum"] < 0: self.world.properties["momentum"] = 0
                
                #increment view x,y,z
                v.x += self.world.properties["momentum"] * math.cos(self.world.properties["momentum_direction"])
                v.z += self.world.properties["momentum"] * -math.sin(self.world.properties["momentum_direction"])
                v.y = self.get_elevation_continuous(v.z, v.x)*self.world.properties["vertical_stretch"] + self.world.properties["player_height"]
                
                
                    
            else:
                if self.world.properties["momentum"] > .1:
                    self.falling = True
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
            if self.key(constants["no_look_key"], "down"):
                self.no_look += -(rel[0])*self.world.view.rot_spd*.4
                self.world.view.hor_rot += -(rel[0])*self.world.view.rot_spd*.6
                self.world.view.vert_rot += -(rel[1])*self.world.view.rot_spd
            else:
                self.world.view.hor_rot += -(rel[0])*self.world.view.rot_spd
                self.world.view.vert_rot += -(rel[1])*self.world.view.rot_spd
                self.no_look = 0
                
            
                
                
            
            
            
            if self.world.view.vert_rot > self.world.view.max_vert_rot:
                self.world.view.vert_rot = self.world.view.max_vert_rot
            if self.world.view.vert_rot < -self.world.view.max_vert_rot:
                self.world.view.vert_rot = -self.world.view.max_vert_rot
    def e_key(self):
        if self.key(constants["menu_key"], "pressed"):
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
            
            if self.health_timer > 0:
                #draw health bar
                bar_x = 40
                bar_y = 1030
                bar_width = 200
                bar_height = 10
                full_part_width = bar_width * self.world.properties["health"]/100
                back = black
                front = yellow
                
                self.draw_rect(bar_x, bar_y, bar_x+full_part_width, bar_y+bar_height, front)
                self.draw_rect(bar_x, bar_y, bar_x+bar_width, bar_y+bar_height, back)
        
            #if self.world.properties["momentum"] > .02:
            if self.key("w", "down") and self.skis=="on":
                pointer_radius = 15
                angle_d = angle_distance(self.world.properties["ski_direction"],self.world.view.hor_rot)/(math.pi/2)
                if angle_d > 1: angle_d = 1
                if angle_d < -1: angle_d = -1
                if angle_distance(self.world.properties["ski_direction"]+.001,self.world.view.hor_rot) < angle_distance(self.world.properties["ski_direction"]-.001,self.world.view.hor_rot):
                    angle_d = -abs(angle_d)
                else:
                    angle_d = abs(angle_d)
                
                
                
                
                if self.slope/constants["fall_slope"] < .88:
                    self.draw_circle(
                            self.get_my_window().get_internal_size()[0]/2 - pointer_radius,
                            self.get_my_window().get_internal_size()[1] - 2*pointer_radius,
                            self.get_my_window().get_internal_size()[0]/2 + pointer_radius,
                            self.get_my_window().get_internal_size()[1], Color(0,0,0))
                else:
                    self.draw_circle(
                            self.get_my_window().get_internal_size()[0]/2 - pointer_radius,
                            self.get_my_window().get_internal_size()[1] - 2*pointer_radius,
                            self.get_my_window().get_internal_size()[0]/2 + pointer_radius,
                            self.get_my_window().get_internal_size()[1], Color(1,0,0))
                self.draw_circle(
                        self.get_my_window().get_internal_size()[0]/2 - pointer_radius - (angle_d*self.get_my_window().get_internal_size()[0]/2),
                        self.get_my_window().get_internal_size()[1] - 2*pointer_radius,
                        self.get_my_window().get_internal_size()[0]/2 + pointer_radius - (angle_d*self.get_my_window().get_internal_size()[0]/2),
                        self.get_my_window().get_internal_size()[1], Color(.3,.3,.3))
                    
                    
        if self.interface_mode == "menu":
            self.draw_text(0,100,"FPS: " + str(self.world.fps.fps))
        if self.can_load:
            self.draw_image(950, 900, 1050, 1000,self.load_icon)
        if self.can_unload:
            self.draw_image(950, 910, 1050, 1010,self.unload_icon)
        #self.draw_text(0,50, "%f %f %f %f %f" % (self.world.view.x, self.world.view.y, self.world.view.z, self.world.view.hor_rot, self.world.view.vert_rot))
        #self.draw_text(0,600,str(round(self.world.properties["momentum"])))
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



def round(x):
    return int(x * 10 + .5)/10
def simp(angle):
    while angle < 0:
        angle += math.pi*2
    while angle > math.pi*2:
        angle -= math.pi*2
    return angle
def angle_avg(a1, a2):
    avg = (a1+a2)/2
    flip_avg = avg+math.pi
    if angle_distance(a1, avg) < angle_distance(a1, flip_avg):
        return avg
    else:
        return flip_avg
    
    
    
