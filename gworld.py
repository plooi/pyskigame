import world
from world import *
import shading


class GWorld(World):
    def __init__(self):
        super().__init__()
    def init(self, name, width, height, more_properties={}, elevation_function=lambda z,x:0, view=None, prog_bar=True, natural_bumps=True):
        self.quads = []
        self.chunks = []
        self.pan_chunk_squares = None
    
    
        if prog_bar: loading.progress_bar("Loading 1/2")
        
        
        #set properties properly
        for property in more_properties:
            self.properties[property] = more_properties[property]
        self.properties["name"] = name
        self.properties["width_chunks"] = int(width/self.properties["chunk_size"])
        self.properties["height_chunks"] = int(height/self.properties["chunk_size"])
        self.properties["width"] = self.properties["width_chunks"]*self.properties["chunk_size"]
        self.properties["height"] = self.properties["height_chunks"]*self.properties["chunk_size"]
        if view != None: self.view = view
        
        """
        mobile drawables are stored in these arrays
        
        "mobile" refers to, it can move. So once this paint iteration completes and all the
        mobile vertices are drawn with their corresponding colors, all the mobile vertices
        are DELETED, so that on the next iteration you can add the vertices and colors in
        again, but if they've changed that's okay cuz that's why we add fresh ones every time
        
        However, don't make everything a mobile vertex because mobile vertices are slower than static ones
        """
        self.mobile_vertices_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors_close = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_vertices_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.mobile_colors_far = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        
        #initialize all chunks
        for z in range(self.properties["height_chunks"]):
            row = []
            for x in range(self.properties["width_chunks"]):
                c = Chunk(self)
                
                row.append(c)
            self.chunks.append(row)
            
        
        self.list_mode()
        
        
        vs = self.properties["vertical_stretch"]
        
        elevation_function_orig = elevation_function
        elevation_function = lambda z,x: elevation_function_orig(z,x)*vs
        
        t1 = time()
        
        
        
        #initialize quads 
        for z in range(self.properties["height"]):
            row = []
            self.quads.append(row)
            for x in range(self.properties["width"]):
                #actually create the quad object
                row.append(Quad())#add the quad object to the self.quads
        
        #fill the quads with data
        for z in range(self.properties["height"]):
            for x in range(self.properties["width"]):
                z_chunk, x_chunk = self.convert_to_chunk_coords(z, x)#find which chunk this quad z,x is in
                
                q=self.quads[z][x]
                q.my_chunk_z = z_chunk#set properly which chunk it belongs to
                q.my_chunk_x = x_chunk
                
                vh = self.chunks[z_chunk][x_chunk].vh
                
                hs = self.properties["horizontal_stretch"]
                
                #allocate memory for the quad that is going to be drawn and
                #set all the elevations to what the elevation function wants
                q.floor_pointer = vh.add_vertex([x*hs,elevation_function(z,x),z*hs])
                vh.add_vertex([(x+1)*hs,elevation_function(z, x+1),z*hs])
                vh.add_vertex([(x+1)*hs,elevation_function(z+1, x+1),(z+1)*hs])
                vh.add_vertex([x*hs,elevation_function(z+1, x),(z+1)*hs])
            if prog_bar and z % 25 == 0: loading.update(z/self.properties["height"]*50)
        #reset floor textures
        #by the way, having this as it's own loop increased performance by 15%
        for z in range(self.properties["height"]):
            for x in range(self.properties["width"]):
                self.reset_floor_texture(z, x)
            if prog_bar and z % 25 == 0: loading.update(z/self.properties["height"]*50+50)
            
        #print("loading 1/3 took",time() - t1)
        
        """
        do not worry about allocating all the pan chunk squares
        they will be allocated during the step function
        """
                
        
        
        
        #other stuff
        self.fps = FPS(0)
        self.add(self.fps)
        
        
        
        
        #initialize the natural bumps
        if prog_bar: loading.update(100)
        if natural_bumps:
            world_operations.natural_bumps(self, 0,0,self.get_height_points(), self.get_width_points(), prog_bar=True)
        
        
        return self
        #END INIT
    def reset_floor_texture(self, floor_z, floor_x):
        shade = self.get_proper_floor_color(floor_z, floor_x)[0]
        #shade = self.get_proper_floor_shade(floor_z, floor_x)
        #floor = self.quads[floor_z][floor_x]
        
        color = shading.apply_color(conv_87_255(shade),scale="0-1")
        
        #print("color",color)
        self.set_floor_texture(floor_z, floor_x, color)
    
    def set_floor_texture(self, floor_z, floor_x, color):
        check(self.valid_floor(floor_z, floor_x))
        
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        if floor_z == self.get_height_floors()-1:
            floor = self.quads[floor_z][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+2] = color
            chunk.vh.vertex_colors[floor.floor_pointer+3] = color
            chunk.colors_changed = True
            self.pan_chunk_squares_changed = True
        if floor_x == self.get_width_floors()-1:
            floor = self.quads[floor_z][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+1] = color
            chunk.vh.vertex_colors[floor.floor_pointer+2] = color
            chunk.colors_changed = True
            self.pan_chunk_squares_changed = True
        if self.valid_floor(floor_z, floor_x):
            floor = self.quads[floor_z][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer] = color
            chunk.colors_changed = True
            self.pan_chunk_squares_changed = True
        if self.valid_floor(floor_z-1, floor_x):
            floor = self.quads[floor_z-1][floor_x]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+3] = color
            chunk.colors_changed = True
            self.pan_chunk_squares_changed = True
        if self.valid_floor(floor_z-1, floor_x-1):
            floor = self.quads[floor_z-1][floor_x-1]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+2] = color
            chunk.colors_changed = True
            self.pan_chunk_squares_changed = True
        if self.valid_floor(floor_z, floor_x-1):
            floor = self.quads[floor_z][floor_x-1]
            chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
            chunk.vh.vertex_colors[floor.floor_pointer+1] = color
            chunk.colors_changed = True
            self.pan_chunk_squares_changed = True
    
    """
    get_elevation
    
    finds the UNSCALED elevation of the POINT z, x that you input
        must unscale the elevation
    """
    def get_elevation(self, z, x, scaled=False):
        x = int(x)
        z = int(z)
        if z < 0: z = 0
        if x < 0: x = 0
        if z >= self.get_height_points(): z = self.get_height_points()-1
        if x >= self.get_width_points(): x = self.get_width_points()-1
        
        if z > 0 and x > 0:
            #for all the points not in first column or row
            chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x-1)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z-1][x-1].floor_pointer
            point = chunk_obj.vh.vertices[floor_pointer+2]#+2 for lower right
            return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
        else:
            #we must be in the first row, or first column, or both
            if x == 0 and z == 0:
                chunk_z, chunk_x = self.convert_to_chunk_coords(0, 0)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[0][0].floor_pointer
                point = chunk_obj.vh.vertices[floor_pointer+0]#+0 for upper left
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
            elif x == 0:
                chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, 0)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z-1][0].floor_pointer
                point = chunk_obj.vh.vertices[floor_pointer+3]#+3 for lower left
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
            elif z == 0:
                #for all the points not in first column or row
                chunk_z, chunk_x = self.convert_to_chunk_coords(0, x-1)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[0][x-1].floor_pointer
                point = chunk_obj.vh.vertices[floor_pointer+1]#+1 for upper right right
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
            else:
                raise Exception("Impossible!"+str(z)+" " + str(x))
            
        """
            
        
        if z < self.get_height_floors() and x < self.get_width_floors():#is the point we're looking for NOT on the last row or col?
            #then we can just find the corresponding floor z, x and get it's upper left hand corner 
            chunk_z, chunk_x = self.convert_to_chunk_coords(z, x)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z][x].floor_pointer
            point = chunk_obj.vh.vertices[floor_pointer+0]#+0 for upper left
            return point[1] if scaled else point[1]/self.properties["vertical_stretch"]#1 for the y elevation
        else:# we are either on the last row, or the last column, or both
            #so we will have to access other corners and be smart about it
            if x == 0:#then we are on the last row, first (0th) column
                #so ill just go to that floor and get the lower left point
                chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z-1][x].floor_pointer
                point = chunk_obj.vh.vertices[floor_pointer+3]#+0 for lower left
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]
            elif z == 0:#then we are on the last column, first (0th) row
                #so ill just go to that floor and get the upper right point
                chunk_z, chunk_x = self.convert_to_chunk_coords(z, x-1)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z][x-1].floor_pointer
                point = chunk_obj.vh.vertices[floor_pointer+1]#+1 for upper right
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]
            else:#then we can just go to the corresponding floor z-1,x-1 and get it's lower right corner
                chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x-1)
                chunk_obj = self.chunks[chunk_z][chunk_x]
                floor_pointer = self.quads[z-1][x-1].floor_pointer
                point = chunk_obj.vh.vertices[floor_pointer+2]#+1 for lower right
                return point[1] if scaled else point[1]/self.properties["vertical_stretch"]
        """
    
  
    """
    set_elevation
    
    void set_elevation(z, x, unscaled_elevation, reset_color?)
        goes to the quadrilateral array and finds the four (or fewer) quadrilaterals that are touching 
            this point
        using the information inside each quadrilateral,
            finds out which indexes inside which chunk's numpy buffer need to be modified
        scales the elevation
        gives the elevation to the right chunks at the right indexes
        
        recolor if requested
    
    
    UNTESTED
    """
    def set_elevation(self, z, x, elevation, reset_color=True, delete_trees=False):
        #print("set")
        elevation *= self.properties["vertical_stretch"]
        
        #upper left floor
        if self.valid_floor(z-1, x-1):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x-1)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z-1][x-1].floor_pointer
            point = chunk_obj.vh.vertices[floor_pointer+2]#+2 for upper left floor's LOWER RIGHT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z-1,x-1)
                
            if delete_trees:
                i=0
                while i < len(self.quads[z-1][x-1].containedObjects):
                    obj = self.quads[z-1][x-1].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
            
        #upper right floor
        if self.valid_floor(z-1, x):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z-1, x)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z-1][x].floor_pointer
            point = chunk_obj.vh.vertices[floor_pointer+3]#+3 for upper right floor's LOWER LEFT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z-1,x)
            if delete_trees:
                i=0
                while i < len(self.quads[z-1][x].containedObjects):
                    obj = self.quads[z-1][x].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
            
        #lower right floor
        if self.valid_floor(z, x):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z, x)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z][x].floor_pointer
            point = chunk_obj.vh.vertices[floor_pointer+0]#+0 for lower right floor's UPPER LEFT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z,x)
            if delete_trees:
                i=0
                while i < len(self.quads[z][x].containedObjects):
                    obj = self.quads[z][x].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
            
        #lower left floor
        if self.valid_floor(z, x-1):
            chunk_z, chunk_x = self.convert_to_chunk_coords(z, x-1)
            chunk_obj = self.chunks[chunk_z][chunk_x]
            floor_pointer = self.quads[z][x-1].floor_pointer
            point = chunk_obj.vh.vertices[floor_pointer+1]#+1 for upper left floor's UPPER RIGHT point
            point[1] = elevation
            
            if reset_color:
                self.reset_floor_texture(z,x-1)
            if delete_trees:
                i=0
                while i < len(self.quads[z][x-1].containedObjects):
                    obj = self.quads[z][x-1].containedObjects[i]
                    if isinstance(obj,Tree) or isinstance(obj, Bump) or isinstance(obj, WorldObject):
                        obj.delete()
                        i -= 1
                    i+=1
                        
    """
    get_proper_floor_color
    
    goes to the correct quadrilateral z,x
    looks at the four corners and calculates color based on angle
    gets the corresponding chunk's vertex handler
    uses the indices of the four corners to set the color to the new color in the vertex handler
    """
    def get_proper_floor_color(self, floor_z, floor_x, consider_ice=True):
        
        #find the floor object and the chunk object
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        
        #find the coordinates of all the 
        ul = chunk.vh.vertices[floor.floor_pointer]
        ur = chunk.vh.vertices[floor.floor_pointer+1]
        lr = chunk.vh.vertices[floor.floor_pointer+2]
        ll = chunk.vh.vertices[floor.floor_pointer+3]
        
        #find hr and vr or the floor so we can use that to calculate the color
        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ur[0],ur[1],ur[2],lr[0],lr[1],lr[2])
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        
        
        
        color1 = self.calculate_floor_color(hr, vr)
        """
        #cut short here
        return color1
        ##BUTT! Although it loads faster now, it will have just a bit less shading accuracy especially on those non-planar quads
        
        ...
        
        
        No, I want it to have full color accuracy
        """
        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ll[0],ll[1],ll[2],lr[0],lr[1],lr[2])
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        color2 = self.calculate_floor_color(hr, vr)
        
        
        ret = [(color1[0]+color2[0])/2, (color1[1]+color2[1])/2, (color1[2]+color2[2])/2]
        
        return ret
    def get_rotation(self, floor_z, floor_x):
    
        #find the floor object and the chunk object
        floor = self.quads[floor_z][floor_x]
        chunk = self.chunks[floor.my_chunk_z][floor.my_chunk_x]
        
        
        #find the coordinates of all the 
        ul = chunk.vh.vertices[floor.floor_pointer]
        ur = chunk.vh.vertices[floor.floor_pointer+1]
        lr = chunk.vh.vertices[floor.floor_pointer+2]
        ll = chunk.vh.vertices[floor.floor_pointer+3]
        
        #find hr and vr or the floor so we can use that to calculate the color
        hr, vr = normal.get_plane_rotation(ul[0],ul[1],ul[2],ur[0],ur[1],ur[2],lr[0],lr[1],lr[2])
        if vr < 0:
            vr = -vr
            hr = hr + math.pi
            
        return hr,vr
