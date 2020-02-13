from tree import Tree
from models import *

class Landmark(Tree):
    def __init__(self, z, x, world, darkness_factor=.4, design_function=landmark_model_1, rotation=None):
        super().__init__(z,x,world,darkness_factor,design_function,rotation,gradient_model=True)
        self.world.landmarks.append(self)
        self.showing = True
        
    def add_object_account(self):
        self.world.add_object_account(self, "Landmark(%d, %d, world, %f, %s, %f)"%(self.z, self.x, self.darkness_factor, find_name(self.design_function), self.rotation))
    def reset(self,delete=True):
        super().reset(delete=delete)
        self.showing = True
    def open_menu(self):
        layout = [
            [sg.Button("Delete")],
        ]
        
        
        window = sg.Window("Landmark", layout, size=(500,800))
        event, values = window.Read()
        
        if event == "Delete":
            self.delete()
        window.close()
    
    def hide(self):
        if self.showing:
            rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
            self.showing = False
    def show(self):
        if not self.showing:
            self.vertex_handler_pointers = add_model_to_world_fixed(self.design, self.world, self.z, self.x, self, gradient_model=True)
            self.showing = True
    def delete(self):
        if self.showing:
            rm_model_from_world_fixed(self.vertex_handler_pointers, self.world, self.z, self.x, self)
        self.world.delete_object_account(self)
        if self in self.world.landmarks:
            self.world.landmarks.remove(self)
        


