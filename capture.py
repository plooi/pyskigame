import pyscreenshot as ImageGrab
import os
import sys
if __name__ == '__main__':
    # part of the screen
    try:
        os.mkdir("./screenshots")
    except:
        pass
    im = ImageGrab.grab()  # X1,Y1,X2,Y2
    im.save("./screenshots/"+sys.argv[1]+".png")
