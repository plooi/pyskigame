from pylooiengine import *
import pylooiengine
import numpy
#from queue import Queue

size_increase = 50*4#this has to be a multiple of four.
class Queue:
    def __init__(self):
        self.data = []
    def put(self,x,block=False):
        self.data.append(x)
    def empty(self):
        return len(self.data) == 0
    def get(self, block=False):
        return self.data.pop(0)
        


class VertexHandler:
    def __init__(self, vertex_size, color_size=3, initial_capacity=2):
        initial_capacity *= 4 #to make sure it's multiple of four so squares will stay together
        #self.vertices = numpy.zeros([initial_capacity, vertex_size])
        #self.vertex_colors = numpy.zeros([initial_capacity, color_size])
        self.vertices = numpy.zeros([initial_capacity, vertex_size])
        self.vertex_colors = numpy.zeros([initial_capacity, color_size])
        self.available_indices = Queue()
        self.vertex_size = vertex_size
        self.color_size = color_size
        self.num_available_indices = 0
        
        for i in range(initial_capacity):
            self.available_indices.put(i, block=False)
            self.num_available_indices += 1
                
    def get_vertices(self):
        return self.vertices
    def get_colors(self):
        return self.vertex_colors
        
    #set the vertex handler to read mode. Returns true if mode was switched, and false if it was already in the correct mode
    def numpy_mode(self):
        if self.get_mode() == "list":
            self.vertices = numpy.array(self.vertices)
            self.vertex_colors = numpy.array(self.vertex_colors)
            return True
        return False
    #set the vertex handler to write mode. Returns true if mode was switched, and false if it was alwritey in the correct mode
    def list_mode(self):
        if self.get_mode() == "numpy":
            self.vertices = self.vertices.tolist()
            self.vertex_colors = self.vertex_colors.tolist()
            return True
        return False
    def get_mode(self):
        if type(self.vertices) == type([]):
            return "list"
        return "numpy"
    def add_vertex(self, vertex=None, color=None):
        
        if vertex == None: vertex = [0]*self.vertex_size
        if color == None: color = [0]*self.color_size
        if self.available_indices.empty():
            self.inc_size()
        index = self.available_indices.get(block=False)
        self.num_available_indices -= 1
        self.update_vertex(index, vertex, color)
        return index
        
    def capacity(self):
        return len(self.vertices)
    def num_occupied(self):
        return self.capacity() - self.num_available_indices
    def rm_vertex(self, index):
        if index >= len(self.vertices):
            fail("Cannot remove vertex %d from vertex list of length %d" % (index, len(self.vertices)))
        self.vertices[index] = [0]*self.vertex_size
        self.vertex_colors[index] = [0]*self.color_size
        self.available_indices.put(index, block=False)
        self.num_available_indices += 1
    def inc_size(self):
        #increases the size by size_increase variable
        original_length = len(self.vertices)
        for i in range(size_increase):
            self.available_indices.put(i + original_length, block=False)
        
        if self.get_mode() == "numpy":
            self.vertices = numpy.vstack((self.vertices, [[0]*self.vertex_size]*size_increase))
            self.vertex_colors = numpy.vstack((self.vertex_colors, [[0]*self.color_size]*size_increase))
        else:
            for i in range(size_increase):
                self.vertices.append([0]*self.vertex_size)
                self.vertex_colors.append([0]*self.color_size)
        
        self.num_available_indices += size_increase
    #vertices and colors are numpy arrays with vertices and colors
    def add_vertices_colors(self, vertices, colors):
        if len(vertices) % 4 != 0:
            raise Exception("no")
        if len(vertices) != len(colors):
            raise Exception("no")
        ret = len(self.vertices)
        self.vertices = numpy.vstack((self.vertices,vertices))
        self.vertex_colors = numpy.vstack((self.vertex_colors,colors))
        
        return ret
    def update_vertex(self, index, new_vertex, new_color):
        if index >= len(self.vertices):
            fail("Cannot update vertex %d from vertex list of length %d" % (index, len(self.vertices)))
        
        
    
        self.vertices[index] = new_vertex
        self.vertex_colors[index] = new_color
    def clear(self):
        taken_indices = [x for x in range(0, len(self.vertices))]
        available_indices = []
        for i in range(self.num_available_indices):
            index = self.available_indices.get(block = False)
            available_indices.append(index)
            self.available_indices.put(index, block=False)
        
        for item in available_indices:
            taken_indices.remove(item)
        for index in taken_indices:
            self.rm_vertex(index)
    def __str__(self):
        ret = ""
        ret += "VertexHandler object\n"
        ret += "capacity = " + str(len(self.vertices)) + "\n"
        available_indices = []
        for i in range(self.num_available_indices):
            index = self.available_indices.get(block = False)
            available_indices.append(index)
            self.available_indices.put(index, block=False)
        taken_indices = [x for x in range(0, len(self.vertices))]
        
        
        for index in [x for x in range(0, len(self.vertices))]:
            ret += (str(self.vertices[index]) + " " + str(self.vertex_colors[index]) + "\n")
        return ret

    
def main():
    pass
    
    print(v)
if __name__ == "__main__": main()
"""
def draw_quad_3ds(self, setup_3d=default_3d_view_setup):
        vertices = self.quad_3d_vertex_handler.vertices
        colors = self.quad_3d_vertex_handler.vertex_colors
        
        
        glPushMatrix()
        setup_3d()
        
        
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_COLOR_ARRAY);
        
        glVertexPointerf(vertices);
        glColorPointerf(colors)
        glDrawArrays(GL_QUADS, 0, self.quad_3d_vertex_handler.capacity());
        
        #e = time()
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_COLOR_ARRAY);
        
        glPopMatrix()
"""
