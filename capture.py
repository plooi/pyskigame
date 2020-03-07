import pyscreenshot as ImageGrab
import os
import sys
if __name__ == '__main__':
    # part of the screen
    try:
        os.mkdir("./screenshots")
    except:
        pass
    
    if len(sys.argv) > 2:
        im = ImageGrab.grab(bbox = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])))
        im.save("./"+sys.argv[1])
    else:
        im = ImageGrab.grab()
        im.save("./"+sys.argv[1])
