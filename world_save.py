import world as world_module
from pylooiengine import *
import pylooiengine
from os import path
import os
import traceback
from models import *
import loading
from building import *
from bump import Bump, NaturalBump
from landmark import Landmark
from world_object import *
from mission_center import MissionCenter
from lodge import *
import pickle
import dill
from time import time

from lift import Lift,Terminal#,chair_model_1,chair_model_2,chair_model_3,chair_model_4,rope_model_1,terminal_design_1,pole_design_1


class StringBuffer:
    def __init__(self):
        self.array = []
    def append(self, text):
        self.array.append(str(text))
    def get_string(self):
        return "".join(self.array)





"""
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
self.object_account = {}

self.landmarks = []
"""


#attrs is a list of attr names
def temp_remove(world, attrs):
    ret = {}
    for attr in attrs:
        if hasattr(world, attr):
            ret[attr] = getattr(world, attr)
            delattr(world, attr)
        
    return ret
    
#attrs is a dictionary of attr names and values
def replace(world, attrs):
    for attr in attrs:
        setattr(world, attr, attrs[attr])

"""
write

writes a map editor world to a file
"""
def write(world,old_vertical_stretch=None,writepath="../worlds/", new_version=True):
    if writepath.endswith("/") or writepath.endswith("\\"):
        pass#okay
    else:
        writepath+="/"
    if not path.isdir(writepath):#worlds is for map editor worlds, ./saves is for ski game saves
        os.mkdir(writepath)
    if not path.isdir(writepath+world.properties["name"]):
        os.mkdir(writepath+world.properties["name"])
        
    if new_version:
        #now use pickle
        
        f = open(writepath+world.properties["name"]+"/bin", "wb")
        attrs = temp_remove(world,["game_ui","setup_3d"])
        pickle.dump(world,f)
        replace(world,attrs)
        f.close()   
            
        return
    
    f = open(writepath+world.properties["name"]+"/save", "w")
    
    out = StringBuffer()
    
    
    #step 1: Write all the terrain points to the file
    for r in range(world.get_height_points()):
        for c in range(world.get_width_points()):
            if c > 0:
                out.append(",")
            if old_vertical_stretch == None:
                #vertical stretch hasn't changed
                out.append(world.get_elevation(r, c, scaled=False))
            else:
                #the vertical stretch that is currently in this world's properties cannot correctly return
                #the world back to the proper unscaled values. (because the vertical stretch was changed by user)
                #thus, we must return the world back to its proper unscaled values by 
                #dividing by the old vertical stretch
                out.append(world.get_elevation(r, c, scaled=True) / old_vertical_stretch)
        out.append("\n")
    out.append("WAHLAO EH!\n")
    
    v=world.view
    out.append("World().init(%s, %d, %d, %s, elevation_function, view=new_view(%f,%f,%f,%f,%f,%f,%f,%d,%f))"% ('"'+world.properties["name"]+'"', world.properties["width"], world.properties["height"], property_string(world.properties), v.x,v.y,v.z,v.hor_rot,v.vert_rot,v.speed,v.rot_spd,v.line_of_sight,v.max_vert_rot))
    out.append("\nWAHLAO EH!\n")
    for object_id in world.object_account:
        out.append(world.object_account[object_id])
        out.append("\n")
    
    out.append("WAHLAO EH!")
    f.write(out.get_string())
    f.close()
    
def property_string(properties):
    ret = "{"
    i=0
    for key in properties:
        if i > 0: ret += ","
        ret += '"' + str(key) + '" : '
        if isinstance(properties[key], Color):
            ret += "Color(%f, %f, %f)" % (properties[key].r, properties[key].g, properties[key].b)
        else:
            ret += repr(properties[key])
        i+=1
    ret+="}"
    return ret
        


"""
read

Accepts a path to the directory of a world. Returns a World
object that can be deciphered from that world directory

For map editor worlds
"""
def read(path, new_version = True):
    
    
    
    if new_version:
        if "bin" in os.listdir(path):
            def set_active_variable_false(looiobject):
                looiobject.active=False
                for obj in looiobject.contained_looi_objects:
                    set_active_variable_false(obj)
                    
                    
            #unpickle everything
            f = open(path+"/bin", "rb")
            the_world = pickle.load(f)
            f.close()
            
            for z in range(the_world.get_height_floors()):
                for x in range(the_world.get_width_floors()):
                    for obj in the_world.quads[z][x].containedObjects:
                        
                        if isinstance(obj, Terminal):
                            if obj.top_or_bot == "bot":
                                set_active_variable_false(obj.chairlift)
                                obj.chairlift.reset()
                                
                        elif isinstance(obj, LooiObject):
                            if obj.active:
                                if not isinstance(obj, Landmark):
                                    set_active_variable_false(obj)
                                    obj.activate()
            for landmark in the_world.landmarks:
                set_active_variable_false(landmark)
                landmark.activate()
            set_active_variable_false(the_world)

            #ensure that this world has all the needed properties, for backward compatibility reasons
            example_world = world_module.World()
            for key in example_world.properties:
                if key not in the_world.properties:
                    the_world.properties[key] = example_world.properties[key]
            if not hasattr(the_world, "mobile_vertices_close"):
                the_world.mobile_vertices_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                the_world.mobile_colors_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                the_world.mobile_vertices_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                the_world.mobile_colors_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                    
            #end backward compatibility code
            return the_world
    
    #otherwise do it the old fashioned way
    #no, ALWAYS do it the old fashioned way
    #conservative = good
    
    from world import World,View
    from tree import Tree
    #from lift import Lift#,chair_model_1,chair_model_2,chair_model_3,chair_model_4,rope_model_1,terminal_design_1,pole_design_1
    from rock import Rock
    
    def new_view(x,y,z,hr,vr,spd,rotspd,los,maxvrot):
        v = View()
        v.x = x
        v.y = y
        v.z = z
        v.hor_rot = hr
        v.vert_rot = vr
        v.rot_spd = rotspd
        v.line_of_sight = los
        v.max_vert_rot = maxvrot
        v.speed = spd
        return v
    
    
    
    
    
    
    f = open(path+"/save", "r")
    
    elevations = []
    the_world = None
    
    
    mode = "read_elevations"
    
    objects_to_load = []
    
    for line in f:
        line = line.strip()
        if mode == "read_elevations":
            if line == "WAHLAO EH!":
                mode = "read_the_world_command"
                continue
            elevations.append([float(x) for x in line.split(",")])
        if mode == "read_the_world_command":
            if line == "WAHLAO EH!":
                mode = "load_objects"
                continue
            
            elevation_function = lambda z,x: elevations[z][x]
            try:
                the_world = eval(line)
            except:
                traceback.print_exc()
                raise Exception("Tried to execute:"+line)
        if mode == "load_objects":
            
            if line == "WAHLAO EH!":
                break
            
            objects_to_load.append(line)
            
    loading.progress_bar("Loading 3/3")
    world=the_world
    executables = []
    count = 0
    load_objects = ""
    for i in range(len(objects_to_load)):
        load_objects += "try:"+objects_to_load[i] + "\nexcept:print('failure')\n"
        count += 1
        if count >= 1000:
            executables.append(load_objects)
            load_objects=''
            count = 0
    if load_objects != '':
        executables.append(load_objects)
    
    t = time()
    for i in range(len(executables)):
        exec(executables[i])
        loading.update(i/len(executables)*100)
    print("loading 3/3 took",time() - t)
    loading.update(100)
    
    #for backward compatibility
    if "line_of_sight2" not in the_world.properties:
        the_world.properties["line_of_sight2"] = 8
    
    return the_world
