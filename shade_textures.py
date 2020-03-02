from pylooiengine import *
import PIL


def average_rgb(pixels):
    num = 0
    rsum = 0
    gsum = 0
    bsum = 0
    for x in range(img.size[0]):
        for z in range(img.size[1]):
            rsum += pixels[x,z][0]
            gsum += pixels[x,z][1]
            bsum += pixels[x,z][2]
            num += 1
    ravg = rsum/num
    gavg = gsum/num
    bavg = bsum/num
    
    return (ravg+gavg+bavg)/3

blends = 1
'''
#for doing snow textures
name = "./3d_textures/MinecraftSnow"
extension = "png"
for blend in range(blends):
    for target in range(155, 256, 4):
        img = image(name + "." + extension)
        pixels = img.load()
        while average_rgb(pixels) < target:
            for x in range(img.size[0]):
                for z in range(img.size[1]):
                    r,g,b,a = pixels[x,z]
                    r += 1
                    g += 1
                    b += 1
                    if r > 255: r = 255
                    if r < 0: r = 0
                    if g > 255: g = 255
                    if g < 0: g = 0
                    if b > 255: b = 255
                    if b < 0: b = 0
                    pixels[x,z] = (r,g,b,a)
        while average_rgb(pixels) > target:
            for x in range(img.size[0]):
                for z in range(img.size[1]):
                    r,g,b,a = pixels[x,z]
                    r -= 1
                    g -= 1
                    b -= 1
                    if r > 255: r = 255
                    if r < 0: r = 0
                    if g > 255: g = 255
                    if g < 0: g = 0
                    if b > 255: b = 255
                    if b < 0: b = 0
                    pixels[x,z] = (r,g,b,a)
                    
        for x in range(img.size[0]):
            for z in range(img.size[1]):
                
                r,g,b,a = pixels[x,z]
                #modify color here if you want
                """
                p = 2
                if g > b+p:
                    g = b+p
                if r > b+p:
                    r = b+p
                if r < b-p:
                    r = b-p
                if g < b-p:
                    g = b-p
                """
                r = ( r*(blends-blend)+target*blend ) / blends
                g = ( g*(blends-blend)+target*blend ) / blends
                b = ( b*(blends-blend)+target*blend ) / blends
                pixels[x,z] = (int(r),int(g),int(b),a)
        #img.show()
        img.save(name + "-lighting-" + str(target) + "_"*blend + "." + extension)
        print(target,blend)
'''

#for doing pine textures


for i in [1,2,3,4]:
    
    factor = 4-i
    #rsub = 40 * factor
    #gsub = 24 * factor
    #bsub = 40 * factor
    rsub = 60 * factor
    gsub = 36 * factor
    bsub = 60 * factor
    if i == 4:
        gsub -= 30
        rsub += 10
        bsub += 10
    img = image("../OriginalPineTexture.png")
    pixels = img.load()
    for x in range(img.size[0]):
        for z in range(img.size[1]):
            r,g,b,a = pixels[x,z]
            r -= rsub
            g -= gsub
            b -= bsub
    
            if r > 255: r = 255
            if r < 0: r = 0
            if g > 255: g = 255
            if g < 0: g = 0
            if b > 255: b = 255
            if b < 0: b = 0
            
            pixels[x,z] = (r,g,b,a)
    img.save("3d_textures/PineTexture%d.png"%(i,))



