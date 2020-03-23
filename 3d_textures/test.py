from PIL import Image


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
