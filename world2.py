






from pylooiengine import *
from pylooiengine.misc.graphics import VertexHandler
import math
import pylooiengine
import easygui
import rooms #UNCOMMENT THIS PLEASE!
import normal
import copy
from tree import Tree


#for testing




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
    def __init__(self, name, width, height, player=None, unit_length = 2, vertical_stretch = .15, chunk_size = 8):
        super().__init__(active=False)
        self.unit_length = unit_length
        self.vertical_stretch = vertical_stretch
        self.vertex_handler = VertexHandler(3)
        self.chunk_size = chunk_size
        self.mobile_vertices = []
        self.mobile_colors = []
        self.name = name
        self.grid = Grid().init(height, width)
        
        self.line_of_sight_update_box_size_scalar = 1.6 #as you move, you can turn off and on squares in the box
            #defined by player's line of sight TIMES line_of_sight_update_box_size_scalar
            #if it's too small (like .5) then the tiles farthest away aren't gonna get turned off and on
            #properly because we're not checking them
        
        
        
        #create player
        self.player = MapEditorPlayer() if player == None else player
        self.player.world = self
        self.player.deactivate()
        self.add(self.player)
        
        
        
        self.add(FPS(0))
        
        
        
        #setup_3d
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
        points, colors = self.grid.draw(self.get_chunk_load_grid())
        self.draw_quad_array_3d(points, colors, setup_3d=self.setup_3d)
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
            print("This should eventually be an entirely different pause menu")
            if result == 0:
                rooms.main_menu()
    
    """
    adds a mobile quad
    """
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
    
    
    
    def get_chunk_load_grid(self):
        #find which chunk the player is in
        ret = []
        for z in range(self.grid.height()):
            row = [0] * self.grid.width()
            ret.append(row)
        
        player_z, player_x = zx_to_chunk_zx(self.player.z, self.player.x)#IN CHUNKS, NOT BLOCKS
        
        #find all chunks within player's los
        
        los = self.player.los #IN CHUNKS NOT BLOCKS
        for z in range(player_z-los, player_z+los):
            for x in range(player_x-los, player_x+los):
                if ( (z-player_z)**2 + (x-player_x)**2 ) <= los: #pythagorean theorem
                    ret[z][x] = 1
        return ret
        
                    
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

    

    def __str__(self):
        ret = "World: " + str(self.name) + "\n"
        ret += "Width: " + str(self.grid.get_width()) + "\n"
        ret += "Height: " + str(self.grid.get_height()) + "\n"
        
        return ret
    def get_elevation(self, z, x):
        return self.grid.get_elevation(z, x)
    def get_real_elevation(self, z, x):
        return self.grid.get_elevation(z, x) * self.grid.vertical_stretch
    def grid_to_real(self, xz):
        return xz*self.unit_length + self.unit_length/2
    def real_to_grid(self, xz):
        return int((xz - self.unit_length/2)/self.unit_length)
    
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
    def __init__(self, world, z, x, width, height, color_size=3):
        self.world = world
        self.z = z
        self.x = x
        self.width = width#width as in number of vertices not number of squares
        self.height = height#height as in number of vertices not number of squares
        num_squares = (width-1) * (height-1) 
        
        self.color_size = color_size
        
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
        self.chunk_points_buffer = numpy.zeros([num_squares * 4, 3])
        self.chunk_colors_buffer = numpy.zeros([num_squares * 4, self.color_size])
    """
    quad_conv 
    
    input z and x coordinates of a quad within this chunk
    this outputs the list of all the indices in the chunk_points_buffer
    that are the four corners of this quad. 
    
    These indices work for the points buffer and the colors buffer
    """
    def quad_conv(self, z, x):
        index_of_first_point_of_this_quad_in_2d_flatten_to_1d = (z*self.width + x) * 4
        
        return [
        index_of_first_point_of_this_quad_in_2d_flatten_to_1d,
        index_of_first_point_of_this_quad_in_2d_flatten_to_1d+1,
        index_of_first_point_of_this_quad_in_2d_flatten_to_1d+2,
        index_of_first_point_of_this_quad_in_2d_flatten_to_1d+3
        ]
    """
    conv 
    
    input z and x coordinates of a vertex within this chunk
    this outputs the list of all the indices in the chunk_points_buffer
    that correspond to this z x vertex. There are multiple because
    for each vertex, there may be multiple quadrilaterals that 
    touch it, so for each quadrilateral that touches it it is going
    to have to have its own array spot for that
    
    These indices work for the points buffer and the colors buffer
    """
    def conv(self, z, x):
        if not self.valid_vertex(z, x):
            raise Exception("Invalid vertex %d %d" %(z, x))
        ret = []
        
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
    
    
    """
    set_elevation
    
    sets the elevation of point z x in this chunk to the value
    given by "elevation". You input a NON-SCALED elevation, and 
    this function will automatically scale it for you (scales
    by the elevation scaling factor in self.world)
    
    the corresponding bytes in the chunk points buffer will be
    set to the proper values
    """
    def set_elevation(self, z, x, elevation, recolor=True):
        buffer_indices = self.conv(z, x)
        for index in buffer_indices:
            self.chunk_points_buffer[index] = [self.world.scale_x(x), self.world.scale_elevation(elevation), self.world.scale_z(z)]
        if recolor:
            if valid_quad(z-1, x-1): self.reset_color(z-1, x-1)
            if valid_quad(z, x-1): self.reset_color(z, x-1)
            if valid_quad(z-1, x): self.reset_color(z-1, x)
            if valid_quad(z, x): self.reset_color(z, x)
    """
    get_elevation
    
    returns the NON-SCALED elevation value at the point z x
    """
    def get_elevation(self, z, x):
        buffer_indices = self.conv(z, x)
        index = buffer_indices[0]
        return self.world.unscale_elevation(self.chunk_points_buffer[index][1]) #1 for y in [x, y, z]
    """
    reset_color
    
    input the z x coordinates of a quadrilateral and then
    the color bytes in the color buffer will be automatically
    set to whatever is the correct color depending on the floor's
    orientation
    """
    def reset_color(self, z, x):
        color = self.world.get_floor_color_zx(z, x)
        indices = self.quad_conv(z, x)
        for index in indices:
            self.chunk_colors_buffer[index] = color
            
        
def main():
     c = Chunk(0,0, 3, 3)
     print(c.conv(1,1))
if __name__ == "__main__": main()
