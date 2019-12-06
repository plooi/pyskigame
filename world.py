from pylooiengine import *
from player import *
from pylooiengine.misc.graphics import VertexHandler
import math
import pylooiengine
import easygui
import rooms #UNCOMMENT THIS PLEASE!
import normal
import copy
from tree import Tree


#for testing
class FPS(LooiObject):
    def __init__(self, v):
        super().__init__()
        self.frames = 0
        self.seconds = 0
        self.fps = 0
        self.v = v
    def step(self):
        if int(time()) > (self.seconds):
            self.seconds = int(time())
            self.fps = self.frames
            self.frames = 0
        self.frames += 1
        
    def paint(self):
        self.draw_text(300,200,"FPS: " + str(self.fps))



def rad_to_deg(rad):
    return rad/(2*math.pi) *360



def new_world_from_dims(name, width, height):
    w = World(name, width, height)
    w.reset_floor_colors()
    return w
def new_world_from_data_file(name, file_name, min_row=0, max_row=9999999999999999999, min_col=0, max_col=9999999999999999999):
    w = World(name, 0, 0)
    f = open(file_name, "r")
    
    
    
    
    file_row = 0
    
    row = 0
    for line in f:
        if file_row >= min_row and file_row < max_row:
            line = line.strip().split(",")
            col = 0
            for file_col in range(0, len(line)):
                if file_col >= min_col and file_col < max_col:
                    w.set_elevation(row, col, 0 if line[file_col] == 'None' else float(line[file_col]) )
                    col += 1
                else:
                    pass
                    #print("col: " + str(file_col) + " rejected")
            row += 1
        file_row += 1
    f.close()
    w.smooth(0,0,w.get_height(),w.get_width())
    
    w.reset_floor_colors()
    
    return w


class World(LooiObject):
    def __init__(self, name, width, height, player=None, unit_length = 2, vertical_stretch = .15, chunk_size = 8, update_probability=1):
        super().__init__(active=False)
        self.unit_length = unit_length
        self.vertical_stretch = vertical_stretch
        self.vertex_handler = VertexHandler(3)
        self.chunk_size = chunk_size
        self.mobile_vertices = []
        self.mobile_colors = []
        self.name = name
        self.grid = []
        self.line_of_sight_update_box_size_scalar = 1.6 #as you move, you can turn off and on squares in the box
        self.update_probability = update_probability
        #defined by player's line of sight TIMES line_of_sight_update_box_size_scalar
        #if it's too small (like .5) then the tiles farthest away aren't gonna get turned off and on
        #properly because we're not checking them
        
        self.player = MapEditorPlayer() if player == None else player
        self.player.world = self
        self.player.deactivate()
        self.add(self.player)
        self.a = None
        self.add(FPS(0))
        for z in range(height):
            for x in range(width):
                self.set_elevation(z, x, 0)
        def setup_3d():
            p = self.player
            gluPerspective(45, (pylooiengine.main_window.window_size[0]/pylooiengine.main_window.window_size[1]), 0.1, 50000.0)
            try:
                glRotate(rad_to_deg(-(p.hor_rot-math.pi/2)), 0, 1, 0)
                glRotate(rad_to_deg(-p.vert_rot), math.cos(p.hor_rot - math.pi/2), 0, -math.sin(p.hor_rot - math.pi/2))
                glTranslate(-p.x, -p.y, -p.z)
            except:
                pass
        self.setup_3d = setup_3d
    
    def step(self):
        self.menu_option()
        self.update_line_of_sight()
    def paint(self):
        #draw all immobile vertices
        self.draw_quad_array_3d(self.vertex_handler.get_vertices(), self.vertex_handler.get_colors(), setup_3d=self.setup_3d)
        #self.draw_quad_3d(-1,1,-5, 1,1,-5, 1,-1,-5, -1,-1,-5, black, setup_3d=self.setup_3d)
        #self.draw_text(100,100, str(self.vertex_handler.capacity()))
        
        
        #self.add_quad([-1,1,-5],[1,1,-5],[1,-1,-5],[-1,-1,-5], Color(0,0,1))
        #draw mobile vertices
        if len(self.mobile_vertices) > 0:
            mobile_vertices = numpy.array(self.mobile_vertices)
            mobile_colors = numpy.array(self.mobile_colors)
            self.draw_quad_array_3d(mobile_vertices, mobile_colors, setup_3d=self.setup_3d)
            self.mobile_vertices = []
            self.mobile_colors = []
        
    def menu_option(self):
        if self.key("escape", "pressed"):
            result = easygui.indexbox(msg="Game Paused", title="", choices=("Exit", "Resume"), default_choice="Resume", cancel_choice="Resume")
            
            if result == 0:
                rooms.main_menu()
    
    def add_quad(self, vertex1, vertex2, vertex3, vertex4, color):
        self.mobile_vertices.append(vertex1)
        self.mobile_vertices.append(vertex2)
        self.mobile_vertices.append(vertex3)
        self.mobile_vertices.append(vertex4)
        if type(color) == type(Color(0,0,0)):
            color = color.to_tuple()
            self.mobile_colors.append(color)
            self.mobile_colors.append(color)
            self.mobile_colors.append(color)
            self.mobile_colors.append(color)
        elif type(color) == type([]):
            for i in range(4):
                #self.mobile_colors.append(int(i/4 * len(color)))
                self.mobile_colors.append(color)
    
    #unused
    def _add_all_points(self):
        for z in range(0, self.get_height()-1):
            for x in range(0, self.get_width()-1):
                color = random()*.5 +.5# for now we're just doing random colors
                color = [color, color, color]
                self.grid[z][x].floor_vert_handler_index = self.vertex_handler.add_vertex(
                        [x*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z,x),
                        z*self.unit_length]
                        , color) 
                _should_be_previous_plus_1 = self.vertex_handler.add_vertex(
                    [(x+1)*self.unit_length, 
                    self.vertical_stretch * self.get_elevation(z,x+1),
                    z*self.unit_length]
                    , color) 
                _should_be_last_plus_2 = self.vertex_handler.add_vertex(
                    [(x+1)*self.unit_length, 
                    self.vertical_stretch * self.get_elevation(z+1,x+1),
                    (z+1)*self.unit_length]
                    , color) 
                _should_be_plus_3 = self.vertex_handler.add_vertex(
                    [(x)*self.unit_length, 
                    self.vertical_stretch * self.get_elevation(z+1,x),
                    (z+1)*self.unit_length]
                    , color) 
    def update_line_of_sight(self):
        sc = self.line_of_sight_update_box_size_scalar
        los = self.player.line_of_sight
        player_z = int(self.player.z/self.unit_length)
        player_x = int(self.player.x/self.unit_length)
        
        #for z in range(player_z-int(los*sc), player_z+int(los*sc), self.chunk_size):
        #    for x in range(player_x-int(los*sc), player_x+int(los*sc), self.chunk_size):
        for z in range(0, self.get_height(), self.chunk_size):
            for x in range(0, self.get_width(), self.chunk_size):
                #loop through all nearby chunks
                
                
                chunk_corner_x = (x // self.chunk_size)* self.chunk_size
                chunk_corner_z = (z // self.chunk_size)* self.chunk_size
                chunk_center_x = (x // self.chunk_size)* self.chunk_size + self.chunk_size/2
                chunk_center_z = (z // self.chunk_size)* self.chunk_size + self.chunk_size/2
                
                #check if the chunk has any blocks in it (by checking the upper left corner (if U L corner has nothing, then it's empty/ off the screen))
                if chunk_corner_z >= 0 and chunk_corner_x >= 0 and chunk_corner_z < self.get_height()-1 and chunk_corner_x < self.get_width()-1:
                    
                    #check if the chunk is within the player's los
                    if (  ( (chunk_center_z-player_z)**2 + (chunk_center_x-player_x)**2 ) ** .5  ) <= (los):
                        #yes it is within the player's los
                        
                        #is it added?
                        if self.grid[chunk_corner_z][chunk_corner_x].floor_vert_handler_index == None:
                            #sweet niblets we have a square inside the los and not added
                            #we must add it
                            #if the probability test passes
                            if random() < self.update_probability:
                                for z in range(chunk_corner_z, chunk_corner_z+self.chunk_size):
                                    for x in range(chunk_corner_x, chunk_corner_x+self.chunk_size):
                                        if z < self.get_height()-1 and x <  self.get_width()-1: #if it's a bottom or right edge chunk, make sure that I am only attempting to add the squares that actually exist 
                                            #color = random()*.5 +.5# for now we're just doing random colors
                                            #color = [color, color, color]
                                            
                                            color = self.grid[z][x].color#self.get_floor_color_zx(z, x)
                                            
                                            #ADD FLOOR QUADRILATERAL
                                            self.grid[z][x].floor_vert_handler_index = self.vertex_handler.add_vertex(
                                                [x*self.unit_length, 
                                                self.vertical_stretch * self.get_elevation(z,x),
                                                z*self.unit_length]
                                                , color) 
                                            _should_be_previous_plus_1 = self.vertex_handler.add_vertex(
                                                [(x+1)*self.unit_length, 
                                                self.vertical_stretch * self.get_elevation(z,x+1),
                                                z*self.unit_length]
                                                , color) 
                                            _should_be_last_plus_2 = self.vertex_handler.add_vertex(
                                                [(x+1)*self.unit_length, 
                                                self.vertical_stretch * self.get_elevation(z+1,x+1),
                                                (z+1)*self.unit_length]
                                                , color) 
                                            _should_be_plus_3 = self.vertex_handler.add_vertex(
                                                [(x)*self.unit_length, 
                                                self.vertical_stretch * self.get_elevation(z+1,x),
                                                (z+1)*self.unit_length]
                                                , color) 
                                            if self.grid[z][x].tree_obj != None:
                                                #print("tree at %d %d" % (z,x))
                                                if not self.grid[z][x].tree_obj.added: self.grid[z][x].tree_obj.add_to_vertex_handler(self.vertex_handler)
                                            
                                                
                        else:
                            #kay that's fine, square inside the los and also added to vertex handler. good
                            pass
                        
                        #is the pan-chunk square added?
                        if self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index != None:
                            #yeah it's added, but we need to get rid of it because the chunk is actually within the los of player now
                            self.vertex_handler.rm_vertex(self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index)
                            self.vertex_handler.rm_vertex(self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index+1)
                            self.vertex_handler.rm_vertex(self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index+2)
                            self.vertex_handler.rm_vertex(self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index+3)
                            self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index = None
                    else:
                        #this square is outside the los
                        
                        #is it added?
                        if self.grid[chunk_corner_z][chunk_corner_x].floor_vert_handler_index == None:
                            #kay that's fine, square outside the los and also not added to vertex handler. good
                            pass
                        else:
                            #sweet niblets we have a square outside the los and IS added
                            #we must remove it
                            #if the probability test passes
                            if random() < self.update_probability:
                                for z in range(chunk_corner_z, chunk_corner_z+self.chunk_size):
                                    for x in range(chunk_corner_x, chunk_corner_x+self.chunk_size):
                                        if z < self.get_height()-1 and x <  self.get_width()-1: #if it's a bottom or right edge chunk, make sure that I am only attempting to rm the squares that actually exist 
                                            self.vertex_handler.rm_vertex(self.grid[z][x].floor_vert_handler_index)
                                            self.vertex_handler.rm_vertex(self.grid[z][x].floor_vert_handler_index+1)
                                            self.vertex_handler.rm_vertex(self.grid[z][x].floor_vert_handler_index+2)
                                            self.vertex_handler.rm_vertex(self.grid[z][x].floor_vert_handler_index+3)
                                            self.grid[z][x].floor_vert_handler_index = None
                                            
                                            
                                            if self.grid[z][x].tree_obj != None:
                                                if self.grid[z][x].tree_obj.added: self.grid[z][x].tree_obj.remove_from_vertex_handler(self.vertex_handler)
                                            
                        
                        #is the pan-chunk square added?
                        if self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index == None:
                            #it is not added, but we must add it
                            bottom_right_z = chunk_corner_z + self.chunk_size
                            bottom_right_x = chunk_corner_x + self.chunk_size
                            
                            
                            if bottom_right_z >= self.get_height() or bottom_right_x >= self.get_width():
                                pass #nevermind, I'm not drawing a pan chunk square for a chunk that's half off the world
                            else:
                                #okay we'll draw the pan chunk square
                                #color = random()*.5 +.5# for now we're just doing random colors
                                #color = [color, color, color]
                                
                                
                                color = self.get_floor_color(
                                    chunk_corner_x*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z,chunk_corner_x),
                                    chunk_corner_z*self.unit_length,
                                    (chunk_corner_x+self.chunk_size)*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z,chunk_corner_x+self.chunk_size),
                                    chunk_corner_z*self.unit_length,
                                    (chunk_corner_x+self.chunk_size)*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z+self.chunk_size,chunk_corner_x+self.chunk_size),
                                    (chunk_corner_z+self.chunk_size)*self.unit_length)
                                
                                
                                #make the chunk green
                                color_adjust = 0
                                for zz in range(chunk_corner_z, bottom_right_z):
                                    for xx in range(chunk_corner_x, bottom_right_x):
                                        if self.grid[zz][xx].tree_obj != None:
                                            color_adjust += .005
                                if color_adjust > .15: color_adjust = .25
                                if color_adjust > .1:
                                    color[1] -= color_adjust
                                    color[0] -= color_adjust*2
                                    color[2] -= color_adjust*2
                                if color[1] > 1: color[1] = 1
                                if color[0] < 0: color[2] = 0
                                if color[2] < 0: color[2] = 0
                                        
                                
                                
                                self.grid[chunk_corner_z][chunk_corner_x].chunk_vert_handler_index = self.vertex_handler.add_vertex(
                                    [chunk_corner_x*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z,chunk_corner_x),
                                    chunk_corner_z*self.unit_length]
                                    , color) 
                                _should_be_previous_plus_1 = self.vertex_handler.add_vertex(
                                    [(chunk_corner_x+self.chunk_size)*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z,chunk_corner_x+self.chunk_size),
                                    chunk_corner_z*self.unit_length]
                                    , color) 
                                _should_be_last_plus_2 = self.vertex_handler.add_vertex(
                                    [(chunk_corner_x+self.chunk_size)*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z+self.chunk_size,chunk_corner_x+self.chunk_size),
                                    (chunk_corner_z+self.chunk_size)*self.unit_length]
                                    , color) 
                                _should_be_plus_3 = self.vertex_handler.add_vertex(
                                    [(chunk_corner_x)*self.unit_length, 
                                    self.vertical_stretch * self.get_elevation(chunk_corner_z+self.chunk_size,chunk_corner_x),
                                    (chunk_corner_z+self.chunk_size)*self.unit_length]
                                    , color) 
                    
    def reset_floor_colors(self):
        for x in range(self.get_width()-1):
            for z in range(self.get_height()-1):
                self.grid[z][x].reset_floor_color()
    def get_floor_color_zx(self, z, x):
        return self.get_floor_color(
                        x*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z,x),
                        z*self.unit_length,
                        (x+1)*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z,x+1),
                        z*self.unit_length,
                        (x+1)*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z+1,x+1),
                        (z+1)*self.unit_length)
    def get_floor_color(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        hr, vr = normal.get_plane_rotation(x1,y1,z1,x2,y2,z2,x3,y3,z3)
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        sun = math.pi/4
        angle_distance_from_sun = normal.angle_distance(hr, sun)/math.pi
        inverse_angle_distance_from_sun = 1 - angle_distance_from_sun
        inverse_angle_distance_from_sun_m1_to_p1 = inverse_angle_distance_from_sun*2-1
        
        vertical_rotation_0_to_1 = vr/(math.pi/2)
        inverse_vertical_rotation_0_to_1 = 1 - vertical_rotation_0_to_1
        
        neutral_floor_color = .8
        extremity = .5
        
        color_value = neutral_floor_color + inverse_angle_distance_from_sun_m1_to_p1*inverse_vertical_rotation_0_to_1*extremity
        if color_value > 1: color_value = 1
        if color_value < 0: color_value = 0
        
        color = [color_value]*3
        return color
    def get_width(self):
        if len(self.grid) == 0:
            return 0
        return len(self.grid[0])
    def get_height(self):
        return len(self.grid)
    
    
    """
    Use set_elevation to change the elevation of any point
    If a coordinate outside of the world's bounds is given,
    the world will be automatically expanded
    """
    def set_elevation(self, z, x, elevation):
        #flat_floor_color = self.get_floor_color(0,0,0, 1,0,0, 0,0,1)
        while self.get_height() <= z:
            new_row = []
            new_color_row = []
            for i in range(self.get_width()):
                new_row.append(FloorVertex(x=i, z=self.get_height(), world=self))#elevation, floor first corner index in vertex handler, chunk floor first corner index in vertex handler,tree object
                #new_color_row.append(flat_floor_color)
            self.grid.append(new_row)
        
        
        while self.get_width() <= x:
            x_of_following_floor_vertices = self.get_width()
            for z in range(len(self.grid)):
                self.grid[z].append(FloorVertex(x=x_of_following_floor_vertices, z=z, world=self))
        ###
        self.grid[z][x].elevation = elevation
        if z % 100 == 0 and x == 0:
            print(z,x)
        ###
        self._update_quad(z, x) #update the quad that this vertex is responsible for (lower right)
        self._update_quad(z-1, x) #update the quad to the up right
        self._update_quad(z-1, x-1) #update the quad to the up left
        self._update_quad(z, x-1) #update the quad to the down left
    
    #only call this when you change the elevation of a point. Don't call to refresh line of sight
    #this function only updates the vertex handler if the quad is being displayed
    def _update_quad(self, z, x):
        #color = random()*.5 +.5# for now we're just doing random colors
        #color = [color, color, color]
        
        
        player_z = int(self.player.z/self.unit_length)#in units (not opengl coordinates; that's why we divide by unit_length)
        player_x = int(self.player.x/self.unit_length)
        
        #make sure that the point z,x ACTUALLY HAS a quad that it's responsible for. If not, just ignore this call
        #if we're on the last row or last column, this point actually isn't responsible for any quad
        if z >= 0 and x >= 0 and z < self.get_height()-1 and x < self.get_width()-1:
            
            #check if the square this vertex is responsible for is within the line of sight
            if (  ( (z-player_z)**2 + (x*-player_x)**2 ) ** .5  ) <= (self.player.line_of_sight):
                #So we are in the player's los
                
                #now check if this square is already added
                if self.grid[z][x].floor_vert_handler_index != None:
                    
                    #Okay so this square is already added. We just have to update the four vertexes
                    
                    
                    
                    color = [0,0,0]
                    self.vertex_handler.update_vertex(self.grid[z][x].floor_vert_handler_index,
                        [x*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z,x),#this confirms the height is up to date
                        z*self.unit_length]
                        , color) 
                    self.vertex_handler.update_vertex(self.grid[z][x].floor_vert_handler_index+1,
                        [(x+1)*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z,x+1),#this confirms the height is up to date
                        z*self.unit_length]
                        , color) 
                    self.vertex_handler.update_vertex(self.grid[z][x].floor_vert_handler_index+2,
                        [(x+1)*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z+1,x+1),#this confirms the height is up to date
                        (z+1)*self.unit_length]
                        , color) 
                    self.vertex_handler.update_vertex(self.grid[z][x].floor_vert_handler_index+3,
                        [(x)*self.unit_length, 
                        self.vertical_stretch * self.get_elevation(z+1,x),#this confirms the height is up to date
                        (z+1)*self.unit_length]
                        , color) 
                    
                

    def __str__(self):
        ret = "World: " + str(self.name) + "\n"
        ret += "Width: " + str(self.width) + "\n"
        ret += "Height: " + str(self.height) + "\n"
        
        for z in range(self.height):
            ret += str(self.grid[z]) + '\n'
            if z > 100:
                ret += "...\n"
                break
        return ret
    def get_elevation(self, z, x):
        return self.grid[z][x].elevation
    def get_real_elevation(self, z, x):
        return self.grid[z][x].elevation * self.vertical_stretch
    def grid_to_real(self, xz):
        return xz*self.unit_length + self.unit_length/2
    def real_to_grid(self, xz):
        return int((xz - self.unit_length/2)/self.unit_length)
    def subworld(self, z1, x1, z2, x2):
        w = World(self.name, x2-x1, z2-z1)
        
        
        
        w_z = 0
        w_x = 0
        for my_z in range(z1, z2):
            for my_x in range(x1, x2):
                #print(w_z,w_x)
                w.grid[w_z][w_x] = self.grid[my_z][my_x].copy_move(w_z, w_x)
                
                w_x += 1
            w_x = 0
            w_z += 1
            
        return w
    def smooth(self, z1, x1, z2, x2, strength=.8):
        new_elevations = array_2d(z2-z1, x2-x1)
        
        weight_this_vertex = 1-strength
        weight_each_other_vertex = (1-weight_this_vertex)/8
        
        print(z1, x1, z2, x2, self.get_width(), self.get_height())
        
        for z in range(z1, z2):
            for x in range(x1, x2):
                if z < 0 or z > self.get_height()-1 or x < 0 or x > self.get_width()-1:
                    continue
                if z == 0 or z == self.get_height()-1 or x == 0 or x == self.get_width()-1:
                    new_elevations[z-z1][x-x1] = self.get_elevation(z, x)
                    continue
                new_elevations[z-z1][x-x1] = (self.get_elevation(z, x) * weight_this_vertex 
                                                + self.get_elevation(z-1, x-1) * weight_each_other_vertex
                                                + self.get_elevation(z-1, x) * weight_each_other_vertex
                                                + self.get_elevation(z-1, x+1) * weight_each_other_vertex
                                                + self.get_elevation(z, x-1) * weight_each_other_vertex
                                                + self.get_elevation(z, x+1) * weight_each_other_vertex
                                                + self.get_elevation(z+1, x-1) * weight_each_other_vertex
                                                + self.get_elevation(z+1, x) * weight_each_other_vertex
                                                + self.get_elevation(z+1, x+1) * weight_each_other_vertex)
                                                
        for z in range(z1, z2):
            for x in range(x1, x2):
                if z < 0 or z > self.get_height()-1 or x < 0 or x > self.get_width()-1:
                    continue
                self.set_elevation(z, x, new_elevations[z-z1][x-x1])
    def add_tree(self, z, x):
        if z < 0 or x < 0 or z >= self.get_height() or x >= self.get_width():
            return
        t = Tree(z, x, self)
        chunk_corner_x = (x // self.chunk_size)* self.chunk_size
        chunk_corner_z = (z // self.chunk_size)* self.chunk_size
        chunk_center_x = (x // self.chunk_size)* self.chunk_size + self.chunk_size/2
        chunk_center_z = (z // self.chunk_size)* self.chunk_size + self.chunk_size/2
        
        self.grid[z][x].tree_obj = t
        #t.add_to_vertex_handler(self.vertex_handler)
    def add_trees(self, z1, x1, z2, x2, density=.5):
        for z in range(z1, z2):
            for x in range(x1, x2):
                if random() < density:
                    self.add_tree(z, x)
    def add_trees_elevation(self, z1, x1, z2, x2, density=.5):
        lowest = 999999999999999999999999999999999999
        highest = -999999999999999999999999999999999999
        for z in range(0, self.get_height()):
            for x in range(0, self.get_width()):
                if self.get_elevation(z, x) > highest:
                    highest = self.get_elevation(z, x)
                if self.get_elevation(z, x) < lowest:
                    lowest = self.get_elevation(z, x)
                    
        for z in range(z1, z2):
            for x in range(x1, x2):
                elevation = self.get_elevation(z, x)
                if highest-lowest == 0:
                    elevation_frac = .5
                else:
                    elevation_frac = (elevation-lowest)/(highest-lowest)
                if random() < density:
                    if random() > elevation_frac:
                        self.add_tree(z, x)
    def get_player_pointing(self):
        player = self.player
        hr = player.hor_rot
        vr = player.vert_rot
        step_size = .5
        ray = [player.x, player.y, player.z]
        while True:
            if ( (ray[0]-player.x)**2 + (ray[2]-player.z)**2 ) ** .5 > player.line_of_sight*self.unit_length + 2:
                return None
            grid_x = self.real_to_grid(ray[0])
            grid_z = self.real_to_grid(ray[2])
            
            if grid_x >= self.get_width()-1 or grid_z >= self.get_height()-1 or grid_x < 0 or grid_z < 0:
                pass#not inside world
            else:
                four_corners = [self.get_real_elevation(grid_z, grid_x), 
                    self.get_real_elevation(grid_z+1, grid_x), 
                    self.get_real_elevation(grid_z+1, grid_x+1), 
                    self.get_real_elevation(grid_z, grid_x+1)]
                highest = max(four_corners) + step_size*self.unit_length
                lowest = min(four_corners) - step_size*self.unit_length*3
                if ray[1] <= highest and ray[1] >= lowest: 
                    if self.grid[grid_z][grid_x].floor_vert_handler_index == None:
                        return None
                    else:
                        return grid_z, grid_x
                
            ray[0] += step_size*self.unit_length * math.cos(hr) * math.cos(vr)
            ray[2] += step_size*self.unit_length * -math.sin(hr) * math.cos(vr)
            ray[1] += step_size*self.unit_length * math.sin(vr)
                

def array_2d(rows, cols):
    ret = []
    for i in range(rows):
        ret.append([0]*cols)
    return ret


class FloorVertex:
    def __init__(self, x=0, z=0, world=None):
        self.elevation = 0
        self.z = z
        self.x = x
        
        self.world = world
        
        self.floor_vert_handler_index = None
        self.chunk_vert_handler_index = None
        
        self.tree_obj = None
        
        self.color = None#the color of the individual floor tile
    def reset_floor_color(self):
        self.color = self.world.get_floor_color_zx(self.z, self.x)
    def copy_move(self, z, x):
        
        ret = FloorVertex()
        
        ret.x = x
        ret.z = z
        
        x_moved = x - self.x
        z_moved = z - self.z
        
        ret.elevation = self.elevation
        
        ret.floor_vert_handler_index = self.floor_vert_handler_index
        ret.chunk_vert_handler_index = self.chunk_vert_handler_index
        
        ret.tree_obj = self.tree_obj.copy_move(self.tree_obj.z + z_moved, self.tree_obj.x + x_moved)
    
        return ret


class Chunk:
    def __init__(self, z, x, width, height):
        self.z = z
        self.x = x
        self.width = width#width as in number of vertices not number of squares
        self.height = height#height as in number of vertices not number of squares
        num_squares = (width-1) * (height-1) 
        
        
        """
        This is directly fed into the OPENGL draw arrays function, so this is
        literally all the corners of all the quadrilaterals in this chunk. Now,
        if you wanted to change the elevation of one vertex, you would actually
        have to change four items in this buffer array, because each point is 
        connected to four squares (unless on the edge of course)
        
        buffer is 1d array containing all the quads
        
        
        [
        quad 1 upper left, 
        quad 1 upper right, 
        quad 1 lower right, 
        quad 1 lower left, 
        quad 2 upper left, 
        quad 2 upper right, 
        quad 2 lower right, 
        quad 2 lower left... ]
        """
        self.chunk_points_buffer = numpy.zeros(num_squares * 4)
        self.chunk_colors_buffer = numpy.zeros(num_squares * 4)
    """
    conv 
    
    input z and x coordinates of a vertex within this chunk
    this outputs the list of all the indices in the chunk_points_buffer
    that correspond to this z x vertex. There are multiple because
    for each vertex, there may be multiple quadrilaterals that 
    touch it, so for each quadrilateral that touches it it is going
    to have to have its own array spot for that
    
    These vertices work for the points buffer and the colors buffer
    """
    def conv(self, z, x):
        ret = []
        up = z-1
        left = x-1
        down = z
        right = x
        
        #upper left quadrilateral
        if self.valid_quad(z-1, x-1):
            index_of_first_point_of_this_quad_in_2d_flatten_to_1d = ((z-1)*self.width + (x-1))*4 # *4 for four points in a square
            ret.append(index_of_first_point_of_this_quad_in_2d_flatten_to_1d + 2)#+2 because the lower right of the upper left quad is point z, x. lower right is the 3rd point (0,1,2...))
        #lower right
        if self.valid_quad(z, x):
            index_of_first_point_of_this_quad_in_2d_flatten_to_1d = ((z)*self.width + (x))*4
            ret.append(index_of_first_point_of_this_quad_in_2d_flatten_to_1d + 0)
        #lower left
        if self.valid_quad(z, x-1):
            index_of_first_point_of_this_quad_in_2d_flatten_to_1d = ((z)*self.width + (x-1))*4
            ret.append(index_of_first_point_of_this_quad_in_2d_flatten_to_1d + 1)
        #upper right
        if self.valid_quad(z-1, x):
            index_of_first_point_of_this_quad_in_2d_flatten_to_1d = ((z-1)*self.width + (x))*4
            ret.append(index_of_first_point_of_this_quad_in_2d_flatten_to_1d + 3)
        return ret
    
    
    """
    checks if a vertex is inside this chunk (starting at zero, zero for upper left corner
    """
    def valid_vertex(self, z, x):
        return z >= 0 and z < self.height and x >= 0 and x < self.width
    """
    checks if a vertex is inside this chunk (starting at zero, zero for upper left corner
    """
    def valid_quad(self, z, x):
        return z >= 0 and z < self.height-1 and x >= 0 and x < self.width-1
def main():
     c = Chunk(0,0, 3, 3)
     print(c.conv(1,1))


if __name__ == "__main__": main()