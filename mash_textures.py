from pylooiengine import *
import PIL

import sys
from PIL import Image

import os



def minus_extension(name):
    return name[0:name.rfind(".")]


###MAX XXX.PNG width is 14000, but at 9000 it starts to become slower
names = os.listdir("3d_textures/")
n = []
for name in names:
    #if not name.startswith("Ice"):
    n.append(name)
names = n

images = [Image.open("3d_textures/"+x) for x in names]

widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

key = str(total_width)+"_"+str(max_height)
x_offset = 0
for i in range(len(images)):
    im = images[i]
    new_im.paste(im, (x_offset,0))
    key+="\n"+minus_extension(names[i])+"_"+str(x_offset)+"_0_"+str(widths[i])+"_"+str(heights[i])
    x_offset += im.size[0]
    

new_im.save("XXX.png")
f = open("key.txt","w")
f.write(key)
f.close()

#https://sta
            
                
