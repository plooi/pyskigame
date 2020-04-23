from PIL import Image


def color_scalar(x):
    return int(x*.8)





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
    
