from PIL import Image
from random import random


for i in range(155,256,4):
    file = "MinecraftSnow-lighting-%d.png"%(i,)
    img = Image.new('RGBA', (32,32))
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            a = 255
            r = i
            g = i
            b = i
            
            p = random() * 1.5 - .75
            
            r += p
            g += p
            b += p
            
            
            
            b += -(((i-155)/(256-155)-.5)*2-1)*7#for the yellow-blue transition
            
            
            r = int(r)
            g = int(g)
            b = int(b)
            
            
            
            
            
            if r > 255:r = 255
            if r < 0: r = 0
            if g > 255:g = 255
            if g < 0: g = 0
            if b > 255:b = 255
            if b < 0: b = 0
            
            pixels[x,y] = r,g,b,a
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
