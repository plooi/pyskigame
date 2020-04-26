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
from bump import Bump, NaturalBump
from world_object import WorldObject

import texture
import world_operations
from PIL import Image
from time import time
from lift import Pole
import lift
import os
from shading import *

import fast_shadows

from shadow_map import ShadowMap
import particle






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
        self.line_of_sight = 2 #IN NUMBER OF CHUNKS (not opengl space) #the radius
        self.max_vert_rot = math.pi/2.3
        

        
class Quad:
    def __init__(self):
        self.my_chunk_x = -1#keeps track of which chunk we're in
        self.my_chunk_z = -1#keeps track of which chunk we're in
        
        self.floor_pointer = -1#keeps track of the position of the floor quad in the chunk vertex handler
        
        self.containedObjects = []#keeps track of all 3d objects that are related to this quadrilateral (like trees)
class Chunk:
    def __init__(self, world):
        self.vh = VertexHandler(3,initial_capacity=world.properties["chunk_size"]**2+1)#vertex handler to store all non-moving drawables in this chunk
        self.tvh = texture.new_texture_handler(initial_capacity=10)
        self.svh = VertexHandler(3)#shadow vertex handler
        
        self.world = world
        
        self.colors_changed = True
        self.pan_chunk_squares = None
        
        self.tree_shadows_loaded = False
        
        
    def changed(self):
        #self.tree_shadows_loaded = False
        self.colors_changed = True
            
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
        
        
        
        chunk_spanning_square = {}
        
        
        if self.colors_changed or not isinstance(self.pan_chunk_squares, dict):
            
            self.colors_changed=False
            side_length_in_sub_chunks = int(sub_chunks**.5)#how many sub chunks does this chunk have in each row?
            sub_chunk_side_length = int(cs/side_length_in_sub_chunks)#how many floors does each sub chunk have on each row?
            self.pan_chunk_squares = {"trees":VertexHandler(3,initial_capacity=1), "without" : VertexHandler(3,initial_capacity=1)}
            
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
                            
                        shade = self.world.calculate_floor_color_single(hr, vr)
                        shade = conv_87_255(shade)
                        color = apply_color(shade,scale="0-1")
                        
                        ret = color
                            
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
                                    
                                    #base = -999999
                                    base = -30
                                    wid = .3
                                    
                                    hei = 10
                                    brightness = self.world.get_proper_floor_color(r, c)[0]
                                    pole_color = [.75,.75,.75]
                                    pole_color2 = [0,0,0]
                                    
                                    t_color = [.68,.68,.68]
                                    t_wid = 1.3
                                    t_h = .8
                                    
                                    
                                    self.pan_chunk_squares["trees"].add_vertex([real_x-wid,real_y+hei,real_z], pole_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+wid*.7,real_y+hei,real_z+wid*.7], pole_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x+wid*.7,real_y+hei,real_z-wid*.7], pole_color)
                                    self.pan_chunk_squares["trees"].add_vertex([real_x,real_y+base,real_z], pole_color2)
                                    
                                    
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
                    #THIS IS JUST FANCY CODE TO MAKE THE "without" vertex handler have just one 
                    #single quad that covers the whole chunk
                    if scr == 0 and scc == 0:#upper left
                        chunk_spanning_square["ul"] = (ul,color1254)
                    if scr == side_length_in_sub_chunks-1 and scc == 0:
                        chunk_spanning_square["ll"] = (ll,color4587)
                    if scr == side_length_in_sub_chunks-1 and scc == side_length_in_sub_chunks-1:
                        chunk_spanning_square["lr"] = (lr,color5689)
                    if scr == 0 and scc == side_length_in_sub_chunks-1:
                        chunk_spanning_square["ur"] = (ur,color2365)
                    
                    #with trees
                    self.pan_chunk_squares["trees"].add_vertex(ul,color1254)
                    self.pan_chunk_squares["trees"].add_vertex(ur,color2365)
                    self.pan_chunk_squares["trees"].add_vertex(lr,color5689)
                    self.pan_chunk_squares["trees"].add_vertex(ll,color4587)
                    
                    ##remove those lines because the trees pan chunk squares should not contain the floor
                    #no, now we do need them because trees pan chunk squares now contain the MORE DETAILED slope
                    
                    #""" NO SKY COVERUP NEEDED because the pan chunk squares always draw
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
                    
                    #"""
                    
        
        
            self.pan_chunk_squares["without"].add_vertex(chunk_spanning_square["ul"][0],chunk_spanning_square["ul"][1])
            self.pan_chunk_squares["without"].add_vertex(chunk_spanning_square["ur"][0],chunk_spanning_square["ur"][1])
            self.pan_chunk_squares["without"].add_vertex(chunk_spanning_square["lr"][0],chunk_spanning_square["lr"][1])
            self.pan_chunk_squares["without"].add_vertex(chunk_spanning_square["ll"][0],chunk_spanning_square["ll"][1])
        
        
        
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
            "chunk_size" : 16,
            "sub_chunk_squares" : 16,
            "width" : -1,
            "height" : -1,
            "width_chunks" : -1,
            "height_chunks" : -1,
            "line_of_sight2" : 5,#how many chunks away before the trees start to disappear
            "line_of_sight3" : -1,#how many chunks away before no pan chunk squares are rendered
            "horizontal_stretch" : 4,
            "vertical_stretch" : .15,
            
            "allow_shadow_hiding" : True,
            
            "world_image_pix_per_floor" : 1,
            
            "tree_shadow_updates_per_frame" : 1,
            
            "sun_angle" : 0,
            "scenery_angle" : 0,
            "scenery_height" : 0,
            "scenery_radius" : 7000,
            "scenery_segments" : 20,
            "scenery_lower_stretch" : 10000,
            
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
        self.pan_chunk_squares_changed = True
        
        
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
        
        #self.pan_background = image("Panorama.png")
        #self.pan_background = self.pan_background,self.pan_background.tobytes("raw", "RGBA", 0, -1)
        self.pan_background = None
        
        self.disable_remove_fixed_quads = False
        
        self.shadow_map = ShadowMap(self)
        
        self.particle_handler = VertexHandler(2)
        self.last_sparkle_spacing = -999,-999
        self.chunks_in_sight_memo = {}
        
        self.far_shadows = True #if true, all shadows will draw
                                #if false, only shadows close by will draw
        self.lastx = None
        self.lasty = None
        self.lastz = None
        self.lasthr = None
        self.lastvr = None
    """
    init_csv
    """
    
    def init_csv(self, name, csv_name, more_properties={}, view=None, tree_chance = .5):
        lines = []
        f = open(csv_name, "r")
        for line in f:
            lines.append([(0 if x.strip()=="None" else float(x)) for x in line.split(",")])
        f.close()
        
        height = len(lines)
        width = 0 if height==0 else len(lines[0])
        ret = self.init(name, width-1, height-1, more_properties, lambda z,x: lines[z][x], view, natural_bumps=False) 
        
        #smooth yourself
        world_operations.smooth(self, 0,0,height,width)
        
        
        #do trees from csv file
        if os.path.isfile(csv_name + "tree"):
            loading.progress_bar("Creating trees...")
            f = open(csv_name + "tree", "r")
            trees = []
            for line in f:
                trees.append(line.split(","))
            
            for r in range(len(trees)):
                for c in range(len(trees[0])):
                    if trees[r][c] == "1" and self.valid_floor(r, c):
                        if random() < tree_chance:
                            Tree(z=r, x=c, world=self)
                if r % 25 == 0:
                    loading.update(r/len(trees)*100)
            loading.update(100)
            
            f.close()
        
        
        
        #now do natural bumps
        world_operations.natural_bumps(self, 0,0,self.get_height_points(), self.get_width_points(), prog_bar=True)
        
        return ret
    
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
    def init(self, name, width, height, more_properties={}, elevation_function=lambda z,x:0, view=None, prog_bar=True, natural_bumps=True):
        self.quads = []
        self.chunks = []
        self.pan_chunk_squares = None
    
    
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
        self.mobile_vertices_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_vertices_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        
        #initialize all chunks
        for z in range(self.properties["height_chunks"]):
            row = []
            for x in range(self.properties["width_chunks"]):
                c = Chunk(self)
                
                row.append(c)
            self.chunks.append(row)
            
        
        self.list_mode()
        
        
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
                
            if prog_bar and z % 25 == 0: loading.update(z/self.properties["height"]*50)
        #reset floor textures
        #by the way, having this as it's own loop increased performance by 15%
        for z in range(self.properties["height"]):
            for x in range(self.properties["width"]):
                self.reset_floor_texture(z, x)
            if prog_bar and z % 25 == 0: loading.update(z/self.properties["height"]*50+50)
            
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
        if natural_bumps:
            world_operations.natural_bumps(self, 0,0,self.get_height_points(), self.get_width_points(), prog_bar=True)
        
        
        
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
    def get_setup_3d_far(self,translate=True):
        def setup_3d():
            gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), (constants["front_row_chunk_distance"]-.5)*self.properties["chunk_size"]*self.properties["horizontal_stretch"], constants["max_los"] )
            try:
                glRotate(rad_to_deg(-(self.view.hor_rot-math.pi/2)), 0, 1, 0)
                glRotate(rad_to_deg(-self.view.vert_rot), math.cos(self.view.hor_rot - math.pi/2), 0, -math.sin(self.view.hor_rot - math.pi/2))
                if translate:
                    glTranslate(-self.view.x, -self.view.y, -self.view.z)
            except Exception as e:
                pass
        return setup_3d
    def get_setup_3d_chunk_draw(self):
        def setup_3d():
            #gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), self.view.line_of_sight*.7*self.properties["chunk_size"]*self.properties["horizontal_stretch"], constants["max_los"] )
            gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), self.view.line_of_sight*.5*self.properties["chunk_size"]*self.properties["horizontal_stretch"], constants["max_los"] )
            try:
                glRotate(rad_to_deg(-(self.view.hor_rot-math.pi/2)), 0, 1, 0)
                glRotate(rad_to_deg(-self.view.vert_rot), math.cos(self.view.hor_rot - math.pi/2), 0, -math.sin(self.view.hor_rot - math.pi/2))
                glTranslate(-self.view.x, -self.view.y, -self.view.z)
            except Exception as e:
                pass
        return setup_3d
    def get_setup_3d_super_far_chunk_draw(self):
        if self.game_ui.game_mode == "map editor":
            return self.get_setup_3d_far()
        def setup_3d():
            
            gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), self.properties["line_of_sight2"]*.5*self.properties["chunk_size"]*self.properties["horizontal_stretch"], constants["max_los"] )
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
        x = int(x)
        z = int(z)
        if z < 0: z = 0
        if x < 0: x = 0
        if z >= self.get_height_points(): z = self.get_height_points()-1
        if x >= self.get_width_points(): x = self.get_width_points()-1
        
        if z > 0 and x > 0:
            #for all the points not in first column or row
            chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x-1)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z-1][x-1].floor_pointer
            point = chunk_obj.tvh.vertices[floor_pointer+2]#+2 for lower right
            return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
        else:
            #we must be in the first row, or first column, or both
            if x == 0 and z == 0:
                chunk_z, chunk_x = self.convert_to_chunk_coords(0, 0)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[0][0].floor_pointer
                point = chunk_obj.tvh.vertices[floor_pointer+0]#+0 for upper left
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
            elif x == 0:
                chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, 0)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z-1][0].floor_pointer
                point = chunk_obj.tvh.vertices[floor_pointer+3]#+3 for lower left
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
            elif z == 0:
                #for all the points not in first column or row
                chunk_z, chunk_x = self.convert_to_chunk_coords(0, x-1)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[0][x-1].floor_pointer
                point = chunk_obj.tvh.vertices[floor_pointer+1]#+1 for upper right right
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
            else:
                raise Exception("Impossible!"+str(z)+" " + str(x))
            
        """
            
        
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
        """
    
    
    
    
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
        chunk.changed()
        self.pan_chunk_squares_changed = True
        
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
            self.set_floor_texture(floor_z, floor_x, "IceTexture-lighting-%d" % (conv_87_255(shade),))
        else:
            self.set_floor_texture(floor_z, floor_x, "MinecraftSnow-lighting-%d" % (conv_87_255(shade),))
    
    
    
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
        return shade_hill(hr, vr, self.properties["sun_angle"])
        
    def is_ice(self, z, x, hr=None, vr=None):
        return False#ICE DISABLED
        if not self.valid_floor(z, x):
            return False
        hs = self.properties["horizontal_stretch"]
        vs = self.properties["vertical_stretch"]
        
        seed = (  math.sin((10*int((z*hs)/35))**2) + math.sin((12*int((x*hs)/35))**2)  )/2
        seed2 = (  math.sin((12*int((z*hs)/35))**2) + math.sin((6*int((x*hs)/35))**2)  )/2
        seed3 = (  math.sin((20*int((z*hs)/35))**2) + math.sin((17*int((x*hs)/35))**2)  )/2
        if not(seed < .14 and seed > -.14):return False
        
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
    def draw_snow_tex(self):
        start = time()
        def get_texture(dist0to1):
            dist0to1 = dist0to1 ** .5
            """
            if dist0to1 > .9: return "SnowTex05Blurry"
            if dist0to1 > .85: return "SnowTex10Blurry"
            if dist0to1 > .8: return "SnowTex20Blurry"
            if dist0to1 > .75: return "SnowTex30Blurry"
            if dist0to1 > .65: return "SnowTex40Blurry"
            """
            if dist0to1 > .85: return "SnowTex05Blurry"
            if dist0to1 > .825: return "SnowTex10Blurry"
            if dist0to1 > .8: return "SnowTex15Blurry"
            if dist0to1 > .775: return "SnowTex20Blurry"
            if dist0to1 > .75: return "SnowTex25Blurry"
            if dist0to1 > .725: return "SnowTex30Blurry"
            if dist0to1 > .7: return "SnowTex35Blurry"
            if dist0to1 > .6: return "SnowTex40Blurry"
            #if dist0to1 > .5: return "SnowTex40Blurry"
            
            return "SnowTex40Blurry"#"SnowTex40Clear"
        
        
        up = .05
        
        
        hs = self.properties["horizontal_stretch"]
        vs = self.properties["vertical_stretch"]
        
        
        
        radius = int(70/hs)
        radius_sq = radius**2
        
        
        
        tvh = texture.new_texture_handler()
        #tvh.list_mode()
        
        
        
        
        zc = self.view.z/hs
        xc = self.view.x/hs
        
        hr = self.view.hor_rot
        step_back = 20/hs
        zc -= step_back*math.sin(hr+math.pi)
        xc += step_back*math.cos(hr+math.pi)
        zcfloat = zc
        xcfloat = xc
        
        zc=int(zc)
        xc=int(xc)
        
        for z in range(zc - radius-1, zc + radius+1):
            for x in range(xc - radius-1, xc + radius+1):
                distance_sq = (z+.5-zcfloat)**2 + (x+.5-xcfloat)**2
                if not self.valid_floor(z,x):
                    continue
                
                if normal.angle_distance(get_angle(zc, xc, z, x), self.view.hor_rot) < math.pi/3.9:
                    if distance_sq < radius_sq:
                        texture.add_image_to_vertex_handler(
                                    tvh, 
                                    [x*hs,self.get_elevation(z,x)*vs+up, z*hs],
                                    [(x+1)*hs,self.get_elevation(z,x+1)*vs+up, z*hs],
                                    [(x+1)*hs,self.get_elevation(z+1,x+1)*vs+up, (z+1)*hs],
                                    [(x)*hs,self.get_elevation(z+1,x)*vs+up, (z+1)*hs],
                                    get_texture(distance_sq/radius_sq)
                                    )
        #print("setup took", time()-start)
        #tvh.numpy_mode()
        start = time()
        self.draw_tex(tvh.vertices, tvh.vertex_colors, self.get_setup_3d_close(), mipmap=False, blend=True)
        #print("draw took", time()-start)
                        
    def draw_sparkles(self):
        spacing = 2.2
        
        spaces_passed_until_reset = 3#5
        
        z_c = int(self.view.z/spacing)*spacing
        x_c = int(self.view.x/spacing)*spacing
        
        
        #if (z_c,x_c) != self.last_sparkle_spacing:
        #if ( (self.last_sparkle_spacing[0] - z_c)**2 + (self.last_sparkle_spacing[1] - x_c)**2 ) ** .5 > spacing * spaces_passed_until_reset:
        
        
        if self.game_ui.clock %7 == 0:
            self.last_sparkle_spacing = (z_c,x_c)
            self.sparkle_buffer = VertexHandler(3),VertexHandler(3)
            self.sparkle_buffer[0].list_mode()
            self.sparkle_buffer[1].list_mode()
        
        
        
            
            
            try:
                shade_at_player = self.get_proper_floor_color(int(self.view.z/self.properties["horizontal_stretch"]),int(self.view.x/self.properties["horizontal_stretch"]))[0]
            except:
                return
            
            #if shade_at_player > .35:
            if shade_at_player > .55:
                c = [0,0,0]
            else:
                #c = [.4,.6,1]
                #c = [.7,.85,1]
                c = [1,1,1]
            
            
            radius = 21#28
            radius_sq = radius**2
            
            
            sparkle_density = 1
            
            
            for z in range_float(-radius+z_c,radius+z_c,spacing):
                for x in range_float(-radius+x_c,radius+x_c,spacing):
                    #if not self.valid_point(z, x):continue
                    #key = z*self.get_width_points()+x
                    #key *= 10
                    #key = key ** 2
                    if 1:#math.sin(key) > 1-sparkle_density*2:
                        sizekey = z*self.get_width_points()+x
                        sizekey *= 5
                        sizekey = sizekey ** 2
                        
                        w = .0085 + (math.sin(sizekey)*.5+.5)*.0085
                        
                        
                        
                        
                        #dist = ((self.view.x-x) ** 2 + (self.view.z-z) ** 2)**.5
                        dist = ((self.view.x-x) ** 2 + (self.view.z-z) ** 2)
                        
                        """
                        #makes some sparkles only appear when very close, but others start to appear even far away
                        appeardistkey = z*self.get_width_points()+x
                        appeardistkey *= 8.5
                        appeardistkey *= appeardistkey
                        appeardistkey = math.sin(appeardistkey)
                        appeardistkey = (appeardistkey*.5+.5)*6+1
                        dist *= appeardistkey
                        """
                        
                        
                        
                        xposkey = int(z)*self.get_width_points()+int(x)
                        xposkey *= 17
                        xposkey = xposkey ** 2
                        xposkey = math.sin(xposkey) * spacing/2
                        zposkey = int(z)*self.get_width_points()+int(x)
                        zposkey *= 19
                        zposkey = zposkey ** 2
                        zposkey = math.sin(zposkey) * spacing/2
                        
                        
                        x += xposkey
                        z += zposkey
                        
                        
                        
                        
                        theta = get_angle(self.view.z,self.view.x,z,x)
                        
                        
                        
                        
                        
                        
                        
                        if dist < 3**2 or (dist < radius_sq  and normal.angle_distance(theta,self.view.hor_rot) < math.pi/5):
                        #if dist < radius_sq:
                            
                            
                            
                            
                            unscaled_z = z/self.properties["horizontal_stretch"]
                            unscaled_x = x/self.properties["horizontal_stretch"]
                            #print(unscaled_z, unscaled_x)
                            unscaled_y = self.get_elevation_continuous(unscaled_z, unscaled_x)
                            y = unscaled_y * self.properties["vertical_stretch"]
                            
                            theta += math.pi/2
                            
                            #colorkey = z*self.get_width_points()+x
                            #colorkey *= 18
                            #colorkey = colorkey ** 2
                            
                            
                            #shade = .1#(math.sin(colorkey)*.5+.5)*.5 +.5
                            
                            
                            
                            sparkle_chunk_z,sparkle_chunk_x = self.convert_to_chunk_coords(int(z/self.properties["horizontal_stretch"]),int(x/self.properties["horizontal_stretch"]))
                            if sparkle_chunk_z >= 0 and sparkle_chunk_z < len(self.chunk_load_grid) and sparkle_chunk_x >= 0 and sparkle_chunk_x < len(self.chunk_load_grid[0]):
                                if self.chunk_load_grid[sparkle_chunk_z][sparkle_chunk_x] == 2:
                                    #add to near sparkle buffer (0)
                                    self.sparkle_buffer[0].add_vertex([x,y+w*2,z],c)
                                    self.sparkle_buffer[0].add_vertex([x+w*math.cos(theta),y+w,z-w*math.sin(theta)],c)
                                    self.sparkle_buffer[0].add_vertex([x,y,z],c)
                                    self.sparkle_buffer[0].add_vertex([x-w*math.cos(theta),y+w,z+w*math.sin(theta)],c)
                                else:
                                    #add to far sparkle buffer (1)
                                    self.sparkle_buffer[1].add_vertex([x,y+w*2,z],c)
                                    self.sparkle_buffer[1].add_vertex([x+w*math.cos(theta),y+w,z-w*math.sin(theta)],c)
                                    self.sparkle_buffer[1].add_vertex([x,y,z],c)
                                    self.sparkle_buffer[1].add_vertex([x-w*math.cos(theta),y+w,z+w*math.sin(theta)],c)
                            
                            """
                            self.add_mobile_quad(
                                [x,y+w*2,z],
                                [x+w*math.cos(theta),y+w,z-w*math.sin(theta)],
                                [x,y,z],
                                [x-w*math.cos(theta),y+w,z+w*math.sin(theta)],
                                c)
                            """
                        x -= xposkey
                        z -= zposkey
            self.sparkle_buffer[0].numpy_mode()
            self.sparkle_buffer[1].numpy_mode()
    def delete_shadow_map_memos(self):
        self.shadow_map.get_elev_memo = {}
        self.shadow_map.shadow_color_memo = {}
    def calculate_pan_chunk_vertex_handler(self):
        if self.pan_chunk_squares_changed:
            self.pan_chunk_squares_changed = False
            verts = []
            colors = []
            
            for z in range(self.get_height_chunks()):
                for x in range(self.get_width_chunks()):
                    pan_chunk_squares = self.chunks[z][x].get_pan_chunk_squares(z,x,trees=False)
                    verts.append(pan_chunk_squares.vertices)
                    colors.append(pan_chunk_squares.vertex_colors)
                    
                    #print(len(pan_chunk_squares.vertices))
            
            verts = numpy.vstack(verts)
            colors = numpy.vstack(colors)
            self.pan_chunk_squares = {"verts":verts,"colors":colors}
            #print(len(verts))
    def draw_sun(self, model):
        
        vertices = numpy.zeros([len(model), 3])
        vertex_colors = numpy.zeros([len(model), 3])
        numpy_index = 0
        for i in range(0,len(model),5):
            
            vertices[numpy_index] = model[i]
            vertices[numpy_index+1] = model[i+1]
            vertices[numpy_index+2] = model[i+2]
            vertices[numpy_index+3] = model[i+3]
            vertex_colors[numpy_index] = model[i+4]
            vertex_colors[numpy_index+1] = model[i+4]
            vertex_colors[numpy_index+2] = model[i+4]
            vertex_colors[numpy_index+3] = model[i+4]
            
            numpy_index += 4
        self.draw_quad_array_3d(vertices, vertex_colors, self.get_setup_3d_far())
        
        
        
        
        
        
        
        
    def particle_response(self):
        if self.lastx == None or self.lasty == None or self.lastz == None or self.lasthr == None or self.lastvr == None:
            pass
        else:
            sign = 1 if util.is_a_left_of_b(self.lasthr,self.view.hor_rot) else -1
            
            particle.left(sign*normal.angle_distance(self.lasthr,self.view.hor_rot)*2000)
            
            
            
            
            
            dir_moving = util.get_angle(self.lastz, self.lastx, self.view.z, self.view.x)
            mag = ( (self.lastz-self.view.z)**2 + (self.lastx-self.view.x)**2 )**.5
            
            dir_moving_minus_hr = normal.angle_distance(self.view.hor_rot,dir_moving)
            
            if util.is_a_left_of_b(self.view.hor_rot,dir_moving):
                dir_moving_minus_hr *= -1
                
                
            x_move = -mag*math.sin(dir_moving_minus_hr)*20
            z_move = mag*math.cos(dir_moving_minus_hr)*20
            
            particle.forward(z_move)
            particle.left(x_move)
            
            
            y_move = self.view.y - self.lasty
            particle.up(y_move*20)
            
            
            vr_move = self.view.vert_rot - self.lastvr
            particle.up(vr_move*2000)
        
        
        
        
        self.lastx = self.view.x
        self.lasty = self.view.y
        self.lastz = self.view.z
        self.lasthr = self.view.hor_rot
        self.lastvr = self.view.vert_rot
        
        
        
    def snowing(self, intensity, size= .016):
        while len(particle.snowfall_particles) < intensity:
            particle.SnowFall(self)
        while len(particle.snowfall_particles) > intensity:
            particle.snowfall_particles[0].deactivate()
        
             
    def step(self):
    
    
        
        #self.snowing(30)
        self.particle_response()
    
        
        #every step delete the shadow map's memos
        self.delete_shadow_map_memos()
        
        
        if self.game_ui.clock % constants["ray_tracing_memo_refresh_every_n_ticks"] == 0: self.chunks_in_sight_memo = {} #get rid of the chunks_in_sight memo every 30 secs so when you move, it will, after a short while, recalculate which chunks you can see
        #this variable allows you to memoize the ray tracing, but it will only work properly if we recalculate it every so often
        
        
        self.numpy_mode()
        start = time()
        
        
        
        self.calculate_pan_chunk_vertex_handler()
        
        
        
        self.chunk_load_grid = self.get_chunk_load_grid()
        
        
        
        #print("chunk load grid took " + str(time()-start) + " seconds")
        
    
        glDisable(GL_BLEND)#performance optimization
        
        
        start = time()
        self.draw_scenery()
        self.game_ui.draw_sun()
        
        glClear(GL_DEPTH_BUFFER_BIT)
        for obj in self.get_my_window().layered_looi_objects + self.get_my_window().unlayered_looi_objects:
            if hasattr(obj,"draw_heavenly_body"):
                obj.draw_heavenly_body()
        glClear(GL_DEPTH_BUFFER_BIT)
        
        
        self.draw(self.chunk_load_grid)
        self.particle_handler = VertexHandler(2)
        
        
        
        glClear(GL_DEPTH_BUFFER_BIT)
        
        
        #self.shader1()
        
        
        glClear(GL_DEPTH_BUFFER_BIT)#clear the depth buffer bit so that the 2d stuff renders on top
        
        pylooiengine.main_window.draw_borders()
    def shader1(self):
        glEnable(GL_BLEND)
        glDisable(GL_ALPHA_TEST)
        glBlendEquation(GL_FUNC_REVERSE_SUBTRACT)
        self.draw_rect(0,0,self.get_my_window().get_internal_size()[0],self.get_my_window().get_internal_size()[1], Color(0,1,1,.1))
        glEnable(GL_ALPHA_TEST)
        glDisable(GL_BLEND)
    def shader2(self):
        glEnable(GL_BLEND)
        glDisable(GL_ALPHA_TEST)
        #glBlendEquation(GL_FUNC_SUBTRACT)
        self.draw_rect(0,0,self.get_my_window().get_internal_size()[0],self.get_my_window().get_internal_size()[1], Color(1,1,0,.2))
        glEnable(GL_ALPHA_TEST)
        glDisable(GL_BLEND)
    def draw_scenery(self):
        glClearColor(.3,.42,.63, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        if self.pan_background != None:
            upper_stretch = 0#HOW MUCH OF THE IMAGE WILL BE STRETCHED
            lower_stretch = .1#HOW MUCH OF THE IMAGE WILL BE STRETCHED
            
            segments = int(self.properties["scenery_segments"])
            radius = self.properties["scenery_radius"]
            angle = math.pi*2/segments
            
            circumference = segments * (2*radius**2 - 2*radius**2*math.cos(angle))**.5
            
            ratio = circumference/self.pan_background[0].size[0]
            
            drawn_height = ratio*self.pan_background[0].size[1]
            lower_height = self.properties["scenery_lower_stretch"]
            upper_height = 0
            
            vertices = []
            tex_coords = []
            
            for i in range(segments):
                a1 = -angle*(i) + self.properties["scenery_angle"]
                a2 = -angle*(i+1) + self.properties["scenery_angle"]
                x1 = math.cos(a1)*radius + self.get_width_floors()*self.properties["horizontal_stretch"]/2
                z1 = -math.sin(a1)*radius + self.get_height_floors()*self.properties["horizontal_stretch"]/2
                x2 = math.cos(a2)*radius + self.get_width_floors()*self.properties["horizontal_stretch"]/2
                z2 = -math.sin(a2)*radius + self.get_height_floors()*self.properties["horizontal_stretch"]/2
                
                
                vertices.append([x1,self.properties["scenery_height"] + drawn_height*(1-upper_stretch) - drawn_height/2,z1])
                vertices.append([x2,self.properties["scenery_height"] + drawn_height*(1-upper_stretch) - drawn_height/2,z2])
                vertices.append([x2,self.properties["scenery_height"] + -drawn_height*(1-lower_stretch) + drawn_height/2,z2])
                vertices.append([x1,self.properties["scenery_height"] + -drawn_height*(1-lower_stretch) + drawn_height/2,z1])
                
                tex_coords.append([i/segments,1-upper_stretch])
                tex_coords.append([(i+1)/segments,1-upper_stretch])
                tex_coords.append([(i+1)/segments,lower_stretch])
                tex_coords.append([i/segments,lower_stretch])
                
                if lower_height > drawn_height/2:
                    
                    
                    vertices.append([x1,self.properties["scenery_height"] + -drawn_height*(1-lower_stretch) + drawn_height/2,z1])
                    vertices.append([x2,self.properties["scenery_height"] + -drawn_height*(1-lower_stretch) + drawn_height/2,z2])
                    vertices.append([x2,self.properties["scenery_height"] + -lower_height,z2])
                    vertices.append([x1,self.properties["scenery_height"] + -lower_height,z1])
                
                    tex_coords.append([i/segments,lower_stretch])
                    tex_coords.append([(i+1)/segments,lower_stretch])
                    tex_coords.append([(i+1)/segments,0])
                    tex_coords.append([i/segments,0])
                
            
            def setup():
                gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), 50, 99999)
                try:
                    glRotate(rad_to_deg(-(self.view.hor_rot-math.pi/2)), 0, 1, 0)
                    glRotate(rad_to_deg(-self.view.vert_rot), math.cos(self.view.hor_rot - math.pi/2), 0, -math.sin(self.view.hor_rot - math.pi/2))
                    glTranslate(-self.view.x, -self.view.y, -self.view.z)
                except Exception as e:
                    pass
            
            
            self.draw_image_array_3d(vertices, tex_coords, self.pan_background[0], self.pan_background[1],setup_3d=setup)
            glClear(GL_DEPTH_BUFFER_BIT)
    
    
    
    def altitude_sickness(self):
        if not constants["do_shadow_updates"]:
            return
        hr = self.properties["horizontal_stretch"]
        cz = int(self.view.z/hr/self.properties["chunk_size"])#center chunk z
        cx = int(self.view.x/hr/self.properties["chunk_size"])#center chunk x
        
        shadow_load_radius = int(constants["tree_shadow_load_radius"]*self.view.line_of_sight)
        
        
        
        
        """
        for chunk_z in range(cz-shadow_load_radius, cz+shadow_load_radius):
            for chunk_x in range(cx-shadow_load_radius, cx+shadow_load_radius):
                if not self.valid_chunk(chunk_z,chunk_x):continue
                self.chunks[chunk_z][chunk_x].svh.list_mode()
        """
        to_update = []
        
        
        for chunk_z in range(cz-shadow_load_radius, cz+shadow_load_radius):
            for chunk_x in range(cx-shadow_load_radius, cx+shadow_load_radius):
                if not self.valid_chunk(chunk_z,chunk_x):
                    continue
                c = self.chunks[chunk_z][chunk_x]
                if not c.tree_shadows_loaded :
                    c.tree_shadows_loaded = True
                    x1 = chunk_x * self.properties["chunk_size"]
                    z1 = chunk_z * self.properties["chunk_size"]
                    x2 = x1 + self.properties["chunk_size"]
                    z2 = z1 + self.properties["chunk_size"]
                    
                    for z in range(z1,z2):
                        for x in range(x1,x2):
                            q = self.quads[z][x]
                            for containedobj in list(q.containedObjects):
                                if isinstance(containedobj, Tree):
                                    if hasattr(containedobj,"shadow_pointers") and containedobj.shadow_pointers == None:
                                        to_update.append(containedobj)
            
        fast_shadows.add_shadows(self, to_update)
        
        
        
        """
        for chunk_z in range(cz-shadow_load_radius, cz+shadow_load_radius):
            for chunk_x in range(cx-shadow_load_radius, cx+shadow_load_radius):
                if not self.valid_chunk(chunk_z,chunk_x):continue
                self.chunks[chunk_z][chunk_x].svh.numpy_mode()
        """
        
                                    
                    
        
    """
    for each spot in the grid
    
    if it's 
        -2 or -1 chunk is unloaded... only the most blurry background shall be drawn
        0 chunk is "blurry" so you can see trees, lift poles, and rough estimate of ground
        1 chunk is loaded
        2 chunk is loaded and close to player, so draw it in the "near draw
    
    
    
    
    WILL INVOKE SHADOW LOADER if it finds a nearby (status 1 or 2) chunk without shadows
    """
    def get_chunk_load_grid(self):
        los =self.view.line_of_sight
        los2 =self.properties["line_of_sight2"]
        los3 =self.properties["line_of_sight3"]
        
        
        
        chunk_load_grid =[]
        if los3 == -1:
            for r in range(self.get_height_chunks()):
                chunk_load_grid.append([-1]*self.get_width_chunks())
        else:
            for r in range(self.get_height_chunks()):
                chunk_load_grid.append([-2]*self.get_width_chunks())
        
        unscaled_view_z = self.view.z/self.properties["horizontal_stretch"]
        unscaled_view_x = self.view.x/self.properties["horizontal_stretch"]
        
        
        player_z_chunk, player_x_chunk = self.convert_to_chunk_coords(unscaled_view_z, unscaled_view_x)
        
        cs = self.properties["chunk_size"]
        
        
        def nearest_multiple(x, m):
            return int(x/m + .5)*m
        
        view_angle = math.pi*.35
        #far_view_angle = math.pi/6
        far_view_angle = math.pi/4
        
        chunks_out_of_sight = set()
        
        
        
        if los3 != -1:
            for z in range(nearest_multiple(unscaled_view_z - los3*cs, cs), nearest_multiple(unscaled_view_z + los3*cs, cs)+1, cs):
                for x in range(nearest_multiple(unscaled_view_x - los3*cs, cs), nearest_multiple(unscaled_view_x + los3*cs, cs)+1, cs):
                    
                    if not self.valid_point(z, x): continue
                    
                    #here we are testing whether the chunk appears or not
                    if ( (z-unscaled_view_z)**2 + (x-unscaled_view_x)**2 )**.5 <= self.properties["line_of_sight3"]*cs:
                        if far_view_angle > normal.angle_distance(self.view.hor_rot, util.get_angle(unscaled_view_z, unscaled_view_x, z, x)):
                            #then all four neighboring chunks are visible
                            cz = int(z/cs)
                            cx = int(x/cs)
                            
                            if self.valid_chunk(cz, cx): chunk_load_grid[cz][cx] = -1
                            if self.valid_chunk(cz-1, cx-1): chunk_load_grid[cz-1][cx-1] = -1
                            if self.valid_chunk(cz, cx-1): chunk_load_grid[cz][cx-1] = -1
                            if self.valid_chunk(cz-1, cx): chunk_load_grid[cz-1][cx] = -1
                            
        num = 0
        for z in range(nearest_multiple(unscaled_view_z - los2*cs, cs), nearest_multiple(unscaled_view_z + los2*cs, cs)+1, cs):
            for x in range(nearest_multiple(unscaled_view_x - los2*cs, cs), nearest_multiple(unscaled_view_x + los2*cs, cs)+1, cs):
                if not self.valid_point(z, x): continue
                
                #here we are testing whether the chunk at least has trees or not
                if ( (z-unscaled_view_z)**2 + (x-unscaled_view_x)**2 )**.5 <= self.properties["line_of_sight2"]*cs:
                    if far_view_angle > normal.angle_distance(self.view.hor_rot, util.get_angle(unscaled_view_z, unscaled_view_x, z, x)):
                        num += 1
                        #then all four neighboring chunks have trees
                        cz = int(z/cs)
                        cx = int(x/cs)
                        
                        if self.valid_chunk(cz, cx) and chunk_load_grid[cz][cx]<0:
                            if self.in_sight(cz, cx): chunk_load_grid[cz][cx] = 0
                            else: chunks_out_of_sight.add((cz,cx))
                        if self.valid_chunk(cz-1, cx-1) and chunk_load_grid[cz-1][cx-1] < 0: 
                            if self.in_sight(cz-1, cx-1): chunk_load_grid[cz-1][cx-1] = 0
                            else: chunks_out_of_sight.add((cz-1, cx-1))
                        if self.valid_chunk(cz, cx-1) and chunk_load_grid[cz][cx-1] < 0:
                            if self.in_sight(cz, cx-1): chunk_load_grid[cz][cx-1] = 0
                            else: chunks_out_of_sight.add((cz, cx-1))
                        if self.valid_chunk(cz-1, cx) and chunk_load_grid[cz-1][cx] < 0:
                            if self.in_sight(cz-1, cx): chunk_load_grid[cz-1][cx] = 0
                            else: chunks_out_of_sight.add((cz-1, cx))
                       
        #print("checked",num,"points")
        
        
        
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
                        
                        if self.valid_chunk(cz, cx) and chunk_load_grid[cz][cx] == 0:
                            chunk_load_grid[cz][cx] = 1
                        if self.valid_chunk(cz-1, cx-1) and chunk_load_grid[cz-1][cx-1] == 0:
                            chunk_load_grid[cz-1][cx-1] = 1
                        if self.valid_chunk(cz, cx-1) and chunk_load_grid[cz][cx-1] == 0:
                            chunk_load_grid[cz][cx-1] = 1
                        if self.valid_chunk(cz-1, cx) and chunk_load_grid[cz-1][cx] == 0:
                            chunk_load_grid[cz-1][cx] = 1
                        
                        if self.game_ui.clock % constants["altitude_sickness_check_freq"] == 0:
                            #"Altitude sickness"
                            if self.valid_chunk(cz, cx) and not self.chunks[cz][cx].tree_shadows_loaded:
                                self.altitude_sickness()
                            if self.valid_chunk(cz-1, cx-1) and not self.chunks[cz-1][cx-1].tree_shadows_loaded:
                                self.altitude_sickness()
                            if self.valid_chunk(cz, cx-1) and not self.chunks[cz][cx-1].tree_shadows_loaded:
                                self.altitude_sickness()
                            if self.valid_chunk(cz-1, cx) and not self.chunks[cz-1][cx].tree_shadows_loaded:
                                self.altitude_sickness()
                        
                        
        
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
        
        
        #print(self.in_sight(0,0,True))
        self.chunks_out_of_sight = len(chunks_out_of_sight)
        return chunk_load_grid
    
    """
    uses ray tracing to check if a chunk is in sight or not
    """
    def in_sight(self, chunk_z, chunk_x, verbose=False):
        if (chunk_z,chunk_x) in self.chunks_in_sight_memo:
            return self.chunks_in_sight_memo[chunk_z,chunk_x]#dont calculate it AGAIN if we already calculated it
        
        
        hs = self.properties["horizontal_stretch"]
        vs = self.properties["vertical_stretch"]
        
        
        
        #calculate the hr and vr to that chunk
        c_z = (chunk_z+.5) * self.properties["chunk_size"] * hs
        c_x = (chunk_x+.5) * self.properties["chunk_size"] * hs
        c_y = self.get_elevation(int((chunk_z+.5) * self.properties["chunk_size"]), int((chunk_x+.5) * self.properties["chunk_size"]))*vs
        horizontal_dist = ( (self.view.z-c_z)**2 + (self.view.x-c_x)**2 )**.5
        
        aim_higher_than_the_chunk_actually_is = 20#13#cuz then we can just simply ask:
            #if the ray hit somthing, then the chunk isn't visible
            #if the ray didn't hit something, then the chunk is visible
        start_higher_than_you_actually_are = 12#12    
            
        
        
        
        hr = util.get_angle(self.view.z,self.view.x,c_z,c_x)
        vr = normal.get_angle(0,0,horizontal_dist,c_y-(self.view.y+start_higher_than_you_actually_are) + aim_higher_than_the_chunk_actually_is)
        
        
        
        
        
        
        
        #CAST RAY
        
        total_dist = ( (self.view.z-c_z)**2 + (self.view.x-c_x)**2 + (c_y-(self.view.y+start_higher_than_you_actually_are)+aim_higher_than_the_chunk_actually_is)**2 )**.5
        #so if the ray can travel the total_dist, then that means we hit the chunk
        
        
        x=self.view.x
        y=self.view.y+start_higher_than_you_actually_are
        z=self.view.z
        hr=hr
        vr=vr
        max_dist = total_dist
        step_size=self.properties["chunk_size"]*.8#IN UNITS,unscaled (not scaled distance)
        
        
        max_dist_sq = max_dist**2
        
        
        
        view = self.view
        ray = [x,y,z]
        hs = self.properties["horizontal_stretch"]
        
        
        ray_step_x = step_size*hs * math.cos(hr) * math.cos(vr)
        ray_step_y = step_size*hs * math.sin(vr)
        ray_step_z = step_size*hs * -math.sin(hr) * math.cos(vr)#this is a step
        num_steps = 1
        while True:
            #if ( (ray[0]-view.x)**2 + (ray[2]-view.z)**2 + (ray[1]-view.y)**2) > max_dist_sq:#if ray travelled max distance
            if num_steps*step_size*hs > max_dist:#if ray travelled max distance
                self.chunks_in_sight_memo[chunk_z,chunk_x] = True
                return True
            grid_x = int(ray[0] / hs)
            grid_z = int(ray[2] / hs)
            
            if grid_x >= self.get_width_floors()-1 or grid_z >= self.get_height_floors()-1 or grid_x < 0 or grid_z < 0:
                pass#not inside world
            else:
                if ray[1] < self.get_elevation(grid_z, grid_x, scaled=True):
                    if verbose:print("hit",grid_z,grid_x)
                    self.chunks_in_sight_memo[chunk_z,chunk_x] = False
                    return False
                
                
            ray[0] += ray_step_x
            ray[2] += ray_step_z
            ray[1] += ray_step_y
            
            num_steps += 1
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #END CAST RAY
        
        res = ray
        
        #print(hr,vr,res)
        
        if res == None:
            return False
        grid_z,grid_x = res
        hit_chunk_z,hit_chunk_x = self.convert_to_chunk_coords(grid_z,grid_x)
        
        if (chunk_z,chunk_x) == (hit_chunk_z,hit_chunk_x):
            return True
        return False
        
        
        
        
        
        
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
        
        
        
        mobile_vertices_close = numpy.array(self.mobile_vertices_close)
        mobile_colors_close = numpy.array(self.mobile_colors_close)
        mobile_vertices_far = numpy.array(self.mobile_vertices_far)
        mobile_colors_far = numpy.array(self.mobile_colors_far)
        
        self.mobile_vertices_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_vertices_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        #Timing
        start = time()
        
        height = len(chunk_load_grid)
        width = 0 if height == 0 else len(chunk_load_grid[0])
        
        #just check that the dimensions of the chunk load grid are same as self.chunks matrix
        check(height == self.properties["height_chunks"] and width == self.properties["width_chunks"], "Dimensions of chunk_load_grid were %d %d but should have been %d %d" % (width, height, self.properties["width_chunks"], self.properties["height_chunks"]))
        
        #add all the chunks' vertexes and colors here (if the chunk load grid is a 1)
        
        
        #NEAR DRAW
        vertices_draw = [mobile_vertices_close]
        colors_draw = [mobile_colors_close]
        tex_vertices_draw = []
        tex_coords_draw = []
        shadow_vertices_draw = []
        shadow_colors_draw = []
        
        
        #FAR DRAW
        vertices_draw_far = [mobile_vertices_far]
        colors_draw_far = [mobile_colors_far]
        tex_vertices_draw_far = []
        tex_coords_draw_far = []
        shadow_vertices_draw_far = []
        shadow_colors_draw_far = []
        
        pan_chunk_vertices = []
        pan_chunk_colors = []
        
        
        
        
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
                    
                    #print("chunk",z,x,"num occupied",self.chunks[z][x].tvh.num_occupied(), "capacity", self.chunks[z][x].tvh.capacity())
                    
                    if hasattr(self.chunks[z][x],"svh") and constants["do_shadows"]:
                        shadow_vertices_draw.append(self.chunks[z][x].svh.vertices)
                        shadow_colors_draw.append(self.chunks[z][x].svh.vertex_colors)
                elif chunk_load_grid[z][x] == 1:
                    #add this chunk's vertices and colors to the stuff that's gonna be drawn
                    vertices_draw_far.append(self.chunks[z][x].vh.vertices)
                    colors_draw_far.append(self.chunks[z][x].vh.vertex_colors)
                    
                    tex_vertices_draw_far.append(self.chunks[z][x].tvh.vertices)
                    tex_coords_draw_far.append(self.chunks[z][x].tvh.vertex_colors)
                    
                    if hasattr(self.chunks[z][x],"svh") and constants["do_shadows"]:
                        shadow_vertices_draw_far.append(self.chunks[z][x].svh.vertices)
                        shadow_colors_draw_far.append(self.chunks[z][x].svh.vertex_colors)
                    
                elif chunk_load_grid[z][x] == 0:
                    pcsquares = self.chunks[z][x].get_pan_chunk_squares(z, x)
                    #vertices_draw_far.append(pcsquares.vertices)
                    #colors_draw_far.append(pcsquares.vertex_colors)
                    pan_chunk_vertices.append(pcsquares.vertices)
                    pan_chunk_colors.append(pcsquares.vertex_colors)
                elif chunk_load_grid[z][x] == -1:
                    #pcsquares = self.chunks[z][x].get_pan_chunk_squares(z, x, trees=False)
                    #vertices_draw_far.append(pcsquares.vertices)
                    #colors_draw_far.append(pcsquares.vertex_colors)
                    #dont need these because all pan chunk squares are already all drawn all together
                    pass
                elif chunk_load_grid[z][x] == -2:
                    pass
                    
        
        
        #print("setting up took " + str(time()-start) + " seconds")
        
        #glAlphaFunc(GL_GREATER, 0.4);
        #glEnable(GL_ALPHA_TEST);
       
        start = time()
        
        #now here's where we do all the drawing (and stacking)
        
        #shadow_vertices_draw_far + vertices_draw_far
        
        self.num_vertices_drawn = (
        
        len(self.pan_chunk_squares["verts"]) + 
        sum([len(x) for x in pan_chunk_vertices]) +
        sum([len(x) for x in shadow_vertices_draw_far]) + 
        sum([len(x) for x in vertices_draw_far]) + 
        sum([len(x) for x in shadow_vertices_draw]) + 
        sum([len(x) for x in vertices_draw]) + 
        sum([len(x) for x in tex_vertices_draw]) + 
        sum([len(x) for x in tex_vertices_draw_far])
        
        )
        if self.properties["allow_shadow_hiding"] and (self.far_shadows == True) and self.num_vertices_drawn > constants["turn_shadows_off_threshold"]:
            self.far_shadows = False
        elif self.far_shadows == False and self.num_vertices_drawn < constants["turn_shadows_on_threshold"]:
            self.far_shadows = True
        
        if self.far_shadows == False:
            self.num_vertices_drawn = (#recalculate without far shadows
    
            
            len(self.pan_chunk_squares["verts"]) + 
            sum([len(x) for x in pan_chunk_vertices]) +
            
            sum([len(x) for x in vertices_draw_far]) + 
            sum([len(x) for x in shadow_vertices_draw]) + 
            sum([len(x) for x in vertices_draw]) + 
            sum([len(x) for x in tex_vertices_draw]) + 
            sum([len(x) for x in tex_vertices_draw_far])
            
            )
        
        
        #FAR DRAW
        
        #CHUNK DRAW
        
        if True:#draw pan chunk floors
            glDisable(GL_ALPHA_TEST);
            self.draw_quad_array_3d(self.pan_chunk_squares["verts"], self.pan_chunk_squares["colors"], setup_3d=self.get_setup_3d_super_far_chunk_draw())
            glEnable(GL_ALPHA_TEST);
            
        glClear(GL_DEPTH_BUFFER_BIT)
        if len(pan_chunk_vertices) > 0:#draw pan chunk everything else
            glDisable(GL_ALPHA_TEST);
            pan_chunk_vertices = numpy.vstack(pan_chunk_vertices)
            pan_chunk_colors = numpy.vstack(pan_chunk_colors)
            self.draw_quad_array_3d(pan_chunk_vertices, pan_chunk_colors, setup_3d=self.get_setup_3d_chunk_draw())
            glEnable(GL_ALPHA_TEST);
        
        glClear(GL_DEPTH_BUFFER_BIT)
        
        #END CHUNK DRAW
        
        
        if self.far_shadows:
            vertices_draw_far = numpy.vstack(shadow_vertices_draw_far + vertices_draw_far)
            colors_draw_far = numpy.vstack(shadow_colors_draw_far + colors_draw_far)
            self.draw_quad_array_3d(vertices_draw_far, colors_draw_far, setup_3d=self.get_setup_3d_far())
        else:
            vertices_draw_far = numpy.vstack(vertices_draw_far)
            colors_draw_far = numpy.vstack(colors_draw_far)
            self.draw_quad_array_3d(vertices_draw_far, colors_draw_far, setup_3d=self.get_setup_3d_far())
        
        
        if len(tex_vertices_draw_far) > 0:
            _start=time()###
            tex_vertices_draw_far = numpy.vstack(tuple(tex_vertices_draw_far))
            tex_coords_draw_far = numpy.vstack(tuple(tex_coords_draw_far))
            #print("Stacking took %f secs" % (time()-_start,))###
            _start=time()###
            #self.draw_image_array_3d(tex_vertices_draw_far, tex_coords_draw_far, texture.tex, texture.tex_b, setup_3d=self.get_setup_3d_far())
            self.draw_tex(tex_vertices_draw_far, tex_coords_draw_far, self.get_setup_3d_far())
            #print("Drawing took %f secs" % (time()-_start,))###
        
        
        #END FAR DRAW
        
        glClear(GL_DEPTH_BUFFER_BIT)
        
        """
        print("start")
        for a in shadow_vertices_draw + vertices_draw:
            print(a.dtype)
        print("stop")
        """
        
        
        #NEAR DRAW
        vertices_draw = numpy.vstack(tuple(shadow_vertices_draw + vertices_draw))
        colors_draw = numpy.vstack(tuple(shadow_colors_draw + colors_draw))
        self.draw_quad_array_3d(vertices_draw, colors_draw, setup_3d=self.get_setup_3d_close())
        
        if len(tex_vertices_draw) > 0:
            _start=time()###
            tex_vertices_draw = numpy.vstack(tuple(tex_vertices_draw))
            tex_coords_draw = numpy.vstack(tuple(tex_coords_draw))
            #print("Stacking took %f secs" % (time()-_start,))###
            #print(tex_vertices_draw.dtype)
            _start=time()###
            #self.draw_image_array_3d(tex_vertices_draw, tex_coords_draw, texture.tex, texture.tex_b, setup_3d=self.get_setup_3d_close())
            self.draw_tex(tex_vertices_draw, tex_coords_draw, self.get_setup_3d_close())
            #print("Drawing took %f secs" % (time()-_start,))###


        if constants["draw_snow_tex"]:
            self.draw_snow_tex()
        self.draw_tex([],[],self.get_setup_3d_close())
        
        #print("drawing took " + str(time()-start) + " seconds")
        num_vertices_drawn_check = len(tex_vertices_draw)+len(vertices_draw)+len(tex_vertices_draw_far)+len(vertices_draw_far)+len(pan_chunk_vertices)+len(self.pan_chunk_squares["verts"])
        
        
        if self.num_vertices_drawn != num_vertices_drawn_check:
            print("Incorrect!",self.num_vertices_drawn,"!=",num_vertices_drawn_check)
        
        #print(self.get_my_window().layered_looi_objects)
        glClear(GL_DEPTH_BUFFER_BIT)
        
        
        
        
        self.draw_quad_array_2d(self.particle_handler.vertices, self.particle_handler.vertex_colors)
        
        
        
        
        return#######################
    def draw_tex(self, vertices, texture_coords, setup_3d, mipmap=True, blend = False):
        glPushMatrix()
        
        image = texture.tex
        
        ix, iy = image.size[0], image.size[1]
        
        image = texture.tex_b
        
        ID = texture.texture_id
        
        
        glEnable(GL_TEXTURE_2D)
        if blend: glEnable(GL_BLEND)
        if blend: glDisable(GL_ALPHA_TEST)
        
        if mipmap or True: glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, self.get_my_window().mipmap_max_level)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)#USED TO BE GL_NEAREST
        if mipmap: glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)#USED TO BE GL_NEAREST 
        else: glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        
        
        setup_3d()
        if mipmap or True:
            glGenerateMipmap(GL_TEXTURE_2D)
        
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_TEXTURE_COORD_ARRAY);
        
        glVertexPointerf(vertices);
        glTexCoordPointerf(texture_coords);
        glDrawArrays(GL_QUADS, 0, len(vertices));
        
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_TEXTURE_COORD_ARRAY);
        
        if blend: glDisable(GL_BLEND)
        if blend: glEnable(GL_ALPHA_TEST)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
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
        
        
        chunk_z = int( (vertex1[2]/self.properties["horizontal_stretch"])/self.properties["chunk_size"] )
        chunk_x = int( (vertex1[0]/self.properties["horizontal_stretch"])/self.properties["chunk_size"] )
        if (
            chunk_z >= 0 and chunk_z < len(self.chunk_load_grid) and 
            chunk_x >= 0 and chunk_x < len(self.chunk_load_grid[0]) and
            self.chunk_load_grid[chunk_z][chunk_x] == 2
            ):
            v = self.mobile_vertices_close
            c = self.mobile_colors_close
        else:
            v = self.mobile_vertices_far
            c = self.mobile_colors_far
        v.append(vertex1)
        v.append(vertex2)
        v.append(vertex3)
        v.append(vertex4)
        if isinstance(color, Color):
            color = color.to_tuple()
            c.append(color)
            c.append(color)
            c.append(color)
            c.append(color)
        elif type(color) == type([]):
            for i in range(4):
                c.append(color)
        elif type(color) == type(()):
            for i in range(4):
                c.append(color[i])
    
    
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
        
        self.chunks[chunk_z][chunk_x].changed()
        
        
        if object != None:
            self.quads[anchor_z][anchor_x].containedObjects.append(object)

        return ret
        
    def remove_fixed_quad(self, quad_id, anchor_z, anchor_x, object=None):
        if self.disable_remove_fixed_quads: return
        chunk_z, chunk_x = self.convert_to_chunk_coords(anchor_z, anchor_x)
        
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id)
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id+1)
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id+2)
        self.chunks[chunk_z][chunk_x].vh.rm_vertex(quad_id+3)
        
        self.chunks[chunk_z][chunk_x].changed()
        
        if object != None:
            self.quads[anchor_z][anchor_x].containedObjects.remove(object)
    def add_shadow(self, vertex1, vertex2, vertex3, vertex4, color, anchor_z, anchor_x, object=None):
        
        chunk_z, chunk_x = self.convert_to_chunk_coords(anchor_z, anchor_x)
        
        if isinstance(color, list):
            ret = self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex1, color)
            self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex2, color)
            self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex3, color)
            self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex4, color)
        elif isinstance(color, tuple):
            ret = self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex1, color[0])
            self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex2, color[1])
            self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex3, color[2])
            self.chunks[chunk_z][chunk_x].svh.add_vertex(vertex4, color[3])
        
        self.chunks[chunk_z][chunk_x].changed()
        
        if object != None:
            self.quads[anchor_z][anchor_x].containedObjects.append(object)

        return ret
        
    def remove_shadow(self, quad_id, anchor_z, anchor_x, object=None):
        if self.disable_remove_fixed_quads: return
        chunk_z, chunk_x = self.convert_to_chunk_coords(anchor_z, anchor_x)
        
        self.chunks[chunk_z][chunk_x].svh.rm_vertex(quad_id)
        self.chunks[chunk_z][chunk_x].svh.rm_vertex(quad_id+1)
        self.chunks[chunk_z][chunk_x].svh.rm_vertex(quad_id+2)
        self.chunks[chunk_z][chunk_x].svh.rm_vertex(quad_id+3)
        
        self.chunks[chunk_z][chunk_x].changed()
        
        if object != None:
            self.quads[anchor_z][anchor_x].containedObjects.remove(object)
    def get_view_pointing(self):
        return self.cast_ray(self.view.x, self.view.y, self.view.z, self.view.hor_rot, self.view.vert_rot, self.view.line_of_sight*self.properties["chunk_size"]*self.properties["horizontal_stretch"] + 2)
    def cast_ray(self, x,y,z,hr,vr,max_dist,step_size=.5):
        view = self.view
        ray = [x,y,z]
        while True:
            if ( (ray[0]-view.x)**2 + (ray[2]-view.z)**2 ) ** .5 > max_dist:
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
                #highest = max(four_corners) + step_size*self.properties["horizontal_stretch"]
                highest = max(four_corners) 
                #lowest = min(four_corners) - step_size*self.properties["horizontal_stretch"]*3
                #if ray[1] <= highest and ray[1] >= lowest: 
                if ray[1] <= highest:
                    return grid_z, grid_x
                
            ray[0] += step_size*self.properties["horizontal_stretch"] * math.cos(hr) * math.cos(vr)
            ray[2] += step_size*self.properties["horizontal_stretch"] * -math.sin(hr) * math.cos(vr)
            ray[1] += step_size*self.properties["horizontal_stretch"] * math.sin(vr)
    def convert_to_gworld(self):
        self.list_mode()
        
        
        
        
        
        
        all_contained_objects = []
        all_lifts = []
        for z in range(self.get_height_floors()):
            for x in range(self.get_width_floors()):
                for obj in self.quads[z][x].containedObjects:
                    if isinstance(obj, WorldObject) and not isinstance(obj, NaturalBump):#copy everything but the natural bumps and lifts
                        all_contained_objects.append(obj)
                    elif isinstance(obj, lift.Terminal):
                        if obj.chairlift not in all_lifts:
                            all_lifts.append(obj.chairlift)
                        
                        
                        
        import gworld
        world2 = gworld.GWorld()
        world2.properties = dict(self.properties)
        #print("Starting init")
        
        world2.init(self.properties["name"], self.properties["width"], self.properties["height"], view=self.view, elevation_function=lambda z,x:self.get_elevation(z,x),natural_bumps=False)

        
        
        world2.disable_remove_fixed_quads = True#because all the objects' quads have already been removed because we cleaned out everything, so if they try to remove again it'll just error
        world_operations.natural_bumps(world2, 0,0,world2.get_height_points(), world2.get_width_points(), prog_bar=True)#re add the natural bumps here

        world2.reset_objects(all_contained_objects, trees_dont_remove_shadow=True)
        
        
        
        
        lifts_reset = []#make sure no duplicate lifts get away!
        
        for l in list(all_lifts): 
            if ((l.z1,l.x1,l.z2,l.x2) not in lifts_reset) and ((l.z2,l.x2,l.z1,l.x1) not in lifts_reset):
                l.world=world2
                l.reset()
                lifts_reset.append((l.z1,l.x1,l.z2,l.x2))
            else:
                l.delete()
        
        
        world2.disable_remove_fixed_quads = False
        
        world2.pan_chunk_squares_changed = True
        
        return world2
    def reset(self, new_chunk_size = None, new_vertical_stretch = None):
        self.list_mode()
        
        if new_chunk_size == None: new_chunk_size = self.properties["chunk_size"]
        if new_vertical_stretch == None: new_vertical_stretch = self.properties["vertical_stretch"]
        
        
        old_chunk_size = self.properties["chunk_size"]
        old_vertical_stretch = self.properties["vertical_stretch"]
        
        
        self.properties["chunk_size"] = new_chunk_size
        self.properties["vertical_stretch"] = new_vertical_stretch
        
        
        
        
        all_contained_objects = []
        for z in range(self.get_height_floors()):
            for x in range(self.get_width_floors()):
                for obj in self.quads[z][x].containedObjects:
                    if isinstance(obj, WorldObject) and not isinstance(obj, NaturalBump):#copy everything but the natural bumps and lifts
                        all_contained_objects.append(obj)
                        
                        
                        
        import gworld
        world2 = gworld.GWorld()
        world2.properties = dict(self.properties)
        #print("Starting init")
        
        self.properties["vertical_stretch"] = old_vertical_stretch
        self.properties["chunk_size"] = old_chunk_size
        world2.init(self.properties["name"], self.properties["width"], self.properties["height"], view=self.view, elevation_function=lambda z,x:self.get_elevation(z,x),natural_bumps=False)
        self.properties["chunk_size"] = new_chunk_size
        self.properties["vertical_stretch"] = new_vertical_stretch
        
        
        #print("Finishing init")
        
        self.properties = world2.properties
        
        self.quads = world2.quads
        self.chunks = world2.chunks
        self.shadow_map = world2.shadow_map
        
        self.disable_remove_fixed_quads = True#because all the objects' quads have already been removed because we cleaned out everything, so if they try to remove again it'll just error
        world_operations.natural_bumps(self, 0,0,self.get_height_points(), self.get_width_points(), prog_bar=True)#re add the natural bumps here

        self.reset_objects(all_contained_objects, trees_dont_remove_shadow=True)
        
        
        
        
        lifts_reset = []#make sure no duplicate lifts get away!
        
        for l in list(lift.active_lifts): 
            if ((l.z1,l.x1,l.z2,l.x2) not in lifts_reset) and ((l.z2,l.x2,l.z1,l.x1) not in lifts_reset):
                l.reset()
                lifts_reset.append((l.z1,l.x1,l.z2,l.x2))
            else:
                l.delete()
        
        
        self.disable_remove_fixed_quads = False
        
        self.game_ui.restart_shadow_search = True
        
        self.pan_chunk_squares_changed = True
    def reset_objects(self, objects_list, trees_dont_remove_shadow = False):
        
        do_loading = len(objects_list) > 150
        
        objects_list = list(objects_list)
        
        total_progress = len(objects_list)
        
        if do_loading:
            loading_update = int(total_progress/150)
            if loading_update < 1:loading_update = 1
        
            loading.progress_bar("Loading objects...")
    
        i=0
        trees = []
        if trees_dont_remove_shadow:    
            for obj in objects_list:
                obj.args["world"] = self
                if isinstance(obj,Tree): 
                    obj.args["remove_shadow"]=False
                    newobj = obj.reset()
                    if hasattr(newobj,"args"):
                        newobj.args["remove_shadow"]=True
                else:
                    obj.reset()
                
                if do_loading:
                    if i%loading_update == 0:
                        loading.update(i/total_progress*100)
                i+=1
        else:
            for obj in objects_list:
                obj.args["world"] = self
                obj.reset()
                
                if do_loading:
                    if i%loading_update == 0:
                        loading.update(i/total_progress*100)
                i+=1
        
        if do_loading:
            loading.update(100)
    
    
    
    ########################################
    #READ MODE WRITE MODE
    ##################################
    
    def numpy_mode(self):
        for z in range(self.get_height_chunks()):
            for x in range(self.get_width_chunks()):
                chunk = self.chunks[z][x]
                res = chunk.vh.numpy_mode()
                chunk.tvh.numpy_mode()
                
                
                if res == False: return#false means no change, so we're already in the right mode
                
    def list_mode(self):
        for z in range(self.get_height_chunks()):
            for x in range(self.get_width_chunks()):
                chunk = self.chunks[z][x]
                res = chunk.vh.list_mode()
                chunk.tvh.list_mode()
                
                if res == False: return#false means no change, so we're already in the right mode
def rad_to_deg(radians):
    return radians/(2*math.pi) * 360
def round(x):
    return int(x + .5)


def abs(x):return x if x >= 0 else -x


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


def range_float(start, stop, step):
                x = start
                while x < stop:
                    yield x
                    x += step

'''Old chunk load grid loop before debug
for z in range(height):
            for x in range(width):
                #if the chunk load grid says that the chunk should be loaded
                if chunk_load_grid[z][x] == 2:
                    
                    #add this chunk's vertices and colors to the stuff that's gonna be drawn
                    vertices_draw.append(self.chunks[z][x].vh.vertices)
                    colors_draw.append(self.chunks[z][x].vh.vertex_colors)
                    
                    tex_vertices_draw.append(self.chunks[z][x].tvh.vertices)
                    tex_coords_draw.append(self.chunks[z][x].tvh.vertex_colors)
                    
                    #print("chunk",z,x,"num occupied",self.chunks[z][x].tvh.num_occupied(), "capacity", self.chunks[z][x].tvh.capacity())
                    
                    if hasattr(self.chunks[z][x],"svh"):
                        shadow_vertices_draw.append(self.chunks[z][x].svh.vertices)
                        shadow_colors_draw.append(self.chunks[z][x].svh.vertex_colors)
                    
                elif chunk_load_grid[z][x] == 1:
                    #add this chunk's vertices and colors to the stuff that's gonna be drawn
                    vertices_draw_far.append(self.chunks[z][x].vh.vertices)
                    colors_draw_far.append(self.chunks[z][x].vh.vertex_colors)
                    
                    tex_vertices_draw_far.append(self.chunks[z][x].tvh.vertices)
                    tex_coords_draw_far.append(self.chunks[z][x].tvh.vertex_colors)
                    
                    if hasattr(self.chunks[z][x],"svh"):
                        shadow_vertices_draw_far.append(self.chunks[z][x].svh.vertices)
                        shadow_colors_draw_far.append(self.chunks[z][x].svh.vertex_colors)
                    
                elif chunk_load_grid[z][x] == 0:
                    pcsquares = self.chunks[z][x].get_pan_chunk_squares(z, x)
                    #vertices_draw_far.append(pcsquares.vertices)
                    #colors_draw_far.append(pcsquares.vertex_colors)
                    pan_chunk_vertices.append(pcsquares.vertices)
                    pan_chunk_colors.append(pcsquares.vertex_colors)
                elif chunk_load_grid[z][x] == -1:
                    #pcsquares = self.chunks[z][x].get_pan_chunk_squares(z, x, trees=False)
                    #vertices_draw_far.append(pcsquares.vertices)
                    #colors_draw_far.append(pcsquares.vertex_colors)
                    #dont need these because all pan chunk squares are already all drawn all together
                    pass
                elif chunk_load_grid[z][x] == -2:
                    pass
'''
