"""
My philosophy is black box philosophy.

Don't care how it works, just know THAT it works.

Snowfall: Create object of this to instantiate one particle of repeating snowfall



"""
















from pylooiengine import *

from random import random
















snowfall_particles = []
spray_particles = []

w,h=0,0
class Go(LooiObject):
    def __init__(self):
        super().__init__()
    def paint(self):
        self.draw_text(100,100,str(len(snowfall_particles)))
        self.draw_rect(0,0,self.get_my_window().get_internal_size()[0],self.get_my_window().get_internal_size()[1], black)
        
    def step(self):
        if self.key("s","down"):
            back(16)
        if self.key("w","down"):
            forward(16)
        if self.key("a","down"):
            left(-33)
        if self.key("d","down"):
            left(33)
            
def up(n):
    for s in snowfall_particles+spray_particles:
        s.y += n
def left(n):
    for s in snowfall_particles+spray_particles:
        s.x -= n

def forward(n):
    for s in snowfall_particles:
        s.z += .1*n
        s.x -= w/2
        s.y -= h/2
        factor = .01*s.z/20*n
        factor += 1
        s.x *= factor
        s.y *= factor
        s.x += w/2
        s.y += h/2
    for s in spray_particles:
        s.z += .1*n
        s.x -= w/2
        s.y -= 9*h/10
        factor = .01*s.z/20*n
        factor += 1
        s.x *= factor
        s.y *= factor
        s.x += w/2
        s.y += 9*h/10
            
class SnowFall(LooiObject):
    def __init__(self, world):
        global snowfall_particles,w,h
        super().__init__()
        self.set_layer(1)
        self.init()
        self.world = world
        
        w = self.get_my_window().get_internal_size()[0]
        h = self.get_my_window().get_internal_size()[1]
        
        self.upon_activation()
    def init(self):
        
        self.x=random()*w
        self.y=random()**2*h
        self.z=random()*12+3
        self.actual_size = .4
    def upon_activation(self):
        global snowfall_particles
        snowfall_particles.append(self)
    def upon_deactivation(self):
        global snowfall_particles
        snowfall_particles.remove(self)
    def randx(self):
        self.x = random() * self.get_my_window().get_internal_size()[0]
    def step(self):
        self.y += self.z*2.2
        if self.y > h-(1-self.z/13)*600:
            if self.z > 15: 
                self.init()
                self.z = 5
            else:
                self.init()
                self.y = random()*h/5
        if self.y < 0: self.init()
        
        if self.x > w:
            self.init()
            self.x = random() * w/5
        if self.x < 0: 
            self.init()
            self.x = random() *w/5 + 4*w/5
            
        if self.z < 3:
            self.init()
            self.z = 15+random()*5
            r = random()
            if r < .25:
                self.x = random()*w/4
            elif r < .5:
                self.x = random()*w/4+3*w/4
            elif r < .75:
                self.y = random()*h/4
            else:
                self.y = random()*h/4+3*h/4
        
    def paint(self):
        o = self.z
        self.z *= self.actual_size
        x1,y1,x2,y2=self.x-self.z/2,self.y-self.z/2,self.x+self.z/2,self.y+self.z/2
        
        
        self.world.particle_handler.add_vertex([x1,y1],[1,1,1])
        self.world.particle_handler.add_vertex([x2,y1],[1,1,1])
        self.world.particle_handler.add_vertex([x2,y2],[1,1,1])
        self.world.particle_handler.add_vertex([x1,y2],[1,1,1])
        
        
        self.z = o
class Spray(LooiObject):
    def __init__(self, world):
        global spray_particles,w,h
        super().__init__()
        self.set_layer(1)
        self.init()
        self.world = world
        
        w = self.get_my_window().get_internal_size()[0]
        h = self.get_my_window().get_internal_size()[1]
        
        self.upon_activation()
    def init(self):
        
        self.x=random()*w/3+w/3
        self.y=random()*h/4+3*h/4
        self.z=random()*3+6
        self.actual_size = .4
    def upon_activation(self):
        global spray_particles
        spray_particles.append(self)
    def upon_deactivation(self):
        global spray_particles
        spray_particles.remove(self)
    def randx(self):
        self.x = random() * self.get_my_window().get_internal_size()[0]
    def step(self):
        self.y += self.z*1.2
        if self.y > h:self.deactivate()
            
        if self.y < 0: self.deactivate()
        elif self.x > w: self.deactivate()
        elif self.x < 0: self.deactivate()
        elif self.z < 3:self.deactivate()
        elif self.z > 20: self.deactivate
    def paint(self):
        o = self.z
        self.z *= self.actual_size
        x1,y1,x2,y2=self.x-self.z/2,self.y-self.z/2,self.x+self.z/2,self.y+self.z/2
        
        
        self.world.particle_handler.add_vertex([x1,y1],[1,1,1])
        self.world.particle_handler.add_vertex([x2,y1],[1,1,1])
        self.world.particle_handler.add_vertex([x2,y2],[1,1,1])
        self.world.particle_handler.add_vertex([x1,y2],[1,1,1])
        
        
        self.z = o
        
def main():
    w = Window()
    
    
    
    
    Go()
    for i in range(30):
        SnowFall()
    w.start()
if __name__ == "__main__": main()

##################################################################

from pylooiengine import *
import pylooiengine
import numpy
#from queue import Queue
from random import random
import math
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
        


class ParticleHandler:
    def __init__(self, vertex_size, color_size=3, initial_capacity=2):
        initial_capacity *= 4 #to make sure it's multiple of four so squares will stay together
        self.vertices = numpy.zeros([initial_capacity, vertex_size])
        self.vertex_colors = numpy.zeros([initial_capacity, color_size])
        self.velocities = numpy.zeros([initial_capacity, vertex_size])
        self.accelerations = numpy.zeros([initial_capacity, vertex_size])
        self.times = {}
        
        
        
        
        
        self.available_indices = Queue()
        self.vertex_size = vertex_size
        self.color_size = color_size
        self.num_available_indices = 0
        
        for i in range(initial_capacity):
            self.available_indices.put(i, block=False)
            self.num_available_indices += 1
    
    
    
    def add_particle(self,x,y,z,vx,vy,vz,ax,ay,az,size,life,color,theta = None):
        s2 = size/2
        
        if theta==None: theta = random()*math.pi*2
        
        
        
        key=self.add_vertex(
                        [x+s2*math.cos(theta),y,z-s2*math.sin(theta)],
                        color,
                        [vx,vy,vz],
                        [ax,ay,az]
                        )
        self.add_vertex(
                        [x,y+s2,z],
                        color,
                        [vx,vy,vz],
                        [ax,ay,az]
                        )
        self.add_vertex(
                        [x-s2*math.cos(theta),y,z+s2*math.sin(theta)],
                        color,
                        [vx,vy,vz],
                        [ax,ay,az]
                        )
        self.add_vertex(
                        [x,y-s2,z],
                        color,
                        [vx,vy,vz],
                        [ax,ay,az]
                        )
        self.times[key] = life
    def step(self):
        self.velocities = numpy.add(self.velocities,self.accelerations)
        self.vertices = numpy.add(self.vertices, self.velocities)
        
        to_del = set()
        for k in self.times:
            if self.times[k] <= 0:
                self.rm_vertex(k)
                self.rm_vertex(k+1)
                self.rm_vertex(k+2)
                self.rm_vertex(k+3)
                to_del.add(k)
            else:
                self.times[k] -= 1
        for k in to_del:
            del self.times[k]
    
    
    
    
    
    def get_vertices(self):
        return self.vertices
    def get_colors(self):
        return self.vertex_colors
        

    def add_vertex(self, vertex=None, color=None, velocity=None, acc=None):
    
        
        if vertex == None: vertex = [0]*self.vertex_size
        if color == None: color = [0]*self.color_size
        if velocity == None: velocity= [0]*self.vertex_size
        if acc == None: acc = [0]*self.vertex_size
        
        if self.available_indices.empty():
            self.inc_size()
        index = self.available_indices.get(block=False)
        self.num_available_indices -= 1
        self.update_vertex(index, vertex, color, velocity, acc)
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
        self.velocities[index] = [0]*self.vertex_size
        self.accelerations[index] = [0]*self.vertex_size
        
        
        self.available_indices.put(index, block=False)
        self.num_available_indices += 1
    def inc_size(self):
        #increases the size by size_increase variable
        original_length = len(self.vertices)
        for i in range(size_increase):
            self.available_indices.put(i + original_length, block=False)
        

        self.vertices = numpy.vstack((self.vertices, [[0]*self.vertex_size]*size_increase))
        self.vertex_colors = numpy.vstack((self.vertex_colors, [[0]*self.color_size]*size_increase))
        self.velocities = numpy.vstack((self.velocities, [[0]*self.vertex_size]*size_increase))
        self.accelerations = numpy.vstack((self.accelerations, [[0]*self.vertex_size]*size_increase))
        
        
        
        
        self.num_available_indices += size_increase
        
    def update_vertex(self, index, new_vertex, new_color, new_vel, new_acc):
        if index >= len(self.vertices):
            fail("Cannot update vertex %d from vertex list of length %d" % (index, len(self.vertices)))
        
        
    
        self.vertices[index] = new_vertex
        self.vertex_colors[index] = new_color
        self.velocities[index] = new_vel
        self.accelerations[index] = new_acc
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
        ret += "ParticleHandler object\n"
        ret += "capacity = " + str(len(self.vertices)) + "\n"
        ret += "num occupied = " + str(self.num_occupied()) + "\n"
        available_indices = []
        for i in range(self.num_available_indices):
            index = self.available_indices.get(block = False)
            available_indices.append(index)
            self.available_indices.put(index, block=False)
        taken_indices = [x for x in range(0, len(self.vertices))]
        
        
        for index in [x for x in range(0, len(self.vertices))]:
            key = int(index/4)*4
            if key in self.times:
                ret += (str(self.vertices[index]) + " " + str(self.velocities[index]) + " " + str(self.times[key]) + "\n")
        return ret

    
def main():
    p = ParticleHandler(3)
    p.add_particle(0,0,0, 0,0,0, 1,0,0, 2, 10, [1,1,1],0)
    print("phase1",p)
    
    for i in range(100):
        p.step()
        print("phase"+str(i),p)
    
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
