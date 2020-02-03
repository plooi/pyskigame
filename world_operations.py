from tree import Tree
from random import random
from model_3d import *
import PySimpleGUI as sg

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
    
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_point(z, x):
                increase = amount * (   1   -   ((z-middle_z)**2 + (x-middle_x)**2)**.5 / radius   )
                world.set_elevation(z, x, world.get_elevation(z,x) + increase, False)
                
    radius += 2
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                world.reset_floor_color(z,x)
                
                
def plateau(world, z1, x1, z2, x2, amount):
    middle_z = int((z1+z2)/2)
    middle_x = int((x1+x2)/2)
    
    radius = int(((z1-z2)**2 + (x1-x2)**2)**.5 / 2) + 1
    y = world.get_elevation(middle_z,middle_x)
    
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_point(z, x):
                
                world.set_elevation(z, x, y + amount, False)
                
    radius += 2
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                world.reset_floor_color(z,x)
                
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
                    world.set_elevation(z, x, ( origval(z-1,x)+origval(z-1,x-1)+origval(z,x-1)+origval(z+1,x-1)+origval(z+1,x)+origval(z+1,x+1)+origval(z,x+1)+origval(z-1,x+1)+origval(z,x))/9    , reset_color=False)
                    #world.set_elevation(z,x, origval(z,x), False)
    radius += 2
    for z in range(middle_z - radius, middle_z + radius):
        for x in range(middle_x - radius, middle_x + radius):
            if ((z-middle_z)**2 + (x-middle_x)**2)**.5 <= radius and world.valid_floor(z, x):
                world.reset_floor_color(z,x)
                        
    
    
def chainsaw_straight(world, z1, x1, z2, x2, thickness):
    distance = ((z1-z2)**2 + (x1-x2)**2)**.5
    
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
    
    
            
    
    
#thickness in unscaled length
def path(world, z1, x1, z2, x2, thickness):
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
    
    
    for i in range(0, int(distance), 1):
        loc = travel(i/distance)
        
        x = loc[0]
        y = loc[1]
        z = loc[2]
        
        
        #at each step along the path, set all the squares around you to the same elevation as the center of the path
        for zz in range(int(z-thickness), int(z+thickness)):
            for xx in range(int(x-thickness), int(x+thickness)):
                if ((zz-z)**2 + (xx-x)**2)**.5 < thickness and world.valid_point(zz,xx):
                    world.set_elevation(zz,xx,y,False)
    thickness += 2 
    for i in range(0, int(distance), 2):
        loc = travel(i/distance)
        
        x = loc[0]
        y = loc[1]
        z = loc[2]
        
        for zz in range(int(z-thickness), int(z+thickness)):
            for xx in range(int(x-thickness), int(x+thickness)):
                if ((zz-z)**2 + (xx-x)**2)**.5 < thickness and world.valid_floor(zz,xx):
                    world.reset_floor_color(zz,xx)
    
    
    
