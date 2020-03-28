import loading
shadow_margin = .09

#every real unit of length is equal to D shadow units of length
D = 1
from time import sleep

#triangle functions
def about(a,b):
    return a + .01 > b and a - .01 < b
def abs(x):return x if x > 0 else -x
def area(z1,x1,z2,x2,z3,x3):
    return abs( (z1*(x2-x3) + z2*(x3-x1) + z3*(x1-x2))/2 )
def is_inside(x,y,x1,y1,x2,y2,x3,y3):
    A = area (x1, y1, x2, y2, x3, y3) 
    A1 = area (x, y, x2, y2, x3, y3) 
    A2 = area (x1, y1, x, y, x3, y3)
    A3 = area (x1, y1, x2, y2, x, y)
    return about(A , (A1 + A2 + A3))
#shadow map class
class ShadowMap:
    def __init__(self, world):
        self.world = world
        
        #shadow map
        #keys are tuples representing the shadow grid coordinates
        #each value is tuple
            #first element is the vertex handler key
            #second element is an array containing all the objects that have shadows here
            #every 4 rows in shadow grid is the same space as 1 "real" distance unit in the world
        self.shadow_map = {}
        
        
    def get_shadow_color(self, z, x):
        hs = self.world.properties["horizontal_stretch"]
        try:
            
            color = self.world.get_proper_floor_color(int(z/D/hs),int(x/D/hs))
        except:
            print("bad",z,x)
            color = [.8,.8,.8]
        color[0] -= .25
        color[1] -= .25
        color[2] -= .25
        return color
    #only called by add_one_shadow
    #do not call this from outside
    def add_one_shadow_quad(self, z, x):
        z1 = z/D
        z2 = (z+1)/D
        x1 = x/D
        x2 = (x+1)/D
        w=self.world
        
        hs = self.world.properties["horizontal_stretch"]
        vs = self.world.properties["vertical_stretch"]
        
        
        if z1<0 or x1<0 or not w.valid_floor(int(z1/hs),int(x1/hs)):return None
        return self.world.add_fixed_quad(
            [x1,w.get_elevation_continuous(z1/hs,x1/hs)*vs+shadow_margin,z1],
            [x2,w.get_elevation_continuous(z1/hs,x2/hs)*vs+shadow_margin,z1],
            [x2,w.get_elevation_continuous(z2/hs,x2/hs)*vs+shadow_margin,z2],
            [x1,w.get_elevation_continuous(z2/hs,x1/hs)*vs+shadow_margin,z2],
            self.get_shadow_color(z,x),
            int(z1/hs),
            int(x1/hs))
    
    def add_one_shadow(self, z, x, object):
        if (z,x) not in self.shadow_map:
            key = self.add_one_shadow_quad(z, x)
            self.shadow_map[(z,x)] = (key,[object])
        else:
            if object not in self.shadow_map[z,x][1]:
                self.shadow_map[z,x][1].append(object)
            key = self.shadow_map[z,x][0]
        return key
    
    def remove_one_shadow(self, z, x, object):
        if (z,x) not in self.shadow_map: return
        if object not in self.shadow_map[z,x][1]: return
        self.shadow_map[z,x][1].remove(object)
        if len(self.shadow_map[z,x][1]) == 0:
            hs = self.world.properties["horizontal_stretch"]
            self.world.remove_fixed_quad(self.shadow_map[z,x][0], (z/D)/hs, (x/D)/hs)
            del self.shadow_map[z,x]
    
    def add_triangle_shadow(self, z1, x1, z2, x2, z3, x3, object):
        zs = [z1,z2,z3]
        xs = [x1,x2,x3]
        min_z = int(min(zs))-1
        min_x = int(min(xs))-1
        max_z = int(max(zs))+1
        max_x = int(max(xs))+1
        

        
        ret = []
        
        for z in range(min_z, max_z):
            for x in range(min_x, max_x):
                if is_inside(z,x,z1,x1,z2,x2,z3,x3):
                    ret.append(self.add_one_shadow(z,x,object))
        return ret
    def remove_triangle_shadow(self, z1, x1, z2, x2, z3, x3, object):
        zs = [z1,z2,z3]
        xs = [x1,x2,x3]
        min_z = int(min(zs))-1
        min_x = int(min(xs))-1
        max_z = int(max(zs))+1
        max_x = int(max(xs))+1
        
        ret = []
        
        for z in range(min_z, max_z):
            for x in range(min_x, max_x):
                if is_inside(z,x,z1,x1,z2,x2,z3,x3):
                    self.remove_one_shadow(z,x,object)
        return ret
    def add_quad_shadow(self,z1,x1,z2,x2,z3,x3,z4,x4,object):
        self.add_triangle_shadow(z1,x1,z2,x2,z3,x3,object)
        self.add_triangle_shadow(z1,x1,z4,x4,z3,x3,object)
    def remove_quad_shadow(self,z1,x1,z2,x2,z3,x3,z4,x4,object):
        self.remove_triangle_shadow(z1,x1,z2,x2,z3,x3,object)
        self.remove_triangle_shadow(z1,x1,z4,x4,z3,x3,object)
    def update_shadows(self):
        loading.progress_bar("Updating shadows...")
        i = 0
        for z,x in self.shadow_map:
            z1 = z/D
            z2 = (z+1)/D
            x1 = x/D
            x2 = (x+1)/D
            w=self.world
            
            hs = self.world.properties["horizontal_stretch"]
            vs = self.world.properties["vertical_stretch"]
            
            
            anchor_z, anchor_x = int(z1/hs),int(x1/hs)
            if z1<0 or x1<0 or not w.valid_floor(anchor_z, anchor_x):continue
            
            chunk_z, chunk_x = self.world.convert_to_chunk_coords(anchor_z, anchor_x)
            v = self.world.chunks[chunk_z][chunk_x].vh.vertices
            c = self.world.chunks[chunk_z][chunk_x].vh.vertex_colors
            key = self.shadow_map[z,x][0]
            
            """
            v[key] = [x1,w.get_elevation_continuous(z1/hs,x1/hs)*vs+shadow_margin,z1]
            v[key+1] = [x2,w.get_elevation_continuous(z1/hs,x2/hs)*vs+shadow_margin,z1]
            v[key+2] = [x2,w.get_elevation_continuous(z2/hs,x2/hs)*vs+shadow_margin,z2]
            v[key+3] = [x1,w.get_elevation_continuous(z2/hs,x1/hs)*vs+shadow_margin,z2]
            """
            
            
            v0y = w.get_elevation_continuous(z1/hs,x1/hs)*vs+shadow_margin
            v1y = w.get_elevation_continuous(z1/hs,x2/hs)*vs+shadow_margin
            v2y = w.get_elevation_continuous(z2/hs,x2/hs)*vs+shadow_margin
            v3y = w.get_elevation_continuous(z2/hs,x1/hs)*vs+shadow_margin
            
            
            changed = False
            if v[key+0][1] != v0y: 
                v[key+0][1] = v0y
                changed = True
            if v[key+1][1] != v1y: 
                v[key+1][1] = v1y
                changed = True
            if v[key+2][1] != v2y: 
                v[key+2][1] = v2y
                changed = True
            if v[key+3][1] != v3y: 
                v[key+3][1] = v3y
                changed = True
            
            
            if changed:
                color = self.get_shadow_color(z,x)
                c[key][0] = color[0]
                c[key][1] = color[1]
                c[key][2] = color[2]
                c[key+1][0] = color[0]
                c[key+1][1] = color[1]
                c[key+1][2] = color[2]
                c[key+2][0] = color[0]
                c[key+2][1] = color[1]
                c[key+2][2] = color[2]
                c[key+3][0] = color[0]
                c[key+3][1] = color[1]
                c[key+3][2] = color[2]
            
            
            if i % 1000 == 0: loading.update(i/len(self.shadow_map)*100)
            
            i += 1
        loading.update(100)
            
            
def strict_in(item, list_):
    for x in list_:
        if x is item:
            return True
    return False
def strict_remove(item, list_):
    for i in range(len(list_)):
        if list_[i] is item:
            del list_[i]
            return
    raise Exception("Item " + str(item) + " is not in the list. Cannot remove anything")
