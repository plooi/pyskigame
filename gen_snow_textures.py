from PIL import Image
from random import random
from shading import *

for i in range(87,256,4):
    file = "3d_textures/MinecraftSnow-lighting-%d.png"%(i,)
    img = Image.new('RGBA', (32,32))
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            a = 255
            shade = i
            
            shade = shade + random() * 1.5 - .75
            color = apply_color(shade)
            
            
            
            pixels[x,y] = color[0],color[1],color[2],a
    img.save(file)
"""
for i in range(155,256,4):
    file = "MinecraftSnow-lighting-%d.png"%(i,)
    img = Image.open(file)
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r,g,b,a = pixels[x,y]
            b += -(((i-155)/(256-155)-.5)*2+1)*7
            b=int(b)
            if b > 255: b = 255
            if b < 0: b = 0
            
            pixels[x,y] = r,g,b,a
    img.save(file)


"""
