from pylooiengine import *
#from player import *
from pylooiengine.misc.graphics import VertexHandler
import math
import pylooiengine
import easygui
import rooms
import normal
from random import random

import numpy
import copy
from tree import *
from game_ui import UI
import loading
import PySimpleGUI as sg
from rock import Rock
from models import *
import util
import model_3d
from OpenGL.GL import *
from OpenGL.GLU import *
from constants import x as constants
from bump import Bump
from world_object import WorldObject

import texture
import world_operations
from PIL import Image
from time import time
from lift import Pole


#improves performance. 
def conv_155_255(x):
    if x > 1 or x < 0: raise Exception()
    x = int(x*63)*4+3
    if x < 155:
        x = 155
    if x >= 255:
        x = 251#just please don't return the white square
    return x
    
    
"""
def conv_155_255(x):
    if x > 1 or x < 0: raise Exception()
    lighting = x * 255
    def abs(x): return x if x >= 0 else -x
    closest = None
    closest_distance = 999999
    for key in arr_155_255:
        distance = abs(key-lighting)
        if distance < closest_distance:
            closest = key
            closest_distance = distance
    
    return closest
"""


arr_55_255 = [x for x in range(55, 255, 5)]
arr_55_255.reverse()

def conv_55_255(x):
    if x > 1 or x < 0: raise Exception()
    lighting = x * 255
    def abs(x): return x if x >= 0 else -x
    closest = None
    closest_distance = 999999
    for key in arr_55_255:
        distance = abs(key-lighting)
        if distance < closest_distance:
            closest = key
            closest_distance = distance
    
    return closest

ice_textures = {}
ice_textures_keys = []
"""
for blend in range(1):
    ice_textures[blend] = {}
    for target in range(55, 255, 5):
        ice_textures[blend][target] = image("./3d_textures/IceTexture-lighting-"+str(target)+"_"*blend+".png")
        if target not in ice_textures_keys:
            ice_textures_keys.append(target)
            

ice_textures_keys.reverse()
"""
    
def get_ice_texture(lighting):
    lighting = lighting * 255
    def abs(x): return x if x >= 0 else -x
    closest = None
    closest_distance = 999999
    for key in ice_textures_keys:
        distance = abs(key-lighting)
        if distance < closest_distance:
            closest = key
            closest_distance = distance
    
    return ice_textures[0][closest]



#TESTING PURPOSES ONLY FPS
class FPS(LooiObject):
    def __init__(self, v):
        super().__init__()
        self.frames = 0
        self.seconds = 0
        self.fps = 0
        self.v = v
    def step(self):
        if int(time()) > (self.seconds):
            self.seconds = int(time())
            self.fps = self.frames
            self.frames = 0
        self.frames += 1
        
    def paint(self):
        pass
        #

class View:
    def __init__(self):
        self.x = -10
        self.y = 10
        self.z = -10
        self.hor_rot = -math.pi/4
        self.vert_rot = 0
        self.speed = 4
        self.rot_spd = .001
        self.line_of_sight = 3 #IN NUMBER OF CHUNKS (not opengl space) #the radius
        self.max_vert_rot = math.pi/2.3
        

        
class Quad:
    def __init__(self):
        self.my_chunk_x = -1#keeps track of which chunk we're in
        self.my_chunk_z = -1#keeps track of which chunk we're in
        
        self.floor_pointer = -1#keeps track of the position of the floor quad in the chunk vertex handler
        
        self.containedObjects = []#keeps track of all 3d objects that are related to this quadrilateral (like trees)
class Chunk:
    def __init__(self, world):
        self.vh = VertexHandler(3)#vertex handler to store all non-moving drawables in this chunk
        self.tvh = texture.new_texture_handler(initial_capacity=world.properties["chunk_size"]**2+1)
        
        
        #is this even used???
        self.pan_chunk_square_pointers = None #list of pointers to the locations of the pan chunk squares in the "vertex buffer" (None if not added)
        
        
        self.world = world
        
        self.colors_changed = True
        self.pan_chunk_squares = None
    
            
    """
    get_pan_chunk_square
    
    Uses the quads grid to find out what the dimensions and color of the pan chunk 
    square are. Generates a new return value on each call
    
    returns ([x1,y1,z1], [x2,y2,z2], [x3,y3,z3], [x4,y4,z4], [r,g,b]) representing
    the pan chunk square. 
    
    
    """
    def get_pan_chunk_squares(self, chunk_z, chunk_x, trees=True):
        sub_chunks=self.world.properties["sub_chunk_squares"]
        
        cs = self.world.properties["chunk_size"]
        ul_z = chunk_z * cs
        ul_x = chunk_x * cs
        s = self.world.properties["horizontal_stretch"]
        
        if self.colors_changed or not isinstance(self.pan_chunk_squares, dict):
            
        
        
            self.colors_changed=False
            side_length_in_sub_chunks = int(sub_chunks**.5)#how many sub chunks does this chunk have in each row?
            sub_chunk_side_length = int(cs/side_length_in_sub_chunks)#how many floors does each sub chunk have on each row?
            self.pan_chunk_squares = {"trees":VertexHandler(3,initial_capacity=50), "without" : VertexHandler(3,initial_capacity=25)}
            
            #for each sub chunk within this chunk
            #print("making",side_length_in_sub_chunks**2,"sub chunk squares")
            for scr in range(side_length_in_sub_chunks):
                for scc in range(side_length_in_sub_chunks):
                    start_z = int(ul_z + scr*sub_chunk_side_length - sub_chunk_side_length/2)
                    start_x = int(ul_x + scc*sub_chunk_side_length - sub_chunk_side_length/2)
                    
                    
                    
                    
                    #doing the gradient
                    #we start with a shifted start_z and x  (- sub_chunk_side_length/2) so that we can 
                    #calculate the gradients of the squares perfectly around each of the four corners
                    #here, we are calculating each of the surrounding points' elevations
                    """
                    1 2 3
                    4 5 6
                    7 8 9
                    
                    """
                    
                    _1 = [start_x*s, self.world.get_elevation(start_z, start_x, scaled=True), start_z*s]
                    _2 = [(start_x+sub_chunk_side_length)*s, self.world.get_elevation(start_z, start_x+sub_chunk_side_length, scaled=True), start_z*s]
                    _4 = [(start_x)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x, scaled=True), (start_z+sub_chunk_side_length)*s]
                    _5 = [(start_x+sub_chunk_side_length)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x+sub_chunk_side_length, scaled=True), (start_z+sub_chunk_side_length)*s]
                    
                    
                    try:
                        _3 = [(start_x+2*sub_chunk_side_length)*s, self.world.get_elevation(start_z, start_x+2*sub_chunk_side_length, scaled=True), start_z*s]
                    except:
                        _3 = [(start_x+2*sub_chunk_side_length)*s, self.world.get_elevation(start_z, start_x+sub_chunk_side_length, scaled=True), start_z*s]
                    try:
                        _6 = [(start_x+2*sub_chunk_side_length)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x+2*sub_chunk_side_length, scaled=True), (start_z+sub_chunk_side_length)*s]
                    except:
                        _6 = [(start_x+2*sub_chunk_side_length)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x+sub_chunk_side_length, scaled=True), (start_z+sub_chunk_side_length)*s]
                    try:
                        _7 = [(start_x)*s, self.world.get_elevation(start_z+2*sub_chunk_side_length, start_x, scaled=True), (start_z+2*sub_chunk_side_length)*s]
                    except:
                        _7 = [(start_x)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x, scaled=True), (start_z+2*sub_chunk_side_length)*s]
                    try:
                        _8 = [(start_x+sub_chunk_side_length)*s, self.world.get_elevation(start_z+2*sub_chunk_side_length, start_x+sub_chunk_side_length, scaled=True), (start_z+2*sub_chunk_side_length)*s]
                    except:
                        _8 = [(start_x+sub_chunk_side_length)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x+sub_chunk_side_length, scaled=True), (start_z+2*sub_chunk_side_length)*s]
                    try:
                        _9 = [(start_x+2*sub_chunk_side_length)*s, self.world.get_elevation(start_z+2*sub_chunk_side_length, start_x+2*sub_chunk_side_length, scaled=True), (start_z+2*sub_chunk_side_length)*s]
                    except:
                        _9 = [(start_x+2*sub_chunk_side_length)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x+sub_chunk_side_length, scaled=True), (start_z+2*sub_chunk_side_length)*s]
                    
                    
                    
                    
                    
                    
                    
                    def find_color(ul, ur, lr):
                        #find hr and vr or the floor so we can use that to calculate the color
                        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ur[0],ur[1],ur[2],lr[0],lr[1],lr[2])
                        if vr < 0:
                            vr = -vr
                            hr = hr + math.pi
                            
                        ret = self.world.calculate_floor_color(hr, vr)
                        ret[2]*=1.065
                        if ret[2] > 1: ret[2] = 1#make it blue
                        return ret
                    
                    
                    
                    #here, we are finding the colors of the four corners
                    color1254 = find_color(_1, _2, _4)
                    color2365 = find_color(_2, _3, _5)
                    color4587 = find_color(_4, _5, _7)
                    color5689 = find_color(_5, _6, _8)
                    
                    
                    
                    start_z = ul_z + scr*sub_chunk_side_length
                    start_x = ul_x + scc*sub_chunk_side_length
                    #we want start z and x to be at the top left of the chunk now
                    
                    
                    #here, we are adding objects to the pan chunk square
                    for r in range(start_z, start_z + sub_chunk_side_length):
                        for c in range(start_x, start_x + sub_chunk_side_length):
                            
                            for obj in self.world.quads[r][c].containedObjects:
                                if obj.__class__ == Tree:
                                    
                                    #with trees pan chunk squares
                                    real_x = (c+.5)*self.world.properties["horizontal_stretch"]
                                    real_z = (r+.5)*self.world.properties["horizontal_stretch"]
                                    real_y = self.world.get_elevation_continuous(r+.5, c+.5)*self.world.properties["vertical_stretch"]
                                    
                                    base = -5
                                    wid = 3
                                    
                                    hei = 14
                                    brightness = self.world.get_proper_floor_color(r, c)[0]
                                    B = brightness**2
                                    if B < .35:B = .35
                                    #tree_color = [brightness*.45,brightness*.7,brightness*.3]
                                    tree_color = [B*.3,B*.6,B*.08]
                                    
                                    
                                    self.pan_chunk_squares["trees"].add_vertex([real_x-wid,real_y+base,real_z], tree_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+wid*.7,real_y+base,real_z+wid*.7], tree_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+wid*.7,real_y+base,real_z-wid*.7], tree_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x,real_y+hei,real_z], tree_color)
                                if obj.__class__ == Pole:
                                    
                                    real_x = obj.real_x
                                    real_z = obj.real_z
                                    real_y = obj.real_y
                                    
                                    base = -999999
                                    wid = .3
                                    
                                    hei = 10
                                    brightness = self.world.get_proper_floor_color(r, c)[0]
                                    pole_color = [.15,.15,.15]
                                    
                                    t_color = [.7,.7,.7]
                                    t_wid = 1.3
                                    t_h = .8
                                    
                                    
                                    self.pan_chunk_squares["trees"].add_vertex([real_x-wid,real_y+hei,real_z], pole_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+wid*.7,real_y+hei,real_z+wid*.7], pole_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+wid*.7,real_y+hei,real_z-wid*.7], pole_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x,real_y+base,real_z], pole_color)
                                    
                                    
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+t_wid*math.cos(obj.angle+math.pi/2),real_y+hei,real_z-t_wid*math.sin(obj.angle+math.pi/2)], t_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+t_wid*math.cos(obj.angle+math.pi/2),real_y+hei+t_h,real_z-t_wid*math.sin(obj.angle+math.pi/2)], t_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+t_wid*math.cos(obj.angle-math.pi/2),real_y+hei+t_h,real_z-t_wid*math.sin(obj.angle-math.pi/2)], t_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+t_wid*math.cos(obj.angle-math.pi/2),real_y+hei,real_z-t_wid*math.sin(obj.angle-math.pi/2)], t_color)
                                    
                                    
                    
                    
                    #now, we want the actual locations of the four corners
                    _1 = [start_x*s, self.world.get_elevation(start_z, start_x, scaled=True), start_z*s]
                    _2 = [(start_x+sub_chunk_side_length)*s, self.world.get_elevation(start_z, start_x+sub_chunk_side_length, scaled=True), start_z*s]
                    _4 = [(start_x)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x, scaled=True), (start_z+sub_chunk_side_length)*s]
                    _5 = [(start_x+sub_chunk_side_length)*s, self.world.get_elevation(start_z+sub_chunk_side_length, start_x+sub_chunk_side_length, scaled=True), (start_z+sub_chunk_side_length)*s]
                    
                    
                    
                    
                    
                    
                    ul = _1
                    ur = _2
                    lr = _5
                    ll = _4
                    
                    
                    
                    
                    #now, we add everything to the vertex handler
                    
                    
                    #without trees
                    self.pan_chunk_squares["without"].add_vertex(ul,color1254)
                    self.pan_chunk_squares["without"].add_vertex(ur,color2365)
                    self.pan_chunk_squares["without"].add_vertex(lr,color5689)
                    self.pan_chunk_squares["without"].add_vertex(ll,color4587)
                    
                    #with trees
                    self.pan_chunk_squares["trees"].add_vertex(ul,color1254)
                    self.pan_chunk_squares["trees"].add_vertex(ur,color2365)
                    self.pan_chunk_squares["trees"].add_vertex(lr,color5689)
                    self.pan_chunk_squares["trees"].add_vertex(ll,color4587)
                    
                    
                    #add the sky coverup squares
                    def cmd(point):#short for copy move down. Takes a point (list x,y,z) and copies it and moves it down the y axis a specific amount
                        ret = list(point)
                        ret[1] -= 100
                        return ret
                    p = self.pan_chunk_squares["trees"]
                    def sky_cover_square(point1, point2):#points 3 and 4 are same as point 1,2 but moved down
                        if point1 is ul:color1 = color1254
                        if point1 is ur:color1 = color2365
                        if point1 is lr:color1 = color5689
                        if point1 is ll:color1 = color4587
                        if point2 is ul:color2 = color1254
                        if point2 is ur:color2 = color2365
                        if point2 is lr:color2 = color5689
                        if point2 is ll:color2 = color4587
                        p.add_vertex(point1, color1)
                        p.add_vertex(point2, color2)
                        p.add_vertex(cmd(point2), color2)
                        p.add_vertex(cmd(point1), color1)
                    if scr == 0 and scc == 0:#we are at the upper left of the chunk
                        sky_cover_square(ul,ll)
                        sky_cover_square(ul,ur)
                    elif scr == side_length_in_sub_chunks-1 and scc == side_length_in_sub_chunks-1:#we are at the lower right of chunk
                        sky_cover_square(lr,ur)
                        sky_cover_square(lr,ll)
                    elif scr == 0 and scc == side_length_in_sub_chunks-1:#upper right of chunk
                        sky_cover_square(ur,ul)
                        sky_cover_square(ur,lr)
                    elif scr == side_length_in_sub_chunks-1 and scc == 0:#lower left
                        sky_cover_square(ll,ul)
                        sky_cover_square(ll,lr)
                    elif scr == 0:#top side
                        sky_cover_square(ur, ul)
                    elif scr == side_length_in_sub_chunks-1:#bottom side
                        sky_cover_square(lr, ll)
                    elif scc == 0:#left side
                        sky_cover_square(ul, ll)
                    elif scc == side_length_in_sub_chunks-1:#right side
                        sky_cover_square(ur, lr)
                    
                    
                    
        
        #print("pcs",self.pan_chunk_squares.vertices,"colors",self.pan_chunk_squares.vertex_colors)
        if trees:
            return self.pan_chunk_squares["trees"]
        else:
            return self.pan_chunk_squares["without"]
        
        
class World(LooiObject):
    
###################################
#INIT STUFF
###################################
    """
    __init__ 
    
    really the purpose is to just allocate the memory and do some
    basic initialization
    """
    def __init__(self):
        super().__init__(active=False)
        
        
        #just a dictionary that stores all properties of this world
        self.properties = {
            "name" : "unnamed",
            #"chunk_size" : 8,
            "chunk_size" : 32,
            "sub_chunk_squares" : 16,
            "width" : -1,
            "height" : -1,
            "width_chunks" : -1,
            "height_chunks" : -1,
            "line_of_sight2" : 8,#how many chunks away before the trees start to disappear
            "horizontal_stretch" : 4,
            "vertical_stretch" : .15,
            "sun_angle" : 0,
            
            "texture_distance" : 4, #distance at which we start drawing the snow texture in quads not chunks
            "texture_radius" : 3, #distance at which floors are guaranteed to be textured, regardless of whether you're looking or not
            "active_missions" : [],#missions are lists of two values [(landmark_z,landmark_x), type]
            #landmark is obviously the landmark that this mission requires us to go to
            #type is the type of mission. 1=explore mission, 2=fix the lift mission, 3=save the buddy mission
            "completed_missions" : [],#does not include fix the lift missions, only landmark missions
            
            
            #the settings below have nothing to do with the world itself,
            #they're just in here because it's more efficient to put them all together
            "line_thickness(map_editor)" : 5, #in unscaled distance
            "terrain_mod_step_size(map_editor)" : 15, #in unscaled height
            "chair_time_distance_detachable" : 210,#in terms of ticks
            "chair_time_distance_gondola" : 300,#in terms of ticks
            "chair_time_distance_fixed" : 300, #in terms of ticks
            "build_chair_pole_distance(map_editor)" : 85, #in real distance
            "bump_placement_chance(map_editor)" : 1, #0-1
            
            
            #the settings below are just for ski mode
            
            "x_momentum" : 0,
            "y_momentum" : 0,
            "z_momentum" : 0,
            "player_height" : 1.5,
            "ski_direction" : 0,
            "momentum" : 0,
            "momentum_direction" : 0,
            "ski_model" : "Red Basic",
            "do_floor_textures" : True,
            "jerk" : 0,
            "health" : 100,
            
            
            
            
            }
            
        self.set_layer(-1999999) #because the front layer will be drawn first. So 
        #then so the world draws first, and then I can clear the bit buffer and then let the other stuff draw
        
        
        #2D Array where each element denotes one quadrilateral
        self.quads = []
        
        #2D Array where each element denotes one chunk
        self.chunks = []
        
        #stores all the pan chunk squares
        self.pan_chunk_squares = VertexHandler(3)
        
        
        #keep track of the view position
        self.view = View()
        
        
    
        self.mobile_vertices = None
        self.mobile_colors = None
        
        
        #this keeps track of how to save and load the world next time
        #keys are the IDs (id function) of objects such as trees and
        #lifts, values are strings which contain python code describing
        #how to recreate that object
        #self.object_account = {}
        
        self.landmarks = []
        
        self.game_ui = None
        
        
        
        
    
    """
    init_csv
    """
    
    def init_csv(self, name, csv_name, more_properties={}, view=None):
        lines = []
        f = open(csv_name, "r")
        for line in f:
            lines.append([(0 if x.strip()=="None" else float(x)) for x in line.split(",")])
        f.close()
        
        height = len(lines)
        width = 0 if height==0 else len(lines[0])
        return self.init(name, width-1, height-1, more_properties, lambda z,x: lines[z][x], view) 
    
    """
    init 
    
    call this one time to initialize the world
    
    finds the number of chunks in the z and x directions
    then adds new chunk rows and cols until height and width are matching
    
    
    finds the actual height and width in number of quadrilaterals (cuz we can't have half a chunk, so we round up to the nearest chunk)
    then adds new quadrilateral rows and cols until height and width are matching
        tells each quadrilateral which chunk it's in
        allocates a spot in the current chunk's buffer for the floor square, and hands that pointer over to the quadrilateral
    """
    def init(self, name, width, height, more_properties={}, elevation_function=lambda z,x:0, view=None, prog_bar=True):
        self.quads = []
        self.chunks = []
        self.pan_chunk_squares = VertexHandler(3)
    
    
        if prog_bar: loading.progress_bar("Loading 1/2")
        
        
        #set properties properly
        for property in more_properties:
            self.properties[property] = more_properties[property]
        self.properties["name"] = name
        self.properties["width_chunks"] = int(width/self.properties["chunk_size"])
        self.properties["height_chunks"] = int(height/self.properties["chunk_size"])
        self.properties["width"] = self.properties["width_chunks"]*self.properties["chunk_size"]
        self.properties["height"] = self.properties["height_chunks"]*self.properties["chunk_size"]
        if view != None: self.view = view
        
        """
        mobile drawables are stored in these arrays
        
        "mobile" refers to, it can move. So once this paint iteration completes and all the
        mobile vertices are drawn with their corresponding colors, all the mobile vertices
        are DELETED, so that on the next iteration you can add the vertices and colors in
        again, but if they've changed that's okay cuz that's why we add fresh ones every time
        
        However, don't make everything a mobile vertex because mobile vertices are slower than static ones
        """
        self.mobile_vertices = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        
        #initialize all chunks
        for z in range(self.properties["height_chunks"]):
            row = []
            for x in range(self.properties["width_chunks"]):
                c = Chunk(self)
                
                row.append(c)
            self.chunks.append(row)
            
        
        
        
        
        vs = self.properties["vertical_stretch"]
        
        elevation_function_orig = elevation_function
        elevation_function = lambda z,x: elevation_function_orig(z,x)*vs
        
        t1 = time()
        
        
        
        #initialize quads 
        for z in range(self.properties["height"]):
            row = []
            self.quads.append(row)
            for x in range(self.properties["width"]):
                #actually create the quad object
                row.append(Quad())#add the quad object to the self.quads
        
        #fill the quads with data
        for z in range(self.properties["height"]):
            for x in range(self.properties["width"]):
                z_chunk, x_chunk = self.convert_to_chunk_coords(z, x)#find which chunk this quad z,x is in
                
                q=self.quads[z][x]
                q.my_chunk_z = z_chunk#set properly which chunk it belongs to
                q.my_chunk_x = x_chunk
                
                tvh = self.chunks[z_chunk][x_chunk].tvh
                
                hs = self.properties["horizontal_stretch"]
                
                #allocate memory for the quad that is going to be drawn and
                #set all the elevations to what the elevation function wants
                q.floor_pointer = tvh.add_vertex([x*hs,elevation_function(z,x),z*hs])
                tvh.add_vertex([(x+1)*hs,elevation_function(z, x+1),z*hs])
                tvh.add_vertex([(x+1)*hs,elevation_function(z+1, x+1),(z+1)*hs])
                tvh.add_vertex([x*hs,elevation_function(z+1, x),(z+1)*hs])
                
            if prog_bar and z % 7 == 0: loading.update(z/self.properties["height"]*50)
        #reset floor textures
        #by the way, having this as it's own loop increased performance by 15%
        for z in range(self.properties["height"]):
            for x in range(self.properties["width"]):
                self.reset_floor_texture(z, x)
            if prog_bar and z % 7 == 0: loading.update(z/self.properties["height"]*50+50)
            
        #print("loading 1/3 took",time() - t1)
        
        """
        do not worry about allocating all the pan chunk squares
        they will be allocated during the step function
        """
                
        
        
        
        #other stuff
        self.fps = FPS(0)
        self.add(self.fps)
        
        
        
        
        #initialize the natural bumps
        if prog_bar: loading.update(100)
        world_operations.natural_bumps(self, 0,0,self.get_width_points(), self.get_width_points(), prog_bar=True)
        
        
        return self
        #END INIT
        
    #setup for front row things
    def get_setup_3d_close(self):
        
        def setup_3d():
            if self.game_ui.game_mode == "map editor":
                gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), 5, constants["max_los"])
            else:
                gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), constants["min_los"], constants["max_los"])
            
            try:
                glRotate(rad_to_deg(-(self.view.hor_rot-math.pi/2)), 0, 1, 0)
                glRotate(rad_to_deg(-self.view.vert_rot), math.cos(self.view.hor_rot - math.pi/2), 0, -math.sin(self.view.hor_rot - math.pi/2))
                glTranslate(-self.view.x, -self.view.y, -self.view.z)
            except Exception as e:
                pass
        return setup_3d
    def get_setup_3d_far(self):
        def setup_3d():
            gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), (constants["front_row_chunk_distance"]-.5)*self.properties["chunk_size"]*self.properties["horizontal_stretch"], constants["max_los"] )
            try:
                glRotate(rad_to_deg(-(self.view.hor_rot-math.pi/2)), 0, 1, 0)
                glRotate(rad_to_deg(-self.view.vert_rot), math.cos(self.view.hor_rot - math.pi/2), 0, -math.sin(self.view.hor_rot - math.pi/2))
                glTranslate(-self.view.x, -self.view.y, -self.view.z)
            except Exception as e:
                pass
        return setup_3d
    
        
###################################
#END init stuff
###################################



###################################
#ELEVATIONS
###################################
    """
    get_elevation
    
    finds the UNSCALED elevation of the POINT z, x that you input
        must unscale the elevation
    """
    def get_elevation(self, z, x, scaled=False):
        if z < self.get_height_floors() and x < self.get_width_floors():#is the point we're looking for NOT on the last row or col?
            #then we can just find the corresponding floor z, x and get it's upper left hand corner 
            chunk_z, chunk_x = self.convert_to_chunk_coords(z, x)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z][x].floor_pointer
            point = chunk_obj.tvh.vertices[floor_pointer+0]#+0 for upper left
            return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
        else:# we are either on the last row, or the last column, or both
            #so we will have to access other corners and be smart about it
            if x == 0:#then we are on the last row, first (0th) column
                #so ill just go to that floor and get the lower left point
                chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z-1][x].floor_pointer
                point = chunk_obj.tvh.vertices[floor_pointer+3]#+0 for lower left
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]
            elif z == 0:#then we are on the last column, first (0th) row
                #so ill just go to that floor and get the upper right point
                chunk_z, chunk_x = self.convert_to_chunk_coords(z, x-1)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z][x-1].floor_pointer
                point = chunk_obj.tvh.vertices[floor_pointer+1]#+1 for upper right
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]
            else:#then we can just go to the corresponding floor z-1,x-1 and get it's lower right corner
                chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x-1)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z-1][x-1].floor_pointer
                point = chunk_obj.tvh.vertices[floor_pointer+2]#+1 for lower right
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]
                
    #input unscaled position
    #output unscaled elevation
    def get_elevation_continuous(self, z, x):
        
        
        
        if not self.valid_floor(int(z), int(x)):
            return -9999
        
        
        #determine if we're in the upper left triangle, 
        #or the upper right triangle
        fracz = z % 1
        fracx = x % 1
        if fracz+fracx < 1:
            #upper left triangle
            ul = int(x), self.get_elevation(int(z),int(x)), int(z)
            ur = int(x)+1, self.get_elevation(int(z),int(x)+1), int(z)
            ll = int(x), self.get_elevation(int(z)+1,int(x)), int(z)+1
            xrise = ur[1] - ul[1]
            zrise = ll[1] - ul[1]
            
            y = fracx*xrise + fracz*zrise + ul[1]
            
        else:
            #upper right triangle
            lr = int(x)+1, self.get_elevation(int(z)+1,int(x)+1), int(z)+1
            ur = int(x)+1, self.get_elevation(int(z),int(x)+1), int(z)
            ll = int(x), self.get_elevation(int(z)+1,int(x)), int(z)+1
            
            
            xrise = ll[1] - lr[1]
            zrise = ur[1] - lr[1]
            
            y = (1-fracx)*xrise + (1-fracz)*zrise + lr[1]
        #print(ll,ur)
        return y
    """
    set_elevation
    
    void set_elevation(z, x, unscaled_elevation, reset_color?)
        goes to the quadrilateral array and finds the four (or fewer) quadrilaterals that are touching 
            this point
        using the information inside each quadrilateral,
            finds out which indexes inside which chunk's numpy buffer need to be modified
        scales the elevation
        gives the elevation to the right chunks at the right indexes
        
        recolor if requested
    
    
    UNTESTED
    """
    def set_elevation(self, z, x, elevation, reset_color=True, delete_trees=False):
        #print("set")
        elevation *= self.properties["vertical_stretch"]
        
        #upper left floor
        if self.valid_floor(z-1, x-1):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x-1)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z-1][x-1].floor_pointer
            point = chunk_obj.tvh.vertices[floor_pointer+2]#+2 for upper left floor's LOWER RIGHT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z-1,x-1)
                
            if delete_trees:
                i=0
                while i < len(self.quads[z-1][x-1].containedObjects):
                    obj = self.quads[z-1][x-1].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
            
        #upper right floor
        if self.valid_floor(z-1, x):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z-1][x].floor_pointer
            point = chunk_obj.tvh.vertices[floor_pointer+3]#+3 for upper right floor's LOWER LEFT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z-1,x)
            if delete_trees:
                i=0
                while i < len(self.quads[z-1][x].containedObjects):
                    obj = self.quads[z-1][x].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
            
        #lower right floor
        if self.valid_floor(z, x):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z, x)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z][x].floor_pointer
            point = chunk_obj.tvh.vertices[floor_pointer+0]#+0 for lower right floor's UPPER LEFT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z,x)
            if delete_trees:
                i=0
                while i < len(self.quads[z][x].containedObjects):
                    obj = self.quads[z][x].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
            
        #lower left floor
        if self.valid_floor(z, x-1):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z, x-1)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z][x-1].floor_pointer
            point = chunk_obj.tvh.vertices[floor_pointer+1]#+1 for upper left floor's UPPER RIGHT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z,x-1)
            if delete_trees:
                i=0
                while i < len(self.quads[z][x-1].containedObjects):
                    obj = self.quads[z][x-1].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
                        
    def get_rotation(self, floor_z, floor_x):
    
        #find the floor object and the chunk object
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        
        #find the coordinates of all the 
        ul = chunk.tvh.vertices[floor.floor_pointer]
        ur = chunk.tvh.vertices[floor.floor_pointer+1]
        lr = chunk.tvh.vertices[floor.floor_pointer+2]
        ll = chunk.tvh.vertices[floor.floor_pointer+3]
        
        #find hr and vr or the floor so we can use that to calculate the color
        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ur[0],ur[1],ur[2],lr[0],lr[1],lr[2])
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        return hr,vr
    
            
            
    
                
###################################
#END elevations
###################################


###################################
#BASIC GETTERS SETTERS
###################################
    def get_width_floors(self): return self.properties["width"]
    def get_height_floors(self): return self.properties["height"]
    def get_width_chunks(self): return self.properties["width_chunks"]
    def get_height_chunks(self): return self.properties["height_chunks"]
    def get_width_points(self): return self.get_width_floors()+1
    def get_height_points(self): return self.get_height_floors()+1
        
    
###################################
#END basic getters setters
###################################
    
    
###################################
#CHECKS
###################################
    def valid_point(self, z, x): return z < self.get_height_points() and x < self.get_width_points() and z >= 0 and x >= 0
    def valid_floor(self, z, x): return z < self.get_height_floors() and x < self.get_width_floors() and z >= 0 and x >= 0
    def valid_chunk(self, z, x): return z < self.get_height_chunks() and x < self.get_width_chunks() and z >= 0 and x >= 0
    
    
    
    #los in chunks
    def in_los(self, z, x, scaled=False, los=None):
        if los == None: los = self.view.line_of_sight
        if not scaled:
            z *= self.properties["horizontal_stretch"]
            x *= self.properties["horizontal_stretch"]
        return ( (z - self.view.z)**2 + (x - self.view.x)**2 ) ** .5 <= los*self.properties["chunk_size"]*self.properties["horizontal_stretch"]
    
    #input real/scaled distance
    def is_close(self, z, x, dist):
        return ( (z - self.view.z)**2 + (x - self.view.x)**2 ) ** .5 <= dist
###################################
#END checks
###################################


###################################
#FLOOR COLOR
###################################
    """
    get_floor_color
    
    finds the floor, and gives you its color
    """
    def get_floor_color(self, floor_z, floor_x):
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        raise Exception("This needs to be redone to consider textures")
        return chunk.vh.vertex_colors[floor.floor_pointer]
    
    
    
    """
    set_floor_color
    
    finds the floor that we're dealing with
    goes to the floor pointer in the floor's chunk's vertexhandler and sets the color
    """
    def set_floor_texture(self, floor_z, floor_x, texture_str, is_snow_texture=True):
        check(self.valid_floor(floor_z, floor_x))
        
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        texture.set_texture(chunk.tvh, floor.floor_pointer, texture_str)#THIS is where you make the special function to pick only as many pixels as the horizontal stretch allows. Start with 32X32 image, then select from that. pixels = 2 * hs
        if is_snow_texture:
            pixels = self.properties["horizontal_stretch"] * 2
            if pixels < 1: pixels = 1
            if pixels > 32: pixels = 32
            
            pixels_w = pixels/texture.totalw
            pixels_h = pixels/texture.totalh
            
            coords = texture.texture_dictionary[texture_str]
            
            ul = coords[0]
            ulx = ul[0]
            uly = ul[1]
            
            chunk.tvh.vertex_colors[floor.floor_pointer] = coords[0]
            chunk.tvh.vertex_colors[floor.floor_pointer+1] = [ulx+pixels_w,uly]
            chunk.tvh.vertex_colors[floor.floor_pointer+2] = [ulx+pixels_w,uly-pixels_h]
            chunk.tvh.vertex_colors[floor.floor_pointer+3] = [ulx,uly-pixels_h]
        chunk.colors_changed = True
        
        """
        
        if floor_z == self.get_height_floors()-1:
            floor = self.quads[floor_z][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+2] = color
            chunk.vh.vertex_colors[floor.floor_pointer+3] = color
            chunk.colors_changed = True
        if floor_x == self.get_width_floors()-1:
            floor = self.quads[floor_z][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+1] = color
            chunk.vh.vertex_colors[floor.floor_pointer+2] = color
            chunk.colors_changed = True
        
        if self.valid_floor(floor_z, floor_x):
            floor = self.quads[floor_z][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer] = color
            chunk.colors_changed = True
        if self.valid_floor(floor_z-1, floor_x):
            floor = self.quads[floor_z-1][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+3] = color
            chunk.colors_changed = True
        if self.valid_floor(floor_z-1, floor_x-1):
            floor = self.quads[floor_z-1][floor_x-1]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+2] = color
            chunk.colors_changed = True
        if self.valid_floor(floor_z, floor_x-1):
            floor = self.quads[floor_z][floor_x-1]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+1] = color
            chunk.colors_changed = True
        
        """
    """
    reset_floor_texture
    
    calls get_proper_floor_color and sets this floor to whatever shade
    we just got out of that function
    """
    def reset_floor_texture(self, floor_z, floor_x):
        shade = self.get_proper_floor_color(floor_z, floor_x)[0]
        #shade = self.get_proper_floor_shade(floor_z, floor_x)
        #floor = self.quads[floor_z][floor_x]
        
        if self.is_ice(floor_z, floor_x):
            self.set_floor_texture(floor_z, floor_x, "IceTexture-lighting-%d" % (conv_155_255(shade),))
        else:
            self.set_floor_texture(floor_z, floor_x, "MinecraftSnow-lighting-%d" % (conv_155_255(shade),))
    
    
    
    """
    get_proper_floor_color
    
    goes to the correct quadrilateral z,x
    looks at the four corners and calculates color based on angle
    gets the corresponding chunk's vertex handler
    uses the indices of the four corners to set the color to the new color in the vertex handler
    """
    def get_proper_floor_color(self, floor_z, floor_x, consider_ice=True):
        
        #find the floor object and the chunk object
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        
        #find the coordinates of all the 
        ul = chunk.tvh.vertices[floor.floor_pointer]
        ur = chunk.tvh.vertices[floor.floor_pointer+1]
        lr = chunk.tvh.vertices[floor.floor_pointer+2]
        ll = chunk.tvh.vertices[floor.floor_pointer+3]
        
        #find hr and vr or the floor so we can use that to calculate the color
        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ur[0],ur[1],ur[2],lr[0],lr[1],lr[2])
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        
        
        
        color1 = self.calculate_floor_color(hr, vr)
        """
        #cut short here
        return color1
        ##BUTT! Although it loads faster now, it will have just a bit less shading accuracy especially on those non-planar quads
        
        ...
        
        
        No, I want it to have full color accuracy
        """
        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ll[0],ll[1],ll[2],lr[0],lr[1],lr[2])
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        color2 = self.calculate_floor_color(hr, vr)
        
        
        ret = [(color1[0]+color2[0])/2, (color1[1]+color2[1])/2, (color1[2]+color2[2])/2]
        
        return ret
    """
    calculate_floor_color
    
    takes in the hr and vr and calculates a floor color based on that
    """
    def calculate_floor_color(self, hr, vr):
        return [self.calculate_floor_color_single(hr, vr)]*3
    """
    optimized for speed
    """
    def calculate_floor_color_single(self, hr, vr):
        def stretch(_0_to_1,min, max):
            return _0_to_1 * (max-min)+min
        sun = self.properties["sun_angle"]
        angle_distance_from_sun = normal.angle_distance(hr, sun)/math.pi
        inverse_angle_distance_from_sun = 1 - angle_distance_from_sun
        inverse_angle_distance_from_sun_m1_to_p1 = inverse_angle_distance_from_sun*2-1
        
        vertical_rotation_0_to_1 = vr/(math.pi/2)
        inverse_vertical_rotation_0_to_1 = 1 - vertical_rotation_0_to_1
        """
        neutral_floor_color = .8
        extremity = .7
        """
        neutral_floor_color = .5
        #extremity = .5
        #extremity = 1.5
        extremity = 2
        
        inverse_vertical_rotation_0_to_1 = (util.root(2,inverse_vertical_rotation_0_to_1*2-1)+1)/2
        
        color_value = neutral_floor_color + inverse_angle_distance_from_sun_m1_to_p1*inverse_vertical_rotation_0_to_1*extremity#original shader that doesn't give enough contrast
        #color_value = neutral_floor_color + util.root(2, inverse_angle_distance_from_sun_m1_to_p1)*(inverse_vertical_rotation_0_to_1)**.5*extremity#I fell in love with this shader. extremity .5
        #another thing that looks cool is doing extremity 2.5. But I feel like the contrast is too much there. it looks like fricking mars

        
        if color_value > 1: color_value = 1
        if color_value < 0: color_value = 0
        
        
        
        color_value = color_value**.5
        #color_value = stretch(color_value, .6, 1)
        #color_value = stretch(color_value, .54, 1)
        color_value = stretch(color_value, .5, 1)
        #color_value = stretch(color_value, .6, 1)
        
        return color_value
    def is_ice(self, z, x, hr=None, vr=None):
        if not self.valid_floor(z, x):
            return False
        hs = self.properties["horizontal_stretch"]
        vs = self.properties["vertical_stretch"]
        
        seed = (  math.sin((10*int((z*hs)/35))**2) + math.sin((12*int((x*hs)/35))**2)  )/2
        seed2 = (  math.sin((12*int((z*hs)/35))**2) + math.sin((6*int((x*hs)/35))**2)  )/2
        seed3 = (  math.sin((20*int((z*hs)/35))**2) + math.sin((17*int((x*hs)/35))**2)  )/2
        if not(seed < .1 and seed > -.1):return False
        
        xx = x*hs % 35
        zz = z*hs % 35
        if ((xx-(17+seed2*5))**2 + (zz-(17+seed3*5))**2)**.5 > 17:return False
        
        
        def get_elev(zz, xx):
            floor = self.quads[zz][xx]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            return (
                        chunk.tvh.vertices[floor.floor_pointer],
                        chunk.tvh.vertices[floor.floor_pointer+1],
                        chunk.tvh.vertices[floor.floor_pointer+2],
                        chunk.tvh.vertices[floor.floor_pointer+3])
        
        if hr==None and vr==None:
            elevs = get_elev(z, x)
            hr,vr = normal.get_plane_rotation(
                                    x*hs,elevs[0][1],z*hs,
                                    (x+1)*hs,elevs[1][1],z*hs,
                                    (x+1)*hs,elevs[2][1],(z+1)*hs)
            if vr < 0:
                vr = -vr
                hr = hr + math.pi
            
        floor_slope = math.pi/2 - vr
        return (
                floor_slope < constants["ice_slope"][0] and 
                floor_slope > constants["ice_slope"][1] and
                (normal.angle_distance(hr, self.properties["sun_angle"]+math.pi) > constants["no_ice_zone"]/2)
                )
    def is_bump(self, real_z, real_x):
        hs = self.properties["horizontal_stretch"]
        vs = self.properties["vertical_stretch"]
        
        if real_z < 5 or real_x < 5 or real_z > self.get_height_floors()*self.properties["horizontal_stretch"]-6 or real_x > self.get_width_floors()*self.properties["horizontal_stretch"]-6:
            return False
        
        z = int(real_z/hs)
        x = int(real_x/hs)
        
        
        
        if not self.valid_floor(z, x):
            return False
        
        
        
        seed = (  math.sin((17*real_z)**2) + math.sin((27*real_x)**2)  )/2
        seed2 = (  math.sin((209*int((real_z)/35))**2) + math.sin((170*int((real_x)/35))**2)  )/2
        
        if not(seed < constants["bump_density"] and seed > -constants["bump_density"]): return False
        if not(seed2 < constants["bump_group_density"] and seed2 > -constants["bump_group_density"]): return False
        
        hr, vr = self.get_rotation(z, x)
        floor_slope = math.pi/2 - vr
        #print("bump",real_z,real_x)
        return floor_slope < constants["bump_slope"][0] and floor_slope > constants["bump_slope"][1]
        
        
        
    
###################################
#END floor color
###################################






###################################
#STEP AND PAINT STUFF
###################################
    
        
    def step(self):
        pass
        
    def paint(self):
        #draw sky(sun is drawn by game ui)
        def setup_3d_no_trans_no_rot(): gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), 5, 6000 )
        self.draw_quad_3d(-9999999, -9999999, -5800, 9999999, -9999999, -5800, 9999999, 9999999, -5800, -9999999, 9999999, -5800,constants["background_color"], setup_3d=setup_3d_no_trans_no_rot)#draw Sky
        
        
        self.draw(self.get_chunk_load_grid())
        self.draw_mobile()
        
        
        
        glClear(GL_DEPTH_BUFFER_BIT)#clear the depth buffer bit so that the 2d stuff renders on top
        pylooiengine.main_window.draw_borders()
        
        
        
        
        
    def get_chunk_load_grid(self):
        chunk_load_grid =[]
        for r in range(self.get_height_chunks()):
            chunk_load_grid.append([-1]*self.get_width_chunks())
        
        unscaled_view_z = self.view.z/self.properties["horizontal_stretch"]
        unscaled_view_x = self.view.x/self.properties["horizontal_stretch"]
        
        
        player_z_chunk, player_x_chunk = self.convert_to_chunk_coords(unscaled_view_z, unscaled_view_x)
        
        cs = self.properties["chunk_size"]
        los =self.view.line_of_sight
        los2 =self.properties["line_of_sight2"]
        
        def nearest_multiple(x, m):
            return int(x/m + .5)*m
        
        view_angle = math.pi*.35
        
        
        for z in range(nearest_multiple(unscaled_view_z - los2*cs, cs), nearest_multiple(unscaled_view_z + los2*cs, cs)+1, cs):
            for x in range(nearest_multiple(unscaled_view_x - los2*cs, cs), nearest_multiple(unscaled_view_x + los2*cs, cs)+1, cs):
                
                
                #here we are testing whether the chunk at least has trees or not
                if ( (z-unscaled_view_z)**2 + (x-unscaled_view_x)**2 )**.5 <= self.properties["line_of_sight2"]*cs:
                    if view_angle > normal.angle_distance(self.view.hor_rot, util.get_angle(unscaled_view_z, unscaled_view_x, z, x)):
                        #then all four neighboring chunks have trees
                        cz = int(z/cs)
                        cx = int(x/cs)
                        
                        if self.valid_chunk(cz, cx): chunk_load_grid[cz][cx] = 0
                        if self.valid_chunk(cz-1, cx-1): chunk_load_grid[cz-1][cx-1] = 0
                        if self.valid_chunk(cz, cx-1): chunk_load_grid[cz][cx-1] = 0
                        if self.valid_chunk(cz-1, cx): chunk_load_grid[cz-1][cx] = 0
                       
                
                
        for z in range(nearest_multiple(unscaled_view_z - los2*cs, cs), nearest_multiple(unscaled_view_z + los2*cs, cs)+1, cs):
            for x in range(nearest_multiple(unscaled_view_x - los2*cs, cs), nearest_multiple(unscaled_view_x + los2*cs, cs)+1, cs):
                
                #here we are testing whether the chunk is active or not 
                #this has precedence over chunks with trees, so it is executed last
                if ( (z-unscaled_view_z)**2 + (x-unscaled_view_x)**2 )**.5 <= los*cs:#check if this chunk intersection point is within the los of player
                    
                    
                    if (  
                            ((z-unscaled_view_z)**2 + (x-unscaled_view_x)**2)**.5 <= .6*cs#1.2*cs #!!!the chunk must either be super close to the player...
                            or 
                            view_angle > normal.angle_distance(self.view.hor_rot, util.get_angle(unscaled_view_z, unscaled_view_x, z, x))  ):#!!!or the player must be looking at the chunk
                        #then all four neighboring chunks are active
                        cz = int(z/cs)
                        cx = int(x/cs)
                        
                        if self.valid_chunk(cz, cx): chunk_load_grid[cz][cx] = 1
                        if self.valid_chunk(cz-1, cx-1): chunk_load_grid[cz-1][cx-1] = 1
                        if self.valid_chunk(cz, cx-1): chunk_load_grid[cz][cx-1] = 1
                        if self.valid_chunk(cz-1, cx): chunk_load_grid[cz-1][cx] = 1
        
        #here we are testing to see whether the chunk is "Front row" or not
        
        if self.valid_chunk(player_z_chunk, player_x_chunk):
            chunk_load_grid[player_z_chunk][player_x_chunk] = 2 #so the chunk you're standing in is always front row
        
        for z in range(nearest_multiple(unscaled_view_z - los2*cs, cs), nearest_multiple(unscaled_view_z + los2*cs, cs)+1, cs):
            for x in range(nearest_multiple(unscaled_view_x - los2*cs, cs), nearest_multiple(unscaled_view_x + los2*cs, cs)+1, cs):
                #checking if near a corner
                
                def abs(x):return x if x >= 0 else -x
                if (abs(z-unscaled_view_z) < .43*cs and abs(x-unscaled_view_x) < .55*cs) or (abs(z-unscaled_view_z) < .55*cs and abs(x-unscaled_view_x) < .43*cs):
                    cz = int(z/cs)
                    cx = int(x/cs)
                    if self.valid_chunk(cz, cx): chunk_load_grid[cz][cx] = 2
                    if self.valid_chunk(cz-1, cx-1): chunk_load_grid[cz-1][cx-1] = 2
                    if self.valid_chunk(cz, cx-1): chunk_load_grid[cz][cx-1] = 2
                    if self.valid_chunk(cz-1, cx): chunk_load_grid[cz-1][cx] = 2
                """
                #shift the point right and down, now we're checking if close to chunk centers
                z += cs/2
                x += cs/2
                if ( (z-unscaled_view_z)**2 + (x-unscaled_view_x)**2 )**.5 <= .9*cs:
                    z -= cs/2
                    x -= cs/2
                    cz = int(z/cs)
                    cx = int(x/cs)
                    if self.valid_chunk(cz, cx): chunk_load_grid[cz][cx] = 2
                """
                        
        #otherwise, the chunk is -1, which is no trees.
                
        return chunk_load_grid
    def draw_mobile(self):
        mobile_vertices = numpy.array(self.mobile_vertices)
        mobile_colors = numpy.array(self.mobile_colors)
        
        
        self.draw_quad_array_3d(mobile_vertices, mobile_colors, setup_3d=self.get_setup_3d_close())
        self.mobile_vertices = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    
    """
    draw(chunk_load_grid)
            
    new empty numpy array vertices_draw (going to be put into gl draw array by the caller)
    iterates through all the chunks
        if the chunk load grid for that chunk says 1:
            take the vertex handler from that chunk and add it's numpy
            buffer to vertices_draw
            
            make sure that the vertex buffer for all chunk squares does not contain this chunk
        if it's 0:
            if the vertex buffer for all chunk squares does not contain this chunk
                generate the chunk square by calling the function owned by the chunk to generate color
                uses information from the chunk (and the chunk size property) to calculate the four corners
                add the pan chunk square to the vertex buffer for all chunk squares
    
    do all the same for the colors of the quads
    
    does not return anything
    just draws all the chunks
            
    """
    def draw(self, chunk_load_grid):
        
        
        height = len(chunk_load_grid)
        width = 0 if height == 0 else len(chunk_load_grid[0])
        
        #just check that the dimensions of the chunk load grid are same as self.chunks matrix
        check(height == self.properties["height_chunks"] and width == self.properties["width_chunks"], "Dimensions of chunk_load_grid were %d %d but should have been %d %d" % (width, height, self.properties["width_chunks"], self.properties["height_chunks"]))
        
        #add all the chunks' vertexes and colors here (if the chunk load grid is a 1)
        
        vertices_draw = []
        colors_draw = []
        tex_vertices_draw = []
        tex_coords_draw = []
        
        vertices_draw_far = []
        colors_draw_far = []
        tex_vertices_draw_far = []
        tex_coords_draw_far = []
        
        
        
        #if the chunk load grid is not 1, make sure the pan chunk square is added to self.pan_chunk_squares
        
        
        
        #iterate through every single chunk
        #and collect the drawable objects
        for z in range(height):
            for x in range(width):
                #if the chunk load grid says that the chunk should be loaded
                if chunk_load_grid[z][x] == 2:
                    
                    #add this chunk's vertices and colors to the stuff that's gonna be drawn
                    vertices_draw.append(self.chunks[z][x].vh.vertices)
                    colors_draw.append(self.chunks[z][x].vh.vertex_colors)
                    
                    tex_vertices_draw.append(self.chunks[z][x].tvh.vertices)
                    tex_coords_draw.append(self.chunks[z][x].tvh.vertex_colors)
                if chunk_load_grid[z][x] == 1:
                    #add this chunk's vertices and colors to the stuff that's gonna be drawn
                    vertices_draw_far.append(self.chunks[z][x].vh.vertices)
                    colors_draw_far.append(self.chunks[z][x].vh.vertex_colors)
                    
                    tex_vertices_draw_far.append(self.chunks[z][x].tvh.vertices)
                    tex_coords_draw_far.append(self.chunks[z][x].tvh.vertex_colors)
                elif chunk_load_grid[z][x] == 0:
                    pcsquares = self.chunks[z][x].get_pan_chunk_squares(z, x)
                    vertices_draw_far.append(pcsquares.vertices)
                    colors_draw_far.append(pcsquares.vertex_colors)
                elif chunk_load_grid[z][x] == -1:
                    pcsquares = self.chunks[z][x].get_pan_chunk_squares(z, x, trees=False)
                    vertices_draw_far.append(pcsquares.vertices)
                    colors_draw_far.append(pcsquares.vertex_colors)
                    
                
                
        
        
        
       
        
        #now here's where we do all the drawing (and stacking)
        if len(vertices_draw_far) > 0:
            #first draw far stuff, then clear the depth buffer bit so close stuff can draw ontop of it
            vertices_draw_far = numpy.vstack(vertices_draw_far)
            colors_draw_far = numpy.vstack(colors_draw_far)
            self.draw_quad_array_3d(vertices_draw_far, colors_draw_far, setup_3d=self.get_setup_3d_far())
        if len(tex_vertices_draw_far) > 0:
            glBlendFunc(GL_ONE, GL_ZERO)#textures have to be completely opaque to be drawn
            glEnable(GL_BLEND);
            tex_vertices_draw_far = numpy.vstack(tuple(tex_vertices_draw_far))
            tex_coords_draw_far = numpy.vstack(tuple(tex_coords_draw_far))
            self.draw_image_array_3d(tex_vertices_draw_far, tex_coords_draw_far, texture.tex, texture.tex_b, setup_3d=self.get_setup_3d_far())
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND);
        
        glClear(GL_DEPTH_BUFFER_BIT)
        
        
        if len(vertices_draw) > 0:
            vertices_draw = numpy.vstack(tuple(vertices_draw))
            colors_draw = numpy.vstack(tuple(colors_draw))
            self.draw_quad_array_3d(vertices_draw, colors_draw, setup_3d=self.get_setup_3d_close())
        if len(tex_vertices_draw) > 0:
            glBlendFunc(GL_ONE, GL_ZERO)#textures have to be completely opaque to be drawn
            glEnable(GL_BLEND);
            tex_vertices_draw = numpy.vstack(tuple(tex_vertices_draw))
            tex_coords_draw = numpy.vstack(tuple(tex_coords_draw))
            self.draw_image_array_3d(tex_vertices_draw, tex_coords_draw, texture.tex, texture.tex_b, setup_3d=self.get_setup_3d_close())
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND);
            
            
       
            
            
        
            
        
        return#######################
        
        
###################################
#END paint stuff
###################################
    
    """
    input coordinates referring to a specific quad, and it outputs chunk coordinates
    referring to which chunk that quad resides in
    """
    def convert_to_chunk_coords(self, z, x):
        return int(z/self.properties["chunk_size"]), int(x/self.properties["chunk_size"])
    
    
    """
    add_quad
    
    adds a mobile quad
    """
    def add_mobile_quad(self, vertex1, vertex2, vertex3, vertex4, color):
        self.mobile_vertices.append(vertex1)
        self.mobile_vertices.append(vertex2)
        self.mobile_vertices.append(vertex3)
        self.mobile_vertices.append(vertex4)
        if isinstance(color, Color):
            color = color.to_tuple()
            self.mobile_colors.append(color)
            self.mobile_colors.append(color)
            self.mobile_colors.append(color)
            self.mobile_colors.append(color)
        elif type(color) == type([]):
            for i in range(4):
                self.mobile_colors.append(color)
        elif type(color) == type(()):
            for i in range(4):
                self.mobile_colors.append(color[i])
    
    
    def add_fixed_quad(self, vertex1, vertex2, vertex3, vertex4, color, anchor_z, anchor_x, object=None):
        chunk_z, chunk_x = self.convert_to_chunk_coords(anchor_z, anchor_x)
        
        if isinstance(color, list):
            ret = self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex1, color)
            self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex2, color)
            self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex3, color)
            self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex4, color)
        elif isinstance(color, tuple):
            ret = self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex1, color[0])
            self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex2, color[1])
            self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex3, color[2])
            self.chunks[chunk_z][chunk_x].vh.add_vertex(vertex4, color[3])
        
        self.chunks[chunk_z][chunk_x].colors_changed = True
        
        if object != None:
            self.quads[anchor_z][anchor_x].containedObjects.append(object)

        return ret
    def remove_fixed_quad(self, quad_id, anchor_z, anchor_x, object=None):
        chunk_z, chunk_x = self.convert_to_chunk_coords(anchor_z, anchor_x)
        
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id)
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id+1)
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id+2)
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id+3)
        
        self.chunks[chunk_z][chunk_x].colors_changed = True
        
        if object != None:
            self.quads[anchor_z][anchor_x].containedObjects.remove(object)

    def get_view_pointing(self):
        view = self.view
        hr = view.hor_rot
        vr = view.vert_rot
        step_size = .5
        ray = [view.x, view.y, view.z]
        while True:
            if ( (ray[0]-view.x)**2 + (ray[2]-view.z)**2 ) ** .5 > view.line_of_sight*self.properties["chunk_size"]*self.properties["horizontal_stretch"] + 2:
                return None
            grid_x = int(ray[0] / self.properties["horizontal_stretch"])
            grid_z = int(ray[2] / self.properties["horizontal_stretch"])
            
            if grid_x >= self.get_width_floors()-1 or grid_z >= self.get_height_floors()-1 or grid_x < 0 or grid_z < 0:
                pass#not inside world
            else:
                four_corners = [self.get_elevation(grid_z, grid_x, scaled=True), 
                    self.get_elevation(grid_z+1, grid_x, scaled=True), 
                    self.get_elevation(grid_z+1, grid_x+1, scaled=True), 
                    self.get_elevation(grid_z, grid_x+1, scaled=True)]
                highest = max(four_corners) + step_size*self.properties["horizontal_stretch"]
                lowest = min(four_corners) - step_size*self.properties["horizontal_stretch"]*3
                if ray[1] <= highest and ray[1] >= lowest: 
                    #if self.grid[grid_z][grid_x].floor_vert_handler_index == None:
                    #    return None
                    #else:
                    return grid_z, grid_x
                
            ray[0] += step_size*self.properties["horizontal_stretch"] * math.cos(hr) * math.cos(vr)
            ray[2] += step_size*self.properties["horizontal_stretch"] * -math.sin(hr) * math.cos(vr)
            ray[1] += step_size*self.properties["horizontal_stretch"] * math.sin(vr)
    """
    add_object_account
    
    accounts for this object so that when the world is saved to a file, 
    this object can be recreated the next time this world is made
    
    the creation code should be one (or more if you use semicolons) lines of 
    code that create, setup, and add the appropriate object into the world.
    This code will be invoked when the world is being loaded next time.
    
    This code can assume that the variable "world" contains the world we will
    be adding to
    """
    #def add_object_account(self, object, creation_code):
    #    self.object_account[id(object)] = creation_code
    """
    When you delete an object in game, you want it so that when you save
    the world, that object is never saved. Use delete_object_account to
    remove the object from the save list
    """
    #def delete_object_account(self, object):
    #    del self.object_account[id(object)]
def rad_to_deg(radians):
    return radians/(2*math.pi) * 360
def round(x):
    return int(x + .5)





'''
BEST. SHADING. ALGORITHM. EVER

def calculate_floor_color_single(self, hr, vr):
    def stretch(_0_to_1,min, max):
        return _0_to_1 * (max-min)+min
    sun = self.properties["sun_angle"]
    angle_distance_from_sun = normal.angle_distance(hr, sun)/math.pi
    inverse_angle_distance_from_sun = 1 - angle_distance_from_sun
    inverse_angle_distance_from_sun_m1_to_p1 = inverse_angle_distance_from_sun*2-1
    
    vertical_rotation_0_to_1 = vr/(math.pi/2)
    inverse_vertical_rotation_0_to_1 = 1 - vertical_rotation_0_to_1
    """
    neutral_floor_color = .8
    extremity = .7
    """
    neutral_floor_color = .5
    #extremity = .5
    #extremity = 1.5
    extremity = 2
    
    inverse_vertical_rotation_0_to_1 = (util.root(2,inverse_vertical_rotation_0_to_1*2-1)+1)/2
    
    color_value = neutral_floor_color + inverse_angle_distance_from_sun_m1_to_p1*inverse_vertical_rotation_0_to_1*extremity#original shader that doesn't give enough contrast
    #color_value = neutral_floor_color + util.root(2, inverse_angle_distance_from_sun_m1_to_p1)*(inverse_vertical_rotation_0_to_1)**.5*extremity#I fell in love with this shader. extremity .5
    #another thing that looks cool is doing extremity 2.5. But I feel like the contrast is too much there. it looks like fricking mars

    
    if color_value > 1: color_value = 1
    if color_value < 0: color_value = 0
    
    
    
    color_value = color_value**.5
    #color_value = stretch(color_value, .6, 1)
    #color_value = stretch(color_value, .54, 1)
    color_value = stretch(color_value, .5, 1)
    #color_value = stretch(color_value, .6, 1)
'''





