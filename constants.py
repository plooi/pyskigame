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
    "faster_lift_speed" : 8,
    
    
    "fall_speed" : .7,#how fast do you have to go on a "steep" slope to have a chance of falling
    "ice_fall_speed" : .67,
    "fall_slope" : math.pi/4.75,#math.pi/6.2,#math.pi/5.5,#math.pi/4.75,
    "ice_slope" : (math.pi/3.6,math.pi/9),#(math.pi/5.5,math.pi/10),#(math.pi/5.5,math.pi/8.5),
    "no_ice_zone" : math.pi/1.3,
    "crash_speed" : .15,
    "ski_speed" : 1.1,#.55,
    "scroll_speed": math.pi/20000,#math.pi/40,
    "scroll_speed_lift" : math.pi/40,
    "turn_limit" : math.pi/20,
    "min_vr_margin" : math.pi/45,
    
    "swish_angle" : math.pi/20, 
    
    #when you jump, how much angle does the skier get boosted off from the ground
    "jump_angle" : math.pi/12,
    "jump_g" : .019,
    
    
    "friction" : .0065,#.009,#.018,#.0068,]
    "g_force" : .019,
    
    "ice_color" : Color(.84,.87,.9),
    "ice_radius" : 27,#scaled value
    
    
    "bump_slope" : (math.pi/4,math.pi/16),
    "bump_density" : .001,#.36,#.3,
    "bump_group_density" : .3,
    "bump_collision_radius" : 1.6,
    
    "menu_key" : "c",
    "interact_key" : "e",
    "find_key" : "x",
    "no_look_key" : "left",
    "scenery key" : "tab",
    "unweight_key" : "space",
    "action_key" : "space",
    "low_speed_stop_key" : "b",
    
    "scaled_distance_to_meters" : 1.4,
    
    "full_chair_model_distance" : 75,
    "blurry_chair_model_distance" : 180,
    "super_blurry_chair_model_distance" :330,
    
    "background_color" : Color(.7,.7,1),
    "tree_background_color" : Color(.9,.93,.9),#Color(0,.4,.0),
    "front_row_chunk_distance" : .8,#unit: chunks #these will be rendered separately after the depth buffer is cleared
    "max_los" : 6000,
    "min_los" : .5,
    
    
    "distance_before_the_shadow_reset_center_goes_straight_to_you" : 3,
    "max_number_of_spots_checked_for_shadow_add_per_step" : 300,
    
    
    "ray_tracing_memo_refresh_every_n_ticks" : 10,
    


}
