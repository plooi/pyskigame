from pylooiengine import *
import util
from util import get_angle
from model_3d import *
import math
def main():
    l = Lift(None)
    l.add_point(Point(0,0,0,1))
    l.add_point(Point(1,0,0,1))
    l.update()
    print(l.travel(3))
class Lift(LooiObject):
    def __init__(self, world):
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
        
        self.track = Track()
        
    """
    [startZ, startX, [array of pole percentage values, negatives mean midpoints], endZ, endX]
    [z1, x1, [.1, .2, .3, .4, .5, .6, -.7, .8], z2, x2]
    """
    def build(self, chairlift_array):
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
    def travel(self, time):
        for segment in self.track:
            time_duration = segment.get_time_duration()
            print("time duration: " + str(time_duration))
            if time > time_duration:
                time -= time_duration
                continue
            else:
                return (segment.travel(time), segment.horizontal_angle())
        else:
            raise TimeOverflowException(time)
    def add_point(self, point, index=None):
        self.track.add_point(point, index = index)
    def update(self):
        self.track.generate_segments()

class Track:
    def __init__(self):
        self.points = []
        self.segments = []
    def add_point(self, point, index=None):
        if index == None:
            index = len(self.points)
        self.points.insert(index, point)
    def generate_segments(self):
        self.segments = []
        for i in range(len(self.points)):
            self.segments.append(Segment  (self.points[i], self.points[circular_add(i, 1, len(self.points))])  )
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
def circular_add(a, b, max):
    ret = a+b
    while ret >= max:
        ret -= max
    return ret

def terminal_design_1():
    pole_length = 1
    pole_width = .6
    pole_height = 3
    pole_color_array = [.3,.3,.3]
    
    terminal_roof_width = 4
    terminal_roof_length = 7
    terminal_belly_color = [.7,.7,.7]
    
    ret = [
    [-pole_width/2,0,-pole_length/2], [pole_width/2,0,-pole_length/2], [pole_width/2,0,pole_length/2], [-pole_width/2,0,pole_length/2], pole_color_array,#base
    
    [-pole_width/2,0,-pole_length/2], [pole_width/2,0,-pole_length/2], [pole_width/2,pole_height,-pole_length/2], [-pole_width/2,pole_height,-pole_length/2], pole_color_array,
    [pole_width/2,0,-pole_length/2], [pole_width/2,0,pole_length/2], [pole_width/2,pole_height,pole_length/2], [pole_width/2,pole_height,-pole_length/2], pole_color_array,
    [pole_width/2,0,pole_length/2], [-pole_width/2,0,pole_length/2], [-pole_width/2,pole_height,pole_length/2], [pole_width/2,pole_height,pole_length/2], pole_color_array,
    [-pole_width/2,0,pole_length/2], [-pole_width/2,0,-pole_length/2], [-pole_width/2,pole_height,-pole_length/2], [-pole_width/2,pole_height,pole_length/2], pole_color_array,
    
    [-terminal_roof_width/2, pole_height, -terminal_roof_length],[terminal_roof_width/2, pole_height, -terminal_roof_length],[terminal_roof_width/2, pole_height, terminal_roof_length], [-terminal_roof_width/2, pole_height, terminal_roof_length], terminal_belly_color
    ]
    horizontal_rotate_model_around_origin(ret, -math.pi/2)

    return ret, Track()

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
    [-p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,-t_width/2], [p_2,pole_height+t_height,t_width/2], [-p_2,pole_height+t_height,t_width/2], t_color
    
    ],[]
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
        
        self.model,self.track = copy_model(pole_design_1())
        horizontal_rotate_model_around_origin(self.model, self.angle)
        move_model(self.model, self.real_x, self.real_y, self.real_z)
        add_model_to_vertex_handler(self.model, self.chairlift.world.vertex_handler)
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
        
        self.model,self.track = copy_model(terminal_design_1())
        horizontal_rotate_model_around_origin(self.model, self.angle)
        move_model(self.model, self.real_x, self.real_y, self.real_z)
        add_model_to_vertex_handler(self.model, self.chairlift.world.vertex_handler)
        
        
            
if __name__ == "__main__": main()
    
    
