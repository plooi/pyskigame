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


arr_155_255 = [x for x in range(155, 256, 4)]
arr_155_255.reverse()


#improves performance. 
def conv_155_255(x):
    if x > 1 or x < 0: raise Exception()
    x = int(x*63)*4+3
    if x < 155:
        x = 155
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
        self.line_of_sight = 7 #IN NUMBER OF CHUNKS (not opengl space) #the radius
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
        self.pan_chunk_square_pointer = -1 #pointer to it's chunk square location in the "vertex buffer for all chunk squares" (None if not added)
        
        self.world = world
        
        self.colors_changed = False
        self.last_pan_chunk_color = [0,0,0]
    """
    get_pan_chunk_square
    
    Uses the quads grid to find out what the dimensions and color of the pan chunk 
    square are. Generates a new return value on each call
    
    returns ([x1,y1,z1], [x2,y2,z2], [x3,y3,z3], [x4,y4,z4], [r,g,b]) representing
    the pan chunk square. 
    
    
    """
    def get_pan_chunk_square(self, chunk_z, chunk_x):
        cs = self.world.properties["chunk_size"]
        ul_z = chunk_z * cs
        ul_x = chunk_x * cs
        s = self.world.properties["horizontal_stretch"]
        
        if self.colors_changed:
            #if the floor tile colors have changed since last time we calculated the pan chunk square
            #recalculate a new pan chunk square color
            new_pan_chunk_color = [0,0,0]
            self.colors_changed = False
            
            
            
            total_quads = 0
            
            for r in range(ul_z, ul_z+cs):
                for c in range(ul_x, ul_x+cs):
                    for obj in self.world.quads[r][c].containedObjects:
                        if obj.__class__ == Tree:
                            new_pan_chunk_color[0] += .3*8
                            new_pan_chunk_color[1] += .5*8
                            new_pan_chunk_color[2] += .19*8
                            
                            total_quads+=8
            for r in range(ul_z, ul_z+cs):
                for c in range(ul_x, ul_x+cs):
                    floor_shade = self.world.get_proper_floor_color(r, c)[0]
                    new_pan_chunk_color[0] += floor_shade*.97
                    new_pan_chunk_color[1] += floor_shade
                    new_pan_chunk_color[2] += floor_shade
                    
                    total_quads += 1
            new_pan_chunk_color[0] /= total_quads
            new_pan_chunk_color[1] /= total_quads
            new_pan_chunk_color[2] /= total_quads
            self.last_pan_chunk_color = new_pan_chunk_color
        return (
                [ul_x*s, self.world.get_elevation(ul_z, ul_x, scaled=True), ul_z*s], 
                [(ul_x+cs)*s, self.world.get_elevation(ul_z, ul_x+cs, scaled=True), ul_z*s], 
                [(ul_x+cs)*s, self.world.get_elevation(ul_z+cs, ul_x+cs, scaled=True), (ul_z+cs)*s], 
                [ul_x*s, self.world.get_elevation(ul_z+cs, ul_x, scaled=True), (ul_z+cs)*s], 
                self.last_pan_chunk_color
                )
    
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
            "chunk_size" : 8,
            "width" : -1,
            "height" : -1,
            "width_chunks" : -1,
            "height_chunks" : -1,
            "horizontal_stretch" : 2,
            "vertical_stretch" : .15,
            "sun_angle" : 0,
            "background_color" : Color(.7,.7,1),
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
            "chair_time_distance_fixed" : 390, #in terms of ticks
            "build_chair_pole_distance(map_editor)" : 23, #in real distance
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
        
        
        #used to tell opengl to draw our objects from the proper angles
        self.setup_3d = None
        
    
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
        
        
        
        """
        setup_3d
        
        used to tell opengl to draw our objects from the proper angles
        """
        
        self.setup_3d = self.get_setup_3d()
        
        #initialize the natural bumps
        if prog_bar: loading.update(100)
        world_operations.natural_bumps(self, 0,0,self.get_width_points(), self.get_width_points(), prog_bar=True)
        
        
        return self
        #END INIT
    def get_setup_3d(self):
        def setup_3d():
            gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), .5, 6000 )
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
    def set_floor_texture(self, floor_z, floor_x, texture_str):
        check(self.valid_floor(floor_z, floor_x))
        
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        texture.set_texture(chunk.tvh, floor.floor_pointer, texture_str)
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
        #cut short here
        return color1
        ##BUTT! Although it loads faster now, it will have just a bit less shading accuracy especially on those non-planar quads
        
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
        extremity = .5
        
        color_value = neutral_floor_color + inverse_angle_distance_from_sun_m1_to_p1*inverse_vertical_rotation_0_to_1*extremity
        
        if color_value > 1: color_value = 1
        if color_value < 0: color_value = 0
        
        
        #color_value = stretch(color_value, .2, .89)
        color_value = color_value**.7
        color_value = stretch(color_value, .6, 1)
        
        return color_value
    def is_ice(self, z, x, hr=None, vr=None):
        return False
        if not self.valid_floor(z, x):
            return False
        hs = self.properties["horizontal_stretch"]
        vs = self.properties["vertical_stretch"]
        
        seed = (  math.sin((10*int((z*hs)/35))**2) + math.sin((12*int((x*hs)/35))**2)  )/2
        seed2 = (  math.sin((12*int((z*hs)/35))**2) + math.sin((6*int((x*hs)/35))**2)  )/2
        seed3 = (  math.sin((20*int((z*hs)/35))**2) + math.sin((17*int((x*hs)/35))**2)  )/2
        if not(seed < .28 and seed > -.28):return False
        
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
        #draw sky
        self.draw_rect(0,0,self.get_my_window().get_internal_size()[0],self.get_my_window().get_internal_size()[1], self.properties["background_color"])
        glClear(GL_DEPTH_BUFFER_BIT)
        
        self.draw(self.get_chunk_load_grid())
        self.draw_mobile()
        
        
        glClear(GL_DEPTH_BUFFER_BIT)#clear the depth buffer bit so that the 2d stuff renders on top
        pylooiengine.main_window.draw_borders()
        
        
        
        
        
    def get_chunk_load_grid(self):
        chunk_load_grid =[]
        for r in range(self.get_height_chunks()):
            chunk_load_grid.append([0]*self.get_width_chunks())
        
        unscaled_view_z = self.view.z/self.properties["horizontal_stretch"]
        unscaled_view_x = self.view.x/self.properties["horizontal_stretch"]
        
        
        player_z_chunk, player_x_chunk = self.convert_to_chunk_coords(unscaled_view_z, unscaled_view_x)

        
        for r in range(player_z_chunk - self.view.line_of_sight, player_z_chunk + self.view.line_of_sight):
            for c in range(player_x_chunk - self.view.line_of_sight, player_x_chunk + self.view.line_of_sight):
                if self.valid_chunk(r, c):
                    if ( (r-player_z_chunk) ** 2 + (c-player_x_chunk) ** 2 ) ** .5 <= self.view.line_of_sight:#check that the chunk is within the player's los
                        
                        if (    ( (r-player_z_chunk) ** 2 + (c-player_x_chunk) ** 2 ) ** .5 <= 3#!!!the chunk must either be super close to the player (3 chunks)
                                
                            or
                                
                                math.pi/2 > normal.angle_distance( 
                                                                            normal.get_angle( 
                                                                                unscaled_view_x, 
                                                                                -unscaled_view_z, 
                                                                                (c+.5)*self.properties["chunk_size"], 
                                                                                -(r+.5)*self.properties["chunk_size"] ) , 
                                                                                
                                                                            self.view.hor_rot)#!!!or the player must be looking at the chunk
                                                                            ):
                            try:
                                chunk_load_grid[r][c] = 1
                            except:
                                print("%d, %d out of range of %d, %d" %(r, c, len(chunk_load_grid), len(chunk_load_grid[0])))
        
        return chunk_load_grid
    def draw_mobile(self):
        mobile_vertices = numpy.array(self.mobile_vertices)
        mobile_colors = numpy.array(self.mobile_colors)
        
        
        self.draw_quad_array_3d(mobile_vertices, mobile_colors, setup_3d=self.setup_3d)
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
        
        #if the chunk load grid is not 1, make sure the pan chunk square is added to self.pan_chunk_squares
        
        
        
        #iterate through every single chunk
        for z in range(height):
            for x in range(width):
            
                #if the chunk load grid says that the chunk should be loaded
                if chunk_load_grid[z][x] == 1:
                    
                    #add this chunk's vertices and colors to the stuff that's gonna be drawn
                    vertices_draw.append(self.chunks[z][x].vh.vertices)
                    colors_draw.append(self.chunks[z][x].vh.vertex_colors)
                    
                    tex_vertices_draw.append(self.chunks[z][x].tvh.vertices)
                    tex_coords_draw.append(self.chunks[z][x].tvh.vertex_colors)
                    
                    #if the pan chunk square is showing, get rid of it
                    if self.chunks[z][x].pan_chunk_square_pointer != -1:
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer)
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer+1)
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer+2)
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer+3)
                        self.chunks[z][x].pan_chunk_square_pointer = -1
                else:#if the chunk load grid says to not load that chunk
                    #if the pan chunk square is not added then add it
                    if self.chunks[z][x].pan_chunk_square_pointer == -1:
                        p1,p2,p3,p4,color = self.chunks[z][x].get_pan_chunk_square(z, x)
                        self.chunks[z][x].pan_chunk_square_pointer = self.pan_chunk_squares.add_vertex(p1, color)
                        self.pan_chunk_squares.add_vertex(p2, color)
                        self.pan_chunk_squares.add_vertex(p3, color)
                        self.pan_chunk_squares.add_vertex(p4, color)
                    if self.chunks[z][x].colors_changed:
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer)
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer+1)
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer+2)
                        self.pan_chunk_squares.rm_vertex(self.chunks[z][x].pan_chunk_square_pointer+3)
                        p1,p2,p3,p4,color = self.chunks[z][x].get_pan_chunk_square(z, x)
                        self.chunks[z][x].pan_chunk_square_pointer = self.pan_chunk_squares.add_vertex(p1, color)
                        self.pan_chunk_squares.add_vertex(p2, color)
                        self.pan_chunk_squares.add_vertex(p3, color)
                        self.pan_chunk_squares.add_vertex(p4, color)
        
        
        #add the pan_chunk_squares to all the stuff that's gonna be drawn
        vertices_draw.append(self.pan_chunk_squares.vertices)
        colors_draw.append(self.pan_chunk_squares.vertex_colors)
        
        ###NOW vertices draw and colors draw contain all the static objects we want to draw
        
        vertices_draw = numpy.vstack(tuple(vertices_draw))
        colors_draw = numpy.vstack(tuple(colors_draw))
        self.draw_quad_array_3d(vertices_draw, colors_draw, setup_3d=self.setup_3d)
        if len(tex_vertices_draw) > 0:
            tex_vertices_draw = numpy.vstack(tuple(tex_vertices_draw))
            tex_coords_draw = numpy.vstack(tuple(tex_coords_draw))
            
            #print(vertices_draw)
            
            
            #draw the stuff using opengl
            
            self.draw_image_array_3d(tex_vertices_draw, tex_coords_draw, texture.tex, texture.tex_b, setup_3d=self.setup_3d)
            
        
        return#######################
        
        
        
        #draw textures
        if self.properties["do_floor_textures"]:
            hs = self.properties["horizontal_stretch"]
            vs = self.properties["vertical_stretch"]
            
            offset = .08
            
            pz = self.view.z/hs
            px = self.view.x/hs
            
            radius = max([self.properties["texture_distance"],constants["ice_radius"]/hs]) + 1
            
            
            
            def cap_1(x):return x if x < 1 else 1
            for z in range(round(pz-radius), round(pz+radius)):
                for x in range(round(px-radius), round(px+radius)):
                    dist = ( (z+.5-pz)**2 + (x+.5-px)**2 ) ** .5
                    in_front = normal.angle_distance(util.get_angle(pz, px, z, x), self.view.hor_rot) < math.pi/3
                    if dist <= self.properties["texture_distance"] and self.valid_floor(z, x):#distance
                        
                        if dist < self.properties["texture_radius"] or in_front:#radius
                        
                            shade = self.get_proper_floor_color(z, x)[0]
                            
                            
                            if self.is_ice(z, x):
                                tex = get_ice_texture(shade)
                                self.draw_image_3d(
                                        x*hs, self.get_elevation(z,x,scaled=True) + offset, z*hs,
                                        (x+1)*hs, self.get_elevation(z,x+1,scaled=True) + offset, z*hs,
                                        (x+1)*hs, self.get_elevation(z+1,x+1,scaled=True) + offset, (z+1)*hs,
                                        x*hs, self.get_elevation(z+1,x,scaled=True) + offset, (z+1)*hs,
                                        tex,
                                        setup_3d=self.setup_3d
                                        )
                            
                            
                        
                            
                    elif dist < constants["ice_radius"] and self.is_ice(z, x) and in_front:
                        """
                        quad = self.quads[z][x]
                        chunk = self.chunks[quad.my_chunk_z][quad.my_chunk_x]
                        colors = chunk.vh.vertex_colors
                        shades = [    
                                            colors[quad.floor_pointer][1],
                                            colors[quad.floor_pointer+1][1],
                                            colors[quad.floor_pointer+2][1],
                                            colors[quad.floor_pointer+3][1]]
                        
                        
                        color = constants["ice_color"]
                        colors = ([color.r,color.g,color.b],[color.r,color.g,color.b],[color.r,color.g,color.b],[color.r,color.g,color.b])
                        for i in range(4):
                            factor = shades[i]/color.g
                            colors[i][0] = cap_1(colors[i][0]*factor)
                            colors[i][1] = cap_1(colors[i][1]*factor)
                            colors[i][2] = cap_1(colors[i][2]*factor)
                            
                        """
                        
                        
                        
                        self.add_mobile_quad(
                                    [x*hs, self.get_elevation(z,x,scaled=True) + offset*2, z*hs],
                                    [(x+1)*hs, self.get_elevation(z,x+1,scaled=True) + offset*2, z*hs],
                                    [(x+1)*hs, self.get_elevation(z+1,x+1,scaled=True) + offset*2, (z+1)*hs],
                                    [x*hs, self.get_elevation(z+1,x,scaled=True) + offset*2, (z+1)*hs],
                                    constants["ice_color"]
                                    )
                        
            
        
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











