def tree_design_1():
    tree_width = 1
    tree_height = 3
    color = [0,1,0]
    
    
    return [
    [-tree_width/2,0,0], [tree_width/2,0,0], [0,tree_height,0], [0,tree_height,0], color,
    [0,0,-tree_width/2], [0,0,tree_width/2], [0,tree_height,0], [0,tree_height,0], color
    
    
    ]
class Tree:
    def __init__(self, z, x, world, darkness_factor=.5, design_function=tree_design_1):
        self.z=z * world.unit_length + .5*world.unit_length
        self.x=x * world.unit_length + .5*world.unit_length
        self.world = world
        self.y = self.world.grid[z][x].elevation * self.world.vertical_stretch
        self.design_function = design_function
        self.design = design_function()
        for i in range(len(self.design)):
            if i%5 != 4:
                self.design[i][0] += self.x
                self.design[i][1] += self.y
                self.design[i][2] += self.z
            else:
                brightness = self.world.get_floor_color_zx(z, x)[0]
                darkness = 1-brightness
                self.design[i][1] -= darkness*darkness_factor
        self.vertex_handler_pointers = [0]*int(len(self.design)/5)
        self.added = False
        self.darkness_factor = darkness_factor
    """def add_to_vertex_handler(self, vertex_handler):
        if self.added:
            raise Exception()
        for i in range(len(self.vertex_handler_pointers)):
            index = i
            i *= 5
            #print("Adding to vh: " + str(self.design))
            self.vertex_handler_pointers[index] = vertex_handler.add_vertex([self.design[i][0], self.design[i][1], self.design[i][2]], self.design[i+4])
            _ = vertex_handler.add_vertex([self.design[i+1][0], self.design[i+1][1], self.design[i+1][2]], self.design[i+4])
            _ = vertex_handler.add_vertex([self.design[i+2][0], self.design[i+2][1], self.design[i+2][2]], self.design[i+4])
            _ = vertex_handler.add_vertex([self.design[i+3][0], self.design[i+3][1], self.design[i+3][2]], self.design[i+4])
        for index in range(len(self.vertex_handler_pointers)):
            vertex_handler.rm_vertex(self.vertex_handler_pointers[index])
            vertex_handler.rm_vertex(self.vertex_handler_pointers[index]+1)
            vertex_handler.rm_vertex(self.vertex_handler_pointers[index]+2)
            vertex_handler.rm_vertex(self.vertex_handler_pointers[index]+3)
    """
    def add_to_vertex_handler(self, vertex_handler):
        if self.added:
            raise Exception()
        self.added = True
        for i in range(len(self.vertex_handler_pointers)):
            index = i
            i *= 5
            #print("Adding to vh: " + str(self.design))
            self.vertex_handler_pointers[index] = vertex_handler.add_vertex([self.design[i][0], self.design[i][1], self.design[i][2]], self.design[i+4])
            _ = vertex_handler.add_vertex([self.design[i+1][0], self.design[i+1][1], self.design[i+1][2]], self.design[i+4])
            __ = vertex_handler.add_vertex([self.design[i+2][0], self.design[i+2][1], self.design[i+2][2]], self.design[i+4])
            ___ = vertex_handler.add_vertex([self.design[i+3][0], self.design[i+3][1], self.design[i+3][2]], self.design[i+4])
            
        
        
    def remove_from_vertex_handler(self, vertex_handler):
        if not self.added:
            raise Exception()
        self.added = False
        for i in range(len(self.vertex_handler_pointers)):
            vertex_handler.rm_vertex(self.vertex_handler_pointers[i])
            vertex_handler.rm_vertex(self.vertex_handler_pointers[i]+1)
            vertex_handler.rm_vertex(self.vertex_handler_pointers[i]+2)
            vertex_handler.rm_vertex(self.vertex_handler_pointers[i]+3)
    def copy_move(self, z, x):
        ret = Tree(z,x, self.world, self.darkness_factor, self.design_function)
        return ret
        
        
