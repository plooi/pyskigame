from PIL import Image


def color_scalar(x):
    return int(x*.8)



"""

for aa in ["05","10","15","20","25","30","35","40"]:
    im = Image.open("SnowTex.png")
    pix =  im.load()
    al = int(aa)
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r,g,b,a = pix[x,y]
            
            
            pix[x,y] = color_scalar(r),color_scalar(g),color_scalar(b),al
    im = im.resize((65,65))
    im.save("SnowTex%sBlurry.png"%(aa,))
    
for aa in ["40"]:
    im = Image.open("SnowTex.png")
    pix =  im.load()
    al = int(aa)
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r,g,b,a = pix[x,y]
            
            
            pix[x,y] = color_scalar(r),color_scalar(g),color_scalar(b),al
    im.save("SnowTex%sClear.png"%(aa,))
    
"""
"""

i = Image.open("Cloud1.jpg")
i.putalpha(255)
pix = i.load()
q = 150

for x in range(i.size[0]):
    for y in range(i.size[1]):
        r,g,b,a = pix[x,y]
        
        
        
        #pix[x,y] = r,g,b,min([r,g,b])
        if r < q and g < q and b < q:
            pix[x,y] = 0,0,0,0

i.resize((500,500))
i.save("Cloud1.png")
"""
i = Image.open("Cloud2 - copy.png")
#i.putalpha(255)
pix = i.load()
q = 150

for x in range(i.size[0]):
    for y in range(i.size[1]):
        r,g,b,a = pix[x,y]
        
        
        
        #pix[x,y] = r,g,b,min([r,g,b])
        if a < 150:
            pix[x,y] = 0,0,0,0
        else:
            pix[x,y] = r,r,r,a

i.resize((500,500))
i.save("Cloud2.png")