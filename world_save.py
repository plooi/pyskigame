import world
from pylooiengine import *
from os import path
import os
import traceback
from models import *
import loading
from building import *
from bump import Bump
from landmark import Landmark
from world_object import *
from mission_center import MissionCenter

class StringBuffer:
    def __init__(self):
        self.array = []
    def append(self, text):
        self.array.append(str(text))
    def get_string(self):
        return "".join(self.array)

"""
write

writes a map editor world to a file
"""
def write(world,old_vertical_stretch=None,writepath="./worlds/"):
    if writepath.endswith("/") or writepath.endswith("\\"):
        pass#okay
    else:
        writepath+="/"
    if not path.isdir(writepath):#worlds is for map editor worlds, ./saves is for ski game saves
        os.mkdir(writepath)
    if not path.isdir(writepath+world.properties["name"]):
        os.mkdir(writepath+world.properties["name"])
        
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
def read(path):
    from world import World,View
    from tree import Tree
    from lift import Lift#,chair_model_1,chair_model_2,chair_model_3,chair_model_4,rope_model_1,terminal_design_1,pole_design_1
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
    world = None
    
    
    mode = "read_elevations"
    
    objects_to_load = []
    
    for line in f:
        line = line.strip()
        if mode == "read_elevations":
            if line == "WAHLAO EH!":
                mode = "read_world_command"
                continue
            elevations.append([float(x) for x in line.split(",")])
        if mode == "read_world_command":
            if line == "WAHLAO EH!":
                mode = "load_objects"
                continue
            
            elevation_function = lambda z,x: elevations[z][x]
            try:
                world = eval(line)
            except:
                traceback.print_exc()
                raise Exception("Tried to execute:"+line)
        if mode == "load_objects":
            
            if line == "WAHLAO EH!":
                break
            
            objects_to_load.append(line)
            
    loading.progress_bar("Loading 2/2")
    for i in range(len(objects_to_load)):
        try:
            eval(objects_to_load[i])
        except:
            traceback.print_exc()
            raise Exception("Tried to execute:"+line)
        if i %400 == 0:
            loading.update(i/len(objects_to_load)*100)
    loading.update(100)
    return world
