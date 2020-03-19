from pylooiengine import *
import PIL

import sys
from PIL import Image

import os

#locked. warning. if you run this code, it will require all saved world to run reset sun angle

def minus_extension(name):
    return name[0:name.rfind(".")]


###MAX XXX.PNG width is 14000, but at 9000 it starts to become slower
names = [
"Black.png",
"White.png", 
"MinecraftSnow-lighting-155.png",
"MinecraftSnow-lighting-159.png",
"MinecraftSnow-lighting-163.png",
"MinecraftSnow-lighting-167.png",
"MinecraftSnow-lighting-171.png",
"MinecraftSnow-lighting-175.png",
"MinecraftSnow-lighting-179.png",
"MinecraftSnow-lighting-183.png",
"MinecraftSnow-lighting-187.png",
"MinecraftSnow-lighting-191.png",
"MinecraftSnow-lighting-195.png",
"MinecraftSnow-lighting-199.png",
"MinecraftSnow-lighting-203.png",
"MinecraftSnow-lighting-207.png",
"MinecraftSnow-lighting-211.png",
"MinecraftSnow-lighting-215.png",
"MinecraftSnow-lighting-219.png",
"MinecraftSnow-lighting-223.png",
"MinecraftSnow-lighting-227.png",
"MinecraftSnow-lighting-231.png",
"MinecraftSnow-lighting-235.png",
"MinecraftSnow-lighting-239.png",
"MinecraftSnow-lighting-243.png",
"MinecraftSnow-lighting-247.png",
"MinecraftSnow-lighting-251.png",
"MinecraftSnow-lighting-255.png",
"IceTexture.png",
"BumpTextureD.png",
"BumpTextureL.png",
None,
"PineTexture1.png",
None,
"PineTexture2.png",
None,
"PineTexture3.png",
None,
"PineTexture4.png",
None,
"Bark.png",
"CliffTexture.png",
"RockTexture.png",
"BuildingStoneTexture.png",
"BuildingWoodTexture.png",
"BuildingWoodTexture2.png",
"DoorTexture.png"
]
n = []
for name in names:
    #if not name.startswith("Ice"):
    n.append(name)
names = n

blank_space = Image.new('RGBA', (8, 150))
blank_space.paste( (1,1,1,0), [0,0,blank_space.size[0],blank_space.size[1]])


images = [blank_space if x==None else Image.open("3d_textures/"+x) for x in names]




widths, heights = zip(*(i.size for i in images))


total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGBA', (total_width, max_height))
new_im.paste( (1,1,1,1), [0,0,new_im.size[0],new_im.size[1]])



key = str(total_width)+"_"+str(max_height)
x_offset = 0
for i in range(len(images)):
    im = images[i]
    new_im.paste(im, (x_offset,0))
    if names[i] != None:
        key+="\n"+minus_extension(names[i])+"_"+str(x_offset)+"_0_"+str(widths[i])+"_"+str(heights[i])
    x_offset += im.size[0]
    

new_im.save("XXX.png")
f = open("key.txt","w")
f.write(key)
f.close()

#https://sta
            
                
