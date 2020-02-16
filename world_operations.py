from tree import Tree
from random import random
from model_3d import *
import PySimpleGUI as sg
from models import *
from rock import Rock
from bump import Bump,NaturalBump
from world_object import WorldObject
from lodge import *
from mission_center import *
from landmark import *
import traceback
import loading


        
def natural_bumps(world, z1, x1, z2, x2, prog_bar=False):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    radius += 2
    if prog_bar: loading.progress_bar("Loading 2/3")
        
    
    hs = world.properties["horizontal_stretch"]
    vs = world.properties["vertical_stretch"]
    for z in range(int((middle_z - radius)*hs), int((middle_z + radius)*hs),7):
        if prog_bar and z % 7 == 0: loading.update(100*(z-int((middle_z - radius)*hs))/((int((middle_z + radius)*hs))-(int((middle_z - radius)*hs))))
        #print(z,"/",radius*2*hs)
        
        for x in range(int((middle_x - radius)*hs), int((middle_x + radius)*hs), 7):
            if world.is_bump(z, x):
                NaturalBump(z=z/hs,x=x/hs, world=world)
    if prog_bar: loading.update(100)
    
def remove_natural_bumps(world, z1, x1, z2, x2):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    radius += 2
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if world.valid_floor(z,x):
                objs = world.quads[z][x].containedObjects
                i=0
                while i < len(objs):
                    if isinstance(objs[i], NaturalBump):
                        objs[i].delete()#this automatically deletes the bump from the list
                        i -= 1#but I still have to do i -= 1
                    i += 1

def place_bumps(world, z1, x1, z2, x2, chance = 1):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                if chance == 1:
                    Bump(z=z+random(), x=x+random(), world=world)
                else:
                    if random() < chance:
                        Bump(z=z+random(), x=x+random(), world=world)
                        
def remove_bumps(world, z1, x1, z2, x2):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                objs = world.quads[z][x].containedObjects
                i=0
                while i < len(objs):
                    if isinstance(objs[i], Bump):
                        objs[i].delete()#this automatically deletes the bump from the list
                        
                        i -= 1#but I still have to do i -= 1
                        
                    i += 1


def fill_trees(world, z1, x1, z2, x2, chance = 1):
    for z in range(min([z1,z2]), max([z1,z2])+1):
        for x in range(min([x1,x2]), max([x1,x2])+1):
            if chance == 1:
                Tree(z, x, world)
            else:
                if random() < chance:
                    Tree(z, x, world)
            
def chainsaw(world, z1, x1, z2, x2):
    for z in range(min([z1,z2]), max([z1,z2])+1):
        for x in range(min([x1,x2]), max([x1,x2])+1):
            objs = world.quads[z][x].containedObjects
            i=0
            while i < len(objs):
                if isinstance(objs[i], Tree):
                    objs[i].delete()#this automatically deletes the tree from the list
                    
                    i -= 1#but I still have to do i -= 1
                    
                i += 1
                
                

                    
def fill_trees_circular(world, z1, x1, z2, x2, chance = 1):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                if chance == 1:
                    Tree(z, x, world)
                else:
                    if random() < chance:
                        Tree(z, x, world)
                
def chainsaw_circular(world, z1, x1, z2, x2, chance = 1):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                objs = world.quads[z][x].containedObjects
                i=0
                while i < len(objs):
                    if isinstance(objs[i], Tree):
                        objs[i].delete()#this automatically deletes the tree from the list
                        
                        i -= 1#but I still have to do i -= 1
                        
                    i += 1
                    
                    
def raise_hill(world, z1, x1, z2, x2, amount):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    
    recreate_strings = []
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_point(z, x):
                increase = amount * (   1   -   ((z-middle_z)**2 + (x-middle_x)**2)**.5 / radius   )
                if world.valid_floor(z, x):
                    for obj in world.quads[z][x].containedObjects:
                        if isinstance(obj, Tree):
                            recreate_strings.append(world.object_account[id(obj)])
                        elif isinstance(obj, WorldObject):
                            del obj.args["y"]
                            del obj.args["model_y"]
                            recreate_strings.append(obj.get_recreate_string())
                
                world.set_elevation(z, x, world.get_elevation(z,x) + increase, False)
                
    radius += 2
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                world.reset_floor_texture(z,x)
                
    for recreate in recreate_strings:
        eval(recreate)
                
def plateau(world, z1, x1, z2, x2, amount):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    y = world.get_elevation(middle_z,middle_x)
    
    recreate_strings = []
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_point(z, x):
                if world.valid_floor(z, x):
                    for obj in world.quads[z][x].containedObjects:
                        if isinstance(obj, Tree):
                            recreate_strings.append(world.object_account[id(obj)])
                        elif isinstance(obj, WorldObject):
                            del obj.args["y"]
                            del obj.args["model_y"]
                            recreate_strings.append(obj.get_recreate_string())
                world.set_elevation(z, x, y + amount, False)
                
    radius += 2
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                world.reset_floor_texture(z,x)
    
    for recreate in recreate_strings:
        eval(recreate)
        
    
def smooth(world, z1, x1, z2, x2):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    
    
    #bounding box
    boundaryz1 = middle_z - radius - 1
    boundaryx1 = middle_x - radius - 1
    boundaryz2 = middle_z + radius + 1
    boundaryx2 = middle_x + radius + 1
    
    
    original_values = [None]*(boundaryz2-boundaryz1)
    for r in range(len(original_values)):
        original_values[r] = [(world.get_elevation(r+boundaryz1, x, scaled=False) if world.valid_point(r+boundaryz1, x) else None) for x in range(boundaryx1, boundaryx2)]
    def origval(z, x):
        return original_values[z-boundaryz1][x-boundaryx1]
    
    recreate_strings = []
    
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_point(z, x):
                if (
                        world.valid_point(z-1,x) and
                        world.valid_point(z-1,x-1) and
                        world.valid_point(z,x-1) and
                        world.valid_point(z+1,x-1) and
                        world.valid_point(z+1,x) and
                        world.valid_point(z+1,x+1) and
                        world.valid_point(z,x+1) and
                        world.valid_point(z-1,x+1) 
                        
                        ): 
                    if world.valid_floor(z, x):
                        for obj in world.quads[z][x].containedObjects:
                            if isinstance(obj, Tree):
                                recreate_strings.append(world.object_account[id(obj)])
                            elif isinstance(obj, WorldObject):
                                del obj.args["y"]
                                del obj.args["model_y"]
                                recreate_strings.append(obj.get_recreate_string())
                    world.set_elevation(z, x, ( origval(z-1,x)+origval(z-1,x-1)+origval(z,x-1)+origval(z+1,x-1)+origval(z+1,x)+origval(z+1,x+1)+origval(z,x+1)+origval(z-1,x+1)+origval(z,x))/9    , reset_color=False)
                    #world.set_elevation(z,x, origval(z,x), False)
    radius += 2
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                world.reset_floor_texture(z,x)
    for recreate in recreate_strings:
        eval(recreate)
    
    
#THICKNESS IS THE  DIAMETER 
def chainsaw_straight(world, z1, x1, z2, x2, thickness):
    distance = ((z1-z2)**2 + (x1-x2)**2)**.5
    
    thickness = thickness/2
    
    def travel(fraction):
        inverted_fraction = 1-fraction
        return [
                    x1 * inverted_fraction + x2 * fraction,
                    z1 * inverted_fraction + z2 * fraction,
                    ]
    
    for i in range(0, int(distance), 1):
        loc = travel(i/distance)
        x = loc[0]
        z = loc[1]
        for zz in range(int(z-thickness), int(z+thickness)):
            for xx in range(int(x-thickness), int(x+thickness)):
                if ((zz-z)**2 + (xx-x)**2)**.5 < thickness and world.valid_floor(zz,xx):
                    objs = world.quads[zz][xx].containedObjects
                    i=0
                    while i < len(objs):
                        if isinstance(objs[i], Tree):
                            objs[i].delete()#this automatically deletes the tree from the list
                            
                            i -= 1#but I still have to do i -= 1
                            
                        i += 1
    
    
            
    
#thickness is the DIAMETER
#thickness in unscaled length
def path(world, z1, x1, z2, x2, thickness):
    thickness = thickness/2
    elevation1 = world.get_elevation(z1, x1, scaled=False)
    elevation2 = world.get_elevation(z2, x2, scaled=False)
    distance = ((z1-z2)**2 + (x1-x2)**2)**.5
    
    
    if elevation2 > elevation1:
        #we always want elevation 1 to be the higher elevation
        #because then the path is "going down"
        #if the path is going down, the method we're using
        #causes downward paths to be concave, while upward paths are convex. Convex is bad.
        tempx = x1
        tempz = z1
        tempy = elevation1
        x1 = x2
        z1 = z2
        elevation1 = elevation2
        x2 = tempx
        z2 = tempz
        elevation2 = tempy
        
    
    
    def travel(fraction):
        inverted_fraction = 1-fraction
        return [
                    x1 * inverted_fraction + x2 * fraction,
                    elevation1 * inverted_fraction + elevation2 * fraction,
                    z1 * inverted_fraction + z2 * fraction,
                    ]
    
    recreate_strings = []
    for i in range(0, int(distance), 1):
        loc = travel(i/distance)
        
        x = loc[0]
        y = loc[1]
        z = loc[2]
        
        
        
        #at each step along the path, set all the squares around you to the same elevation as the center of the path
        for zz in range(int(z-thickness), int(z+thickness)):
            for xx in range(int(x-thickness), int(x+thickness)):
                if world.valid_floor(zz,xx):
                    dist_frm_ctr = ((zz-z)**2 + (xx-x)**2)**.5
                    
                    if dist_frm_ctr < thickness:
                        for zzz in range(zz-1, zz+1):
                            for xxx in range(xx-1, xx+1):
                                for obj in world.quads[zzz][xxx].containedObjects:
                                    if isinstance(obj, Tree):
                                        if world.object_account[id(obj)] not in recreate_strings:
                                            recreate_strings.append(world.object_account[id(obj)])
                                    elif isinstance(obj, WorldObject):
                                        if obj.get_recreate_string() not in recreate_strings:
                                            del obj.args["y"]
                                            del obj.args["model_y"]
                                            recreate_strings.append(obj.get_recreate_string())
                    
                    if dist_frm_ctr < thickness - 3:
                        world.set_elevation(zz,xx,y,False)
                    elif dist_frm_ctr < thickness - 2:
                        world.set_elevation(zz,xx,(y*3+1*world.get_elevation(zz,xx,scaled=False))/4,False)
                    elif dist_frm_ctr < thickness - 1:
                        world.set_elevation(zz,xx,(y*2+2*world.get_elevation(zz,xx,scaled=False))/4,False)
                    elif dist_frm_ctr < thickness:
                        world.set_elevation(zz,xx,(y*1+3*world.get_elevation(zz,xx,scaled=False))/4,False)
                        
                    
                            
    thickness += 2 
    for i in range(0, int(distance), 2):
        loc = travel(i/distance)
        
        x = loc[0]
        y = loc[1]
        z = loc[2]
        
        for zz in range(int(z-thickness), int(z+thickness)):
            for xx in range(int(x-thickness), int(x+thickness)):
                if ((zz-z)**2 + (xx-x)**2)**.5 < thickness and world.valid_floor(zz,xx):
                    world.reset_floor_texture(zz,xx)
                    
    for recreate in recreate_strings:
        eval(recreate)
    
    
