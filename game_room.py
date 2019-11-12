import rooms
from pylooiengine.misc.graphics import *
from OpenGL.GL import *
from OpenGL.GLU import *
import player
import math




def start():
    rooms.game.start()


def rad_to_deg(rad):
    return rad/(2*math.pi) *360

def setup_3d():
    p = rooms.game.player
    gluPerspective(45, (main_window.window_size[0]/main_window.window_size[1]), 0.1, 50000.0)
    try:
        glRotate(rad_to_deg(-(p.hor_rot-math.pi/2)), 0, 1, 0)
        glRotate(rad_to_deg(-p.vert_rot), math.cos(p.hor_rot - math.pi/2), 0, -math.sin(p.hor_rot - math.pi/2))
        glTranslate(-p.x, -p.y, -p.z)
        
        
    except:
        pass
    
    

class Drawer(LooiObject):
    def __init__(self, game_room):
        super().__init__()
        self.game_room = game_room
    def paint(self):
        self.game_room.draw_quad_array_3d(self.game_room.vertex_handler.get_vertices(), self.game_room.vertex_handler.get_colors(), setup_3d=setup_3d)
        self.game_room.draw_quad_3d(-1,1,-5, 1,1,-5, 1,-1,-5, -1,-1,-5, black, setup_3d=setup_3d)
class GameRoom(rooms.Room):
    def __init__(self):
        super().__init__()
        self.load_mode = None
        self.world = None
        self.upon_enter = start
        self.vertex_handler = VertexHandler(3)
        self.unit_length = 2
        self.vertical_stretch = .15
        self.player = None
        
        self.drawer = Drawer(self)
        self.add(self.drawer)
    def start(self):
        self.player = player.Player()
        if self.load_mode == "new":
            self.load_world()
    def load_world(self):
        vertical_stretch = self.vertical_stretch
        self.vertex_handler.clear()
        for z in range(self.world.height-1):
            for x in range(self.world.width-1):
                
                #print(str(type(vertical_stretch)) + "    " + str(type( self.world.get_height(x,z))))
                
                color = random()*.5 +.5
                color = [color, color, color]
                self.vertex_handler.add_vertex(
                        [x*self.unit_length, 
                        vertical_stretch * self.world.get_height(x,z), 
                        z*self.unit_length]
                        , color)
                self.vertex_handler.add_vertex(
                        [(x+1)*self.unit_length, 
                        vertical_stretch * self.world.get_height(x+1,z), 
                        z*self.unit_length]
                        , color)
                self.vertex_handler.add_vertex(
                        [(x+1)*self.unit_length, 
                        vertical_stretch * self.world.get_height(x+1,z+1), 
                        (z+1)*self.unit_length]
                        , color)
                self.vertex_handler.add_vertex(
                        [x*self.unit_length, 
                        vertical_stretch * self.world.get_height(x,z+1), 
                        (z+1)*self.unit_length]
                        , color)
        
