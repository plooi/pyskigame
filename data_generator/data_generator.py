"""
instructions

go create a huge magenta (196,25,196) polygon in google earth coverting
the whole area you want to capture elevation for 

make it extend sides to ground, set it to "absolute"

first use align_mouse_assistant to find out
where in the screen your google earth altitude box is
so that this program can click it to set the altitude

before you start, make sure google earth view is perfectly facing down.
Do NOT move the view from now on until the end of the procedure

then use align_mouse_assistant to find out where the 
dropdown menu is so that this program can click on it to
update the altitude 

use align_mouse_assistant to find the appropriate
screen shot box

change altitude_box_location and dropdown_menu_location 
accordingly. They should be tuples
screenshot_box is a len 4 tuple x1,y1,x2,y2


start get_data() and then go to google earth
and just wait for the program to do it's thing

Then use create elevation grid with the same name as that which
you just used for get_data() to write the data to a csv file
    Make sure the magenta color in the code is adjusted for the magenta present 
    in the image
"""


from PIL import Image
import pyscreenshot
import pyautogui
from time import sleep


altitude_box_location = (170,187)
dropdown_menu_location = (307,187)
screenshot_box = (830,431,1498,945)
def align_mouse_assistant():
    while True:
        sleep(1)
        print(pyautogui.position())

def get_data(name, lowest=500, highest=2600, step=3):
    sleep(10)
    for elevation in range(lowest, highest, step):
        pyautogui.moveTo(altitude_box_location[0], altitude_box_location[1])
        pyautogui.click()
        #sleep(.01)
        pyautogui.hotkey('ctrl', 'a')
        #sleep(.01)
        for char in str(elevation):
            pyautogui.press(char)
        pyautogui.moveTo(dropdown_menu_location[0], dropdown_menu_location[1])
        pyautogui.click()
        sleep(.01)
        im = pyscreenshot.grab()
        im.crop(screenshot_box).save(name + "___" + str(elevation) + ".png")
        #im.save(name + "___" + str(elevation) + ".png")
        #sleep(.01)
        
def create_elevation_grid(name, lowest=500, highest=2500, step=3):
    grid = None
    
    for elevation in range(lowest, highest, step):
        img = Image.open(name + "___" + str(elevation) + ".png")
        if grid == None:
            grid = []
            for y in range(img.height):
                grid.append([])
                for x in range(img.width):
                    grid[y].append(None)
        print(img.width, img.height)
        for y in range(img.height):
            for x in range(img.width):
                if ( color_distance(img.getpixel((x, y)), (161,43,158)) < 15 ) and grid[y][x]==None:
                    grid[y][x] = elevation
        print(elevation)
    
    f = open(name+".csv", "w")
    for line in grid:
        output_line = ""
        for elev in line:
            output_line += str(elev) + ","
        output_line = output_line[0:-1]
        f.write(output_line+"\n")
    f.close()
        
        
        
def color_distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
        
def main():
    #get_data("fernie")
    #align_mouse_assistant()
    create_elevation_grid("fernie", lowest=950)
    
if __name__ == "__main__": main()
