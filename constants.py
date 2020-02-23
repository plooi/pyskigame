import math
from pylooiengine import *
x = {

    "detachable_rope_speed" : .585,#.375,#.3,
    "detachable_terminal_speed" : .025,
    "gondola_terminal_speed" : .01,
    "gondola_rope_speed" : .7,
    
    "fixed_grip_rope_speed" : .275,
    "fixed_grip_terminal_speed" : .274999,
    "ski_mode_walk_speed" : .17,#.075,
    
    "chair_ride_distance" : 1.5, #in terms of real distance. How far away you need to be from a chair in order to get on it
    "midpoint_hop_distance" : 3.5,
    "midpoint_hop_cooldown" : 240,
    "chair_sit_under_distance" : .5,
    "fall_speed" : .7,#how fast do you have to go on a "steep" slope to have a chance of falling
    "ice_fall_speed" : .67,
    "fall_slope" : math.pi/6.2,#math.pi/5.5,#math.pi/4.75,
    "ice_slope" : (math.pi/5.5,math.pi/7.5),#(math.pi/5.5,math.pi/10),#(math.pi/5.5,math.pi/8.5),
    "no_ice_zone" : math.pi/3,
    "crash_speed" : .15,
    
    "ice_color" : Color(.84,.87,.9),
    "ice_radius" : 27,#scaled value
    
    
    "bump_slope" : (math.pi/4.6,math.pi/10),
    "bump_density" : .3,
    "bump_group_density" : .2,
    
    "move_key" : "w",
    "menu_key" : "c",
    "interact_key" : "e",
    "find_key" : "x",
    "no_look_key" : "q",
    "scenery key" : "tab",
    
    "scaled_distance_to_meters" : 1.4,
    
    
    
    
    


}
