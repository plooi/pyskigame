from pylooiengine import *
import util
from util import get_angle
from model_3d import *
import math
from random import random
def main():
    l = Lift(None)
    l.add_point(Point(0,0,0,1))
    l.add_point(Point(1,0,0,1))
    l.update()
    print(l.travel(3))


def chair_model_1():
    return [
        [0,-.5,-.5], [0,.5,-.5], [0,.5,.5], [0,-.5,.5], [0,0,0]
    ]
def chair_model_2():
    hanger_width = .05
    hanger_height = .5
    hanger_color = [.3,.3,.3]
    seat_back_color = [.1,.1,.1]
    seat_color = [.2,.2,.2]
    
    chair_width = 1.2
    sub_hanger_height = .5
    chair_slouch=.2
    seat_width = .2
    
    seat_back_height=.2
    
    seat_tilt_up = .07
    
    h_2 = hanger_width/2
    return [
        [0,0,-h_2], [0,0,h_2], [0,-hanger_height,h_2], [0,-hanger_height,-h_2], hanger_color,
        [0,-hanger_height,-chair_width/2], [0,-hanger_height,chair_width/2], [0,-hanger_height-hanger_width,chair_width/2], [0,-hanger_height-hanger_width,-chair_width/2], hanger_color,
        [0,-hanger_height-hanger_width,-chair_width/2], [0,-hanger_height-hanger_width,-chair_width/2+hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2+hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2], hanger_color,
        [0,-hanger_height-hanger_width,chair_width/2], [0,-hanger_height-hanger_width,chair_width/2-hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2-hanger_width], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2], hanger_color,
        [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,chair_width/2], [-chair_slouch,-hanger_height-hanger_width-sub_hanger_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,-chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,chair_width/2], seat_back_color,
        [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,chair_width/2], [0,-hanger_height-hanger_width-sub_hanger_height-seat_back_height,-chair_width/2], [seat_width,-hanger_height-hanger_width-sub_hanger_height-seat_back_height+seat_tilt_up,-chair_width/2], [seat_width,-hanger_height-hanger_width-sub_hanger_height-seat_back_height+seat_tilt_up,chair_width/2], seat_color
        
        
    ]

class Lift(LooiObject):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.z1 = None
        self.x1 = None
        self.z2 = None
        self.x2 = None
        
        self.start_terminal = None
        self.end_terminal = None
        self.chairs = []
        self.poles_midpoints = []
        self.angle = None
        self.rope_speed = None
        self.terminal_speed = None
        
        self.chair_time_distance = None
        self.chair_model = None
        
        self.track = Track()
        
    """
    [startZ, startX, [array of pole percentage values, negatives mean midpoints], endZ, endX]
    [z1, x1, [.1, .2, .3, .4, .5, .6, -.7, .8], z2, x2]
    """
    def build(self, chairlift_array, rope_speed = 4, terminal_speed = 2, chair_time_distance = 7,
                        chair_model = chair_model_2):
        self.chair_model = chair_model
        self.chair_time_distance = chair_time_distance
        self.rope_speed = rope_speed
        self.terminal_speed = terminal_speed
        self.z1 = chairlift_array[0]
        self.x1 = chairlift_array[1]
        self.z2 = chairlift_array[3]
        self.x2 = chairlift_array[4]
        self.angle = get_angle(self.z1,self.x1,self.z2,self.x2)
        self.poles_midpoints = chairlift_array[2]
        if self.start_terminal != None: self.start_terminal.deactivate()
        if self.end_terminal != None: self.end_terminal.deactivate()
        self.start_terminal = Terminal(self, "bot")
        self.end_terminal = Terminal(self, "top")
        self.poles_midpoints_objects = []
        for pole_midpoint in self.poles_midpoints:
            if pole_midpoint > 0:
                self.poles_midpoints_objects.append(Pole(self, pole_midpoint))
            elif pole_midpoint < 0:
                #add midpoint...
                #WIP
                pass
        self.track.points = []
        for point in self.start_terminal.track.points:
            self.track.add_point(point)
            
        for pole_midpoint in self.poles_midpoints_objects:
            if isinstance(pole_midpoint, Pole):
                self.track.add_point(Point(pole_midpoint.up_point[0], pole_midpoint.up_point[1], pole_midpoint.up_point[2], self.rope_speed))
            elif isinstance(pole_midpoint, Midpoint):
                #add midpoint...
                #WIP
                pass
        
        for point in self.end_terminal.track.points:
            self.track.add_point(point)
            
        for pole_midpoint in self.poles_midpoints_objects[::-1]:
            if isinstance(pole_midpoint, Pole):
                self.track.add_point(Point(pole_midpoint.down_point[0], pole_midpoint.down_point[1], pole_midpoint.down_point[2], self.rope_speed))
            elif isinstance(pole_midpoint, Midpoint):
                #add midpoint...
                #WIP
                pass
        
        self.track.generate_segments()
        
        self.chairs = []
        chair_time = 0
        total_length = self.round_trip_time()
        while chair_time < total_length:
            self.chairs.append(chair_time)
            chair_time += chair_time_distance
            
        if len(self.chairs) > 0: self.chairs = self.chairs[0:-1]
    def travel(self, time):
        for segment in self.track:
            time_duration = segment.get_time_duration()
            #print("time duration: " + str(time_duration))
            if time > time_duration:
                time -= time_duration
                continue
            else:
                return (segment.travel(time), segment.horizontal_angle())
        else:
            raise TimeOverflowException(time)
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
        for i in range(len(self.chairs)):
            while True:
                try:
                    position, angle = self.travel(self.chairs[i])
                    break
                except TimeOverflowException as t:
                    self.chairs[i] = t.new_time
                    continue
            model = self.chair_model()
            horizontal_rotate_model_around_origin(model, angle)
            move_model(model, position[0], position[1], position[2])
            add_model_to_world(model, self.world)
            self.chairs[i] += 1
            

class Track:
    def __init__(self):
        self.points = []
        self.segments = []
    def add_point(self, point, index=None):
        if index == None:
            index = len(self.points)
        self.points.insert(index, point)
        return self
    def generate_segments(self):
        self.segments = []
        for i in range(len(self.points)):
            self.segments.append(Segment  (self.points[i], self.points[circular_add(i, 1, len(self.points))])  )
        return self
    def __iter__(self):
        for seg in self.segments:
            yield seg
            
class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.hr = util.get_angle(p1.z, p1.x, p2.z, p2.x)
        self.speed = p1.speed
        self.time_duration = self._calc_time_duration()
    def _calc_time_duration(self):
        distance = ( (self.p1.x-self.p2.x)**2 + (self.p1.y-self.p2.y)**2 + (self.p1.z-self.p2.z)**2 )**.5
        return distance/self.speed
    def get_time_duration(self):
        return self.time_duration
    def horizontal_angle(self):
        return self.hr
    def travel(self, time):
        fraction = time/self.time_duration
        inverted_fraction = 1-fraction
        return [
                    self.p1.x * inverted_fraction + self.p2.x * fraction,
                    self.p1.y * inverted_fraction + self.p2.y * fraction,
                    self.p1.z * inverted_fraction + self.p2.z * fraction,
                    ]
class TimeOverflowException(Exception):
    def __init__(self, new_time):
        self.new_time = new_time

class Point:
    def __init__(self, x, y, z, v):
        self.x=x
        self.y=y
        self.z=z
        self.speed=v
    def __getitem__(self, i):
        if i == 0: return self.x
        if i == 1: return self.y
        if i == 2: return self.z
        raise Exception("invalid index")
    def __setitem__(self, i, value):
        if i == 0: self.x = value
        elif i == 1: self.y = value
        elif i == 2: self.z = value
        else: raise Exception("invalid index")
    
def circular_add(a, b, max):
    ret = a+b
    while ret >= max:
        ret -= max
    return ret

def terminal_design_1(
    pole_length = 1,
    pole_width = .6,
    pole_height = 3,
    pole_color = [.3,.3,.3],
    
    terminal_roof_width = 4,
    terminal_roof_length = 7,
    terminal_track_indent = .7,
    terminal_belly_color = [.3,.3,.7],
    
    rope_speed = 3,
    terminal_speed = 1,
    bullwheel_distance_from_pole = 2,
    slow_down_segments = 15,
    bullwheel_segments = 20
    ):
    
    bullwheel_radius = terminal_roof_width/2-terminal_track_indent
    track = Track()
    
    speed_diff = rope_speed-terminal_speed
    
    for x in range(0, slow_down_segments):
        percent_round_down = x/slow_down_segments
        percent_round_up = x/(slow_down_segments-1) if slow_down_segments > 1 else 1
        x_pos = (1 - percent_round_down) * terminal_roof_length/2 
        vel = terminal_speed + (1 - percent_round_up) * speed_diff
        track.add_point(Point(x_pos, pole_height, -terminal_roof_width/2+terminal_track_indent, vel))
    for bws in range(0, bullwheel_segments+1):
        theta = bws / bullwheel_segments * math.pi + math.pi/2
        z = -math.sin(theta) * bullwheel_radius
        x = math.cos(theta) * bullwheel_radius
        x -= bullwheel_distance_from_pole
        track.add_point(Point(x, pole_height, z, terminal_speed))
    for x in range(0, slow_down_segments):
        percent_round_down = x/slow_down_segments
        percent_round_up = x/(slow_down_segments-1) if slow_down_segments > 1 else 1
        x_pos = (percent_round_up) * terminal_roof_length/2 
        vel = terminal_speed + (percent_round_up) * speed_diff
        track.add_point(Point(x_pos, pole_height, terminal_roof_width/2-terminal_track_indent, vel))
    #WORKING HERE
    return [
    [-pole_length/2,0,-pole_width/2], [pole_length/2,0,-pole_width/2], [pole_length/2,pole_height,-pole_width/2], [-pole_length/2,pole_height,-pole_width/2], pole_color,
    [-pole_length/2,0,pole_width/2], [pole_length/2,0,pole_width/2], [pole_length/2,pole_height,pole_width/2], [-pole_length/2,pole_height,pole_width/2], pole_color,
    [-pole_length/2,0,-pole_width/2], [-pole_length/2,0,pole_width/2], [-pole_length/2,pole_height,pole_width/2], [-pole_length/2,pole_height,-pole_width/2], pole_color,
    [pole_length/2,0,-pole_width/2], [pole_length/2,0,pole_width/2], [pole_length/2,pole_height,pole_width/2], [pole_length/2,pole_height,-pole_width/2], pole_color,
    
    [-terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height, -terminal_roof_width/2], [terminal_roof_length/2, pole_height, terminal_roof_width/2], [-terminal_roof_length/2, pole_height, terminal_roof_width/2], terminal_belly_color
    ], track
    


def pole_design_1():
    pole_width = 1
    pole_height = 7
    t_width = 3
    t_height = 1
    pole_color = [.2,.2,.2]
    t_color = [.6,.6,.6]
    
    p_2 = pole_width/2
    return [
    [-p_2/2,0,-p_2], [-p_2,0,p_2], [-p_2,pole_height,p_2], [-p_2,pole_height,-p_2], pole_color,
    [p_2/2,0,-p_2], [p_2,0,p_2], [p_2,pole_height,p_2], [p_2,pole_height,-p_2], pole_color,
    [-p_2/2,0,-p_2], [p_2/2,0,-p_2], [p_2,pole_height,-p_2], [-p_2,pole_height,-p_2], pole_color, 
    [-p_2/2,0,p_2], [p_2/2,0,p_2], [p_2,pole_height,p_2], [-p_2,pole_height,p_2], pole_color, 
    
    [-p_2,pole_height,-t_width/2], [p_2,pole_height,-t_width/2], [p_2,pole_height,t_width/2], [-p_2,pole_height,t_width/2], t_color,
    [-p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,t_width/2], [-p_2,pole_height+t_height,t_width/2], t_color,
    [-p_2,pole_height,-t_width/2], [p_2,pole_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [-p_2,pole_height+t_height,-t_width/2], t_color,
    [-p_2,pole_height,t_width/2], [p_2,pole_height,t_width/2], [p_2,pole_height+t_height,t_width/2], [-p_2,pole_height+t_height,t_width/2], t_color,
    [-p_2,pole_height,-t_width/2], [-p_2,pole_height+t_height,-t_width/2], [-p_2,pole_height+t_height,t_width/2], [-p_2,pole_height,t_width/2],  t_color,
    [p_2,pole_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,t_width/2], [p_2,pole_height,t_width/2],  t_color
    ],[0,pole_height,t_width/2], [0,pole_height,-t_width/2], 
class Pole:
    def __init__(self, chairlift, lift_line_fraction):
        self.chairlift = chairlift
        
        self.angle = chairlift.angle
        
        self.lift_line_fraction = lift_line_fraction
        inverted_lift_line_fraction = 1-lift_line_fraction
        self.x = chairlift.x1 * inverted_lift_line_fraction + chairlift.x2 * lift_line_fraction
        self.z = chairlift.z1 * inverted_lift_line_fraction + chairlift.z2 * lift_line_fraction
        
        self.real_y = chairlift.world.get_real_elevation(int(self.z), int(self.x))
        self.real_x = self.chairlift.world.grid_to_real(self.x)
        self.real_z = self.chairlift.world.grid_to_real(self.z)
        
        self.model,self.up_point,self.down_point = pole_design_1()
        horizontal_rotate_model_around_origin(self.model, self.angle)
        move_model(self.model, self.real_x, self.real_y, self.real_z)
        add_model_to_vertex_handler(self.model, self.chairlift.world.vertex_handler)
        
        horizontal_rotate_around_origin(self.up_point, self.angle)
        horizontal_rotate_around_origin(self.down_point, self.angle)
        move_point(self.up_point, self.real_x, self.real_y, self.real_z)
        move_point(self.down_point, self.real_x, self.real_y, self.real_z)
class Terminal:
    def __init__(self, chairlift, top_or_bot):
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
        
        
        self.real_y = chairlift.world.get_real_elevation(self.z, self.x)
        
        self.real_x = self.chairlift.world.grid_to_real(self.x)
        self.real_z = self.chairlift.world.grid_to_real(self.z)
        
        self.model,self.track = terminal_design_1(rope_speed=chairlift.rope_speed, terminal_speed=chairlift.terminal_speed)
        horizontal_rotate_model_around_origin(self.model, self.angle)
        move_model(self.model, self.real_x, self.real_y, self.real_z)
        add_model_to_vertex_handler(self.model, self.chairlift.world.vertex_handler)
        
        horizontal_rotate_track_around_origin(self.track, self.angle)
        move_track(self.track, self.real_x, self.real_y, self.real_z)

if __name__ == "__main__": main()
    
    
