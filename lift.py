from pylooiengine import *
import traceback
import util
from util import get_angle
from model_3d import *
import math
from random import random
from models import *
from lift_util import *
from selectable import Selectable
from constants import x as constants
import PySimpleGUI as sg
import normal
import mission_center
def main():
    l = Lift(None)
    l.add_point(Point(0,0,0,1))
    l.add_point(Point(1,0,0,1))
    l.update()
    print(l.travel(3))





def rope_model_1(elevation, horizontal_dist, 
                rope_thickness=.1, 
                color = [0,0,0]):
    r_2 = rope_thickness/2
    return [
    [0, -r_2, 0],[0, r_2, 0],[horizontal_dist, r_2+elevation, 0],[horizontal_dist, -r_2+elevation, 0], color,
    [0, 0, -r_2],[0, 0, r_2],[horizontal_dist, elevation, r_2],[horizontal_dist, elevation, -r_2], color,
    
    
    ]

active_lifts = []

class Lift(LooiObject, Selectable):
    def __init__(self, world):
        super().__init__()
        self.set_layer(0)
        self.world = world
        self.z1 = None
        self.x1 = None
        self.z2 = None
        self.x2 = None
        
        self.broken = False
        
        self.start_terminal = None
        self.end_terminal = None
        self.chairs = []
        self.poles_midpoints = []
        self.angle = None
        self.rope_speed = None
        self.terminal_speed = None
        
        self.chair_time_distance = None
        self.chair_model = None
        self.blurry_chair_model = None
        self.super_blurry_chair_model = None
        self.chair_riding_model = None
        
        self.chair_positions=None#at each step, gets updated with the positions of each chair
        self.chair_angles = None
        self.chair_segments = None
        
        self.player_riding = None#which chair is the player riding
        
        self.track = Track()
        
        self.beacon = beacon_model()
        self.can_fix = False
        self.fix_icon = image("textures/Fix Icon.png")
        self.fixing = False
        
        
    """
    [startZ, startX, [array of pole percentage values, negatives mean midpoints], endZ, endX]
    [z1, x1, [.1, .2, .3, .4, .5, .6, -.7, .8], z2, x2]
    """
    def build(self, chairlift_array, rope_speed = "detachable_rope_speed", terminal_speed = "detachable_terminal_speed", chair_time_distance = 210,
                        chair_model = chair_model_2, blurry_chair_model = chair_model_3, super_blurry_chair_model=chair_model_4, rope_model=rope_model_1,terminal_model=terminal_design_1, pole_model=pole_design_1, chair_riding_model=chair_model_2):
        self.chair_model = chair_model
        self.chair_riding_model = chair_riding_model
        self.blurry_chair_model = blurry_chair_model
        self.super_blurry_chair_model = super_blurry_chair_model
        self.chair_time_distance = chair_time_distance
        self.rope_speed = rope_speed
        self.terminal_speed = terminal_speed
        self.rope_model = rope_model_1
        self.terminal_model = terminal_model
        self.pole_model = pole_model
        self.chairlift_array = chairlift_array
        self.z1 = chairlift_array[0]
        self.x1 = chairlift_array[1]
        self.z2 = chairlift_array[3]
        self.x2 = chairlift_array[4]
        self.center_x = (self.x1+self.x2)/2
        self.center_z = (self.z1+self.z2)/2
        self.distance = ( (self.x1-self.x2)**2 + (self.z1-self.z2)**2 )**.5
        self.angle = get_angle(self.z1,self.x1,self.z2,self.x2)
        self.poles_midpoints = chairlift_array[2]
        if len(self.poles_midpoints) == 0: self.poles_midpoints.append(.5)
        if self.start_terminal != None: self.start_terminal.deactivate()
        if self.end_terminal != None: self.end_terminal.deactivate()
        self.start_terminal = Terminal(self, "bot", terminal_model)
        self.end_terminal = Terminal(self, "top", terminal_model)
        self.poles_midpoints_objects = []
        for pole_midpoint in self.poles_midpoints:
            if pole_midpoint > 0:
                self.poles_midpoints_objects.append(Pole(self, pole_midpoint, self.pole_model))
            elif pole_midpoint < 0:
                #add midpoint...
                #WIP
                pass
        self.track.points = []
        for point in self.start_terminal.track.points:
            self.track.add_point(point)
            
        for pole_midpoint in self.poles_midpoints_objects:
            if isinstance(pole_midpoint, Pole):
                self.track.add_point(Point(pole_midpoint.up_point[0], pole_midpoint.up_point[1], pole_midpoint.up_point[2], constants[self.rope_speed]))
            elif isinstance(pole_midpoint, Midpoint):
                #add midpoint...
                #WIP
                pass
        
        for point in self.end_terminal.track.points:
            self.track.add_point(point)
            
        for pole_midpoint in self.poles_midpoints_objects[::-1]:
            if isinstance(pole_midpoint, Pole):
                self.track.add_point(Point(pole_midpoint.down_point[0], pole_midpoint.down_point[1], pole_midpoint.down_point[2], constants[self.rope_speed]))
            elif isinstance(pole_midpoint, Midpoint):
                #add midpoint...
                #WIP
                pass
        
        self.track.generate_segments()
        
        
        self.set_chair_time_distance(chair_time_distance)
        
        self.rope = []#contains the indexes for the rope, if they ever need to be removed again
        
        
        self.do_rope()
        
        self.activate()
        move_model(self.beacon, self.start_terminal.real_x, self.start_terminal.real_y, self.start_terminal.real_z)
        return self
    def set_chair_time_distance(self, chair_time_distance):
        self.chairs = []
        self.chair_time_distance = chair_time_distance
        chair_time = 0
        total_length = self.round_trip_time()
        while chair_time < total_length:
            self.chairs.append(chair_time)
            chair_time += chair_time_distance
            
        if len(self.chairs) > 0: self.chairs = self.chairs[0:-1]
        
        self.chair_positions = [[-9999999,-9999999,-9999999]] * len(self.chairs)
        self.chair_angles = [0] * len(self.chairs)
        self.chair_segments = [-1] * len(self.chairs)

    def fix_underground_spots(self, rep=0):
        if rep > 15:
            return
        travel = 0
        segment_index = 0
        for i in range(0,int(self.round_trip_time())):
            position, angle = self.travel(i)
            if position[1] < self.world.get_elevation_continuous(position[2]/self.world.properties["horizontal_stretch"], position[0]/self.world.properties["horizontal_stretch"])*self.world.properties["vertical_stretch"]:

                #underground
                
                
                
                
                total_distance = ((self.x1-self.x2)**2 + (self.z1-self.z2)**2)**.5 * self.world.properties["horizontal_stretch"]
                pole_distance = ((self.x1*self.world.properties["horizontal_stretch"]-position[0])**2 + (self.z1*self.world.properties["horizontal_stretch"]-position[2])**2)**.5
                
                fraction = pole_distance / total_distance
                if fraction > 1: fraction = 1
                #print(fraction)
                
                for j in range(len(self.chairlift_array[2])):
                    if self.chairlift_array[2][j] > fraction:
                        
                        self.chairlift_array[2].insert(j, fraction)
                        self.reset().fix_underground_spots(rep+1)
                        #print(self.chairlift_array)
                        return
                else:
                    self.chairlift_array[2].append(fraction)
                    self.reset().fix_underground_spots(rep+1)
                    #print(self.chairlift_array)
                    return
                        
                        
    def travel(self, travel_time):
        time = 0
        segment_index = 0
        rtt = self.round_trip_time()
        while 1:
                #make sure the time is between 0 and the round trip time, not more.
                while travel_time >= rtt:
                    #the chair has already gone around the entire lift
                    travel_time -= rtt
                if travel_time < time:
                    #restart because chair is before this segment
                    time = 0
                    segment_index = 0
                elif travel_time < time + self.track.segments[segment_index].get_time_duration():
                    #chair is in this segment
                    position = self.track.segments[segment_index].travel(travel_time - time)
                    angle = self.track.segments[segment_index].horizontal_angle()
                    
                    return position, angle
                else:
                    #chair is in a future segment
                    time += self.track.segments[segment_index].get_time_duration()
                    segment_index += 1
        
    def reset(self):
        self.delete()
        return Lift(self.world).build(self.chairlift_array, self.rope_speed, self.terminal_speed, self.chair_time_distance, self.chair_model, self.blurry_chair_model, self.super_blurry_chair_model,terminal_model=self.terminal_model,pole_model=self.pole_model,chair_riding_model=self.chair_riding_model)
        
    def do_rope(self):
        objs = [self.start_terminal] + self.poles_midpoints_objects + [self.end_terminal]
        i = 0
        for object in objs:
            rope_start = None
            rope_stop = None
            rope_start2 = None
            rope_stop2 = None
            if isinstance(object, Terminal):
                rope_start = object.track[-1]
                if object.top_or_bot == "bot":
                    rope_stop = objs[1].up_point
                else:
                    rope_stop = objs[-2].down_point
            elif isinstance(object, Pole):
                rope_start = object.up_point
                if i == len(objs)-2:
                    rope_stop = objs[-1].track[0]
                else:
                    #add if it's a midpoint here
                    rope_stop = objs[i+1].up_point
                
                rope_start2 = object.down_point
                if i == 1:
                    rope_stop2 = objs[0].track[0]
                else:
                    #add if it's a midpoint here
                    rope_stop2 = objs[i-1].down_point
            elif isinstance(object, Midpoint):
                pass
            if rope_start != None and rope_stop != None:
                self.make_rope(rope_start, rope_stop)
            if rope_start2 != None and rope_stop2 != None:
                self.make_rope(rope_start2, rope_stop2)
            i += 1
    def make_rope(self, start, stop):
        
                
        elevation = stop[1] - start[1]
        dist = (  (stop[0]-start[0])**2 + (stop[2]-start[2])**2  )**.5
        model = self.rope_model(elevation, dist)
        horizontal_rotate_model_around_origin(model, get_angle(start[2],start[0],stop[2],stop[0]))
        
        
        move_model(model,start[0], start[1], start[2])
        
        anchor_z, anchor_x = int(start[2]/self.world.properties["horizontal_stretch"]), int(start[0]/self.world.properties["horizontal_stretch"])
        
        keys = add_model_to_world_fixed(model, self.world, anchor_z, anchor_x, None)
        self.rope.append((keys, anchor_z, anchor_x))
                    
            
        
    def delete(self):
        self.start_terminal.delete()
        self.end_terminal.delete()
        for polemid in self.poles_midpoints_objects:
            polemid.delete()
            
            
        for keys, anchor_z, anchor_x in self.rope:
            rm_model_from_world_fixed(keys, self.world, anchor_z, anchor_x)
            
        self.deactivate()
    def round_trip_time(self):
        ret = 0
        for segment in self.track:
            ret += segment.get_time_duration()
        return ret
    def add_point(self, point, index=None):
        self.track.add_point(point, index = index)
    def update(self):
        self.track.generate_segments()
    def step(self):
        
        #this is so that there is one frame between when I press r and when the lift is fixed
        if self.fixing:
            self.world.properties["active_missions"] = []
            mission_center.check_reset_missions()#for now, just end the mission, because I don't want to have to program the body
            #remember, you have to do the case for if there are no lifts
            #give the save the buddy mission
            #TODO...
        
        self.broken=False
        for mission in self.world.properties["active_missions"]:
            if mission[1] == 2:#lift fix mission
                z,x = mission[0]
                if z==self.z1 and x==self.x1:
                    self.broken=True
                    if self.key(constants["find_key"], "down"):
                        add_model_to_world_mobile(self.beacon, self.world)
        
        
        self.can_fix = False
        self.fixing = False
        if self.broken:
            if ( 
                (self.world.view.x-self.start_terminal.real_x)**2 + 
                (self.world.view.z-self.start_terminal.real_z)**2 )**.5 < 4.5 or ( 
                (self.world.view.x-self.end_terminal.real_x)**2 + 
                (self.world.view.z-self.end_terminal.real_z)**2 )**.5 < 4.5:
                self.can_fix = True
                if self.key(constants["interact_key"], "pressed"):
                    self.fixing=True
                    
        if ( 
            (self.world.view.x/self.world.properties["horizontal_stretch"]-self.center_x)**2 + 
            (self.world.view.z/self.world.properties["horizontal_stretch"]-self.center_z)**2 )**.5 > 5 + self.distance/2 + self.world.view.line_of_sight*self.world.properties["chunk_size"]:
            return
        
        
        
        
        rtt = self.round_trip_time()
        
        segment_index = 0
        time = 0 #time_up_to_not_including_this_segment



        for i in range(len(self.chairs)):
            #try to find position and angle for chair i
            while 1:
                
                
                #make sure the time is between 0 and the round trip time, not more.
                while self.chairs[i] >= rtt:
                    #the chair has already gone around the entire lift
                    self.chairs[i] -= rtt
                
                if self.chairs[i] < time:
                    #restart because chair is before this segment
                    time = 0
                    segment_index = 0
                elif self.chairs[i] < time + self.track.segments[segment_index].get_time_duration():
                    #chair is in this segment
                    chair_i_position = self.track.segments[segment_index].travel(self.chairs[i] - time)
                    chair_i_angle = self.track.segments[segment_index].horizontal_angle()
                    
                    self.chair_positions[i] = chair_i_position
                    self.chair_angles[i] = chair_i_angle
                    
                    #if self.track.segments[segment_index].speed != constants[self.rope_speed] and self.track.segments[segment_index].speed != constants[self.terminal_speed]:
                        #print("rope",constants[self.rope_speed],"term",constants[self.terminal_speed],"this dude",self.track.segments[segment_index].speed)
                    
                    if segment_index != self.chair_segments[i] and self.chair_segments[i] != -1:#if this chair is entering a new segment
                        if self.track.segments[segment_index-1].speed == constants[self.rope_speed]:#and the previous segment is rope speed
                            if self.track.segments[segment_index].speed == constants[self.rope_speed]:#and this new segment is rope speed
                                #then we must be going over a bu bu bump
                                self.world.game_ui.pole_sound(chair_i_position[0], chair_i_position[1], chair_i_position[2])
                    
                    
                    self.chair_segments[i] = segment_index
                    
                    #execute the chair drawing
                    if self.world.in_los(chair_i_position[2], chair_i_position[0], scaled=True):
                        if self.player_riding == i:
                            model = self.chair_riding_model()
                            horizontal_rotate_model_around_origin(model, chair_i_angle)
                            move_model(model, chair_i_position[0], chair_i_position[1], chair_i_position[2])
                            
                            add_model_to_world_mobile(model, self.world)
                        elif self.world.in_los(chair_i_position[2], chair_i_position[0], scaled=True, los=self.world.view.line_of_sight/6):
                            model = self.chair_model()
                            horizontal_rotate_model_around_origin(model, chair_i_angle)
                            move_model(model, chair_i_position[0], chair_i_position[1], chair_i_position[2])
                        
                            add_model_to_world_mobile(model, self.world)
                        elif self.world.in_los(chair_i_position[2], chair_i_position[0], scaled=True, los=self.world.view.line_of_sight/2.5):
                            model = self.blurry_chair_model()
                            horizontal_rotate_model_around_origin(model, chair_i_angle)
                            move_model(model, chair_i_position[0], chair_i_position[1], chair_i_position[2])
                        
                            add_model_to_world_mobile(model, self.world)
                        else:
                            model = self.super_blurry_chair_model()
                            horizontal_rotate_model_around_origin(model, chair_i_angle)
                            move_model(model, chair_i_position[0], chair_i_position[1], chair_i_position[2])
                        
                            add_model_to_world_mobile(model, self.world)
                    
                    if not self.broken:
                        self.chairs[i] += 1#increment the time
                    
                    
                    break#move on to next chair
                else:
                    #chair is in a future segment
                    time += self.track.segments[segment_index].get_time_duration()
                    segment_index += 1
                    
                    
                
                
    def activate(self):
        super().activate()
        if self not in active_lifts:
            active_lifts.append(self)
    def deactivate(self):
        super().deactivate()
        if self in active_lifts:
            active_lifts.remove(self)
          
    def open_menu(self):
        
        layout = [
            
            [sg.Button("Delete")],
            [sg.Button("Reset")] ,
            [sg.Button("Fix Underground Spots")],
            [sg.Text("Pole Locations:"), sg.Multiline(default_text=str(self.chairlift_array[2]), size=(300,10))],
            [sg.OK()]
        ]
        
        
        window = sg.Window("Chairlift", layout, size=(500,800))
        event, values = window.Read()
        
        if event == "Delete":
            self.delete()
        elif event == "Reset":
            self.reset()
        elif event == "Fix Underground Spots":
            self.fix_underground_spots()
        elif event == "OK":
            try:
                new_pole_locations = eval(values[0])
                if new_pole_locations != self.chairlift_array[2] and type(new_pole_locations) == type([]):
                    for item in new_pole_locations:
                        if type(item) == type(1) or type(item) == type(1.0):
                            pass
                        else:
                            raise Exception()
                    self.chairlift_array[2] = new_pole_locations
                    self.reset()
            except:
                pass
        
        
        
        
        
        window.close()

    def paint(self):
        
        if self.can_fix:
            self.draw_image(950, 900, 1050, 1000,self.fix_icon)
        if self.broken and self.key(constants["find_key"], "down"):
            indicator_width = 10
            indicator_height = 50
            indicator_color = Color(1,1,0)
            half_screen = self.get_my_window().get_internal_size()[0]/2
            player_to_me = util.get_angle(self.world.view.z, self.world.view.x, self.start_terminal.real_z, self.start_terminal.real_x)
            diff = normal.angle_distance(self.world.view.hor_rot, player_to_me)
            if normal.angle_distance(self.world.view.hor_rot + .001, player_to_me) < normal.angle_distance(self.world.view.hor_rot - .001, player_to_me):
                #this mission center is left of the player
                x = diff/(math.pi/2)
                if x > 1:
                    x = 1
                x = half_screen - x*half_screen
            else:
                #this mission centre is left of the player
                x = diff/(math.pi/2)
                if x > 1:
                    x = 1
                x = half_screen + x*half_screen
            self.draw_rect(x-indicator_width/2, 0, x+indicator_width/2, indicator_height, indicator_color)
    

class Pole:
    def __init__(self, chairlift, lift_line_fraction, pole_model):
        self.chairlift = chairlift
        self.pole_model = pole_model
        
        self.angle = chairlift.angle
        
        self.lift_line_fraction = lift_line_fraction
        inverted_lift_line_fraction = 1-lift_line_fraction
        self.x = chairlift.x1 * inverted_lift_line_fraction + chairlift.x2 * lift_line_fraction
        self.z = chairlift.z1 * inverted_lift_line_fraction + chairlift.z2 * lift_line_fraction
        
        self.real_y = chairlift.world.get_elevation_continuous(self.z, self.x)*chairlift.world.properties["vertical_stretch"]
        self.real_x = self.x * self.chairlift.world.properties["horizontal_stretch"]
        self.real_z = self.z * self.chairlift.world.properties["horizontal_stretch"]
        
        self.model,self.up_point,self.down_point = self.pole_model()
        horizontal_rotate_model_around_origin(self.model, self.angle)
        move_model(self.model, self.real_x, self.real_y, self.real_z)
        self.vhkeys = add_model_to_world_fixed(self.model, self.chairlift.world, int(self.z), int(self.x), self)
        
        horizontal_rotate_around_origin(self.up_point, self.angle)
        horizontal_rotate_around_origin(self.down_point, self.angle)
        move_point(self.up_point, self.real_x, self.real_y, self.real_z)
        move_point(self.down_point, self.real_x, self.real_y, self.real_z)
    def delete(self):
        rm_model_from_world_fixed(self.vhkeys, self.chairlift.world, int(self.z), int(self.x), self)
class Terminal:
    def __init__(self, chairlift, top_or_bot, terminal_model):
        self.chairlift = chairlift
        self.angle = 0
        
        if top_or_bot == "top":
            self.angle = chairlift.angle + math.pi
            self.x = chairlift.x2
            self.z = chairlift.z2
            
        else:
            self.angle = chairlift.angle
            self.x = chairlift.x1
            self.z = chairlift.z1
        self.top_or_bot = top_or_bot
        
        
        self.real_y = chairlift.world.get_elevation_continuous(self.z, self.x)*chairlift.world.properties["vertical_stretch"]
        
        self.real_x = self.x * self.chairlift.world.properties["horizontal_stretch"]
        self.real_z = self.z * self.chairlift.world.properties["horizontal_stretch"]
        
        self.model,self.track = terminal_model(rope_speed=constants[chairlift.rope_speed], terminal_speed=constants[chairlift.terminal_speed])
        horizontal_rotate_model_around_origin(self.model, self.angle)
        move_model(self.model, self.real_x, self.real_y, self.real_z)
        self.vhkeys = add_model_to_world_fixed(self.model, self.chairlift.world, int(self.z), int(self.x), self)
        
        horizontal_rotate_track_around_origin(self.track, self.angle)
        move_track(self.track, self.real_x, self.real_y, self.real_z)
    def delete(self):
        rm_model_from_world_fixed(self.vhkeys, self.chairlift.world, int(self.z), int(self.x), self)



def beacon_model(
    width=3,
    height=1000):
    
    return [
        [-width/2,0,-width/2],[width/2,0,-width/2],[width/2,height,-width/2],[-width/2,height,-width/2],[.8,.8,.5],
        [-width/2,0,width/2],[width/2,0,width/2],[width/2,height,width/2],[-width/2,height,width/2],[.8,.8,.5],
        [-width/2,0,-width/2],[-width/2,0,width/2],[-width/2,height,width/2],[-width/2,height,-width/2],[.8,.8,.5],
        [width/2,0,-width/2],[width/2,0,width/2],[width/2,height,width/2],[width/2,height,-width/2],[.8,.8,.5],
        #[0,height-square_diagonal/2,0],[0,height,square_diagonal/2],[0,height+square_diagonal/2,0],[0,height,-square_diagonal/2],square_color,
    
    
    
    ]

if __name__ == "__main__": main()
    
    
