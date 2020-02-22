import pylooiengine
from pylooiengine import *
w = Window(internal_size = (2000,1080), fps=30)
#import mash_textures
import os
import pygame

import rooms

def main():  
    if not os.path.exists("../worlds"):os.mkdir("../worlds")
    if not os.path.exists("../saves"):os.mkdir("../saves")
    w.start()
if __name__ == "__main__": main()
