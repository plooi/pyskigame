from pylooiengine.misc.graphics import VertexHandler
from pylooiengine import *
from random import random

texture_id = None

#start texture loading
key = "key.txt"
tex = image("XXX.png")
tex_b = tex.tobytes("raw", "RGBA", 0, -1)

texture_dictionary = {}#input texture name, returns opengl coordinates of this texture where it lies on the master image

f = open(key)
i = 0
for line in f:
    if i == 0:
        wh = line.split("_")
        totalw = int(wh[0])
        totalh = int(wh[1])
    else:
        arr = line.split("_")
        height = int(arr[-1])
        width = int(arr[-2])
        y = int(arr[-3])
        x = int(arr[-4])
        arr = arr[0:-4]
        texname = "".join(arr)
        if texname not in texture_dictionary:
            texture_dictionary[texname] = [[x/totalw,1.0], [(x+width)/totalw,1.0], [(x+width)/totalw,1-height/totalh], [x/totalw,1-height/totalh]]
    i+=1
f.close()


#end texture loading
print(texture_dictionary)

def add_image_to_vertex_handler(vh, p1, p2, p3, p4, image_name, texture_dict=texture_dictionary):
    coords = texture_dict[image_name]
    ret = vh.add_vertex(p1,coords[0])
    vh.add_vertex(p2,coords[1])
    vh.add_vertex(p3,coords[2])
    vh.add_vertex(p4,coords[3])
    return ret
def remove_image_from_vertex_handler(vh, key):
    vh.rm_vertex(key)
    vh.rm_vertex(key+1)
    vh.rm_vertex(key+2)
    vh.rm_vertex(key+3)
    
#sets the whole quad's texture
def set_texture(vh, index, image_name, texture_dict=texture_dictionary):
    coords = texture_dict[image_name]
    vh.vertex_colors[index] = coords[0]
    vh.vertex_colors[index+1] = coords[1]
    vh.vertex_colors[index+2] = coords[2]
    vh.vertex_colors[index+3] = coords[3]
    


def new_texture_handler(initial_capacity=2):
    return VertexHandler(3, color_size=2, initial_capacity=initial_capacity)




class TextureBinder(LooiObject):
    def __init__(self):
        super().__init__()
        self.setup_tex = True
    def upon_resize(self):
        self.setup_tex = True
    def step(self):
        global texture_id
        if self.setup_tex:
            ix, iy, img = tex.size[0], tex.size[1], tex_b
            ID = glGenTextures(1)
            
            texture_id = ID
            
            glBindTexture(GL_TEXTURE_2D, ID)
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            
            
            glTexImage2D(
                GL_TEXTURE_2D, 0, 4, ix, iy, 0,
                GL_RGBA, GL_UNSIGNED_BYTE, img
            )
            self.setup_tex = False
    def deactivate(self):
        pass
TextureBinder()
