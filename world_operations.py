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
