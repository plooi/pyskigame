import pylooiengine
from pylooiengine import *
from constants import x as constants



w = Window(internal_size = (2000,1080), fps=constants["fps"])
#import mash_textures
import os
import pygame

import rooms

def main():  
    print("WARNING: DO NOT CLICK THE BLACK PORTION OF THE COMMAND PROMPT OTHERWISE THE PROGRAM WILL FREEZE. IF YOU ACCIDENTALLY DO THIS, YOU MUST SELECT THE BLACK PORTION OF THE COMMAND PROMPT AND PRESS ESCAPE TO UNFREEZE THE PROGRAM.")
    if not os.path.exists("../worlds"):os.mkdir( "../worlds")
    if not os.path.exists("../saves"):os.mkdir(  "../saves")
    if not os.path.exists("../recycle"):os.mkdir("../recycle")
    w.start()
if __name__ == "__main__": main()
