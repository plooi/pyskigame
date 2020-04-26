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
"MinecraftSnow-lighting-243.png",
"MinecraftSnow-lighting-219.png",
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
"SnowTex40Clear.png",
"SnowTex40Blurry.png",
"SnowTex35Blurry.png",
"SnowTex30Blurry.png",
"SnowTex25Blurry.png",
"SnowTex20Blurry.png",
"SnowTex15Blurry.png",
"SnowTex10Blurry.png",
"SnowTex05Blurry.png",
None,
"Bark.png",
"CliffTexture.png",
"RockTexture.png",
"BuildingStoneTexture.png",
"BuildingWoodTexture.png",
"BuildingWoodTexture2.png",
"DoorTexture.png",
"Cloud1.png",
"Cloud2.png",
"Cloud3.png",
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
            
                
