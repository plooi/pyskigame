from tree import Tree


class Landmark(Tree):
    def __init__(self, z, x, world, darkness_factor=.4, design_function=tree_design_1):
        super().__init__(z,x,world,darkness_factor,design_function,0)
        self.world.landmarks.add(self)
    def add_object_account(self):
        self.world.add_object_account(self, "Landmark(%d, %d, world, %f, %s, %f)"%(self.z, self.x, self.darkness_factor, find_name(self.design_function), self.rotation))
    def open_menu(self):
        layout = [
            [sg.Button("Delete")],
        ]
        
        
        window = sg.Window("Landmark", layout, size=(500,800))
        event, values = window.Read()
        
        if event == "Delete":
            self.delete()
        window.close()
        
    def delete(self):
        if self in self.world.landmarks:
            self.world.landmarks.remove(self)
        super().delete()
        
