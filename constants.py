import math
from pylooiengine import *
x = {

    "detachable_rope_speed" : .375,#.3,
    "detachable_terminal_speed" : .02,
    "gondola_terminal_speed" : .01,
    "gondola_rope_speed" : .65,
    
    "fixed_grip_rope_speed" : .09,
    "ski_mode_walk_speed" : .075,
    
    "chair_ride_distance" : 1.5, #in terms of real distance. How far away you need to be from a chair in order to get on it
    "chair_sit_under_distance" : .5,
    "fall_speed" : .7,
    "ice_fall_speed" : .67,
    "fall_slope" : math.pi/4.75,
    "ice_slope" : (math.pi/5.5,math.pi/8.5),
    "no_ice_zone" : math.pi/3,
    "crash_speed" : .15,
    
    "ice_color" : Color(.84,.87,.9),
    "ice_radius" : 27#scaled value
    


}


