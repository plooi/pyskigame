import world
from pylooiengine import *
from os import path
import os
import traceback

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
def write(world):
    if not path.isdir("./worlds"):#worlds is for map editor worlds, ./saves is for ski game saves
        os.mkdir("./worlds")
    if not path.isdir("./worlds/"+world.properties["name"]):
        os.mkdir("./worlds/"+world.properties["name"])
        
    f = open("./worlds/"+world.properties["name"]+"/save", "w")
    
    out = StringBuffer()
    
    
    #step 1: Write all the terrain points to the file
    for r in range(world.get_height_points()):
        for c in range(world.get_width_points()):
            if c > 0:
                out.append(",")
            out.append(world.get_elevation(r, c, scaled=False))
        out.append("\n")
    out.append("WAHLAO EH!\n")
    
    out.append("World().init(%s, %d, %d, %s, elevation_function)"% ('"'+world.properties["name"]+'"', world.properties["width"], world.properties["height"], property_string(world.properties)))
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
    from world import World
    from tree import Tree,tree_design_1
    from lift import Lift,chair_model_1,chair_model_2,chair_model_3,chair_model_4,rope_model_1,terminal_design_1,pole_design_1
    
    
    
    
    f = open(path+"/save", "r")
    
    elevations = []
    world = None
    
    
    mode = "read_elevations"
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
            try:
                eval(line)
            except:
                traceback.print_exc()
                raise Exception("Tried to execute:"+line)
    return world
