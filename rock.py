import math
from random import random
from model_3d import *
from util import *
from tree import Tree
from models import *
from pylooiengine import *






class Rock(Tree):
    def __init__(self, z, x, world, darkness_factor=2, design_function=rock_design_1, rotation=None):
        super().__init__(z,x,world,darkness_factor,design_function,rotation)
    def add_object_account(self):
        self.world.add_object_account(self, "Rock(%d, %d, world, %f, %s, %f)"%(self.z, self.x, self.darkness_factor, find_name(self.design_function), self.rotation ))
        
        
        
