





import pyperclip
from rooms import *
from pylooiengine import *
import pylooiengine
from PIL import Image
import pyscreenshot
import pyautogui
from time import sleep
import os
import loading
import PySimpleGUI as sg

sound = None




altitude_box_location = 100,100
dropdown_menu_location = 200,200
UL,LR = [0,0],[100,100]
screenshot_box = [0,0,100,100]
world_name = "world"

no_tree = None
yes_tree = None
im = None

trees= None
no_trees = None

min_elevation,max_elevation=0,100

def alert():
    sound.play(maxtime=500)
def data_gen():
    global sound
    sound = LooiObject().new_sound("sounds/ChairliftTerminal.ogg",volume=60)
    try:
        for file in os.listdir('screenshots'): os.remove("screenshots/"+file)
    except:
        pass
    
    kill_all()
    BackgroundPic()
    _=Button(0, 0, 150, 100, "Quit", main_menu, Color(.6,.6,.6), black, 64)
    _.set_layer(0)
    _.depth = 10
    Text(text=split("This feature allows you to use Google Earth to scan in any topography you want."+
                    "\n\nStep 1: Open Google Earth in FULL SCREEN\n\nOnce that is done, return to the game and press next."))
    next(data_gen2)
def data_gen2():
    Text(text=split("Find the location in the world where you would like to ski on.\n\nRemove all overlays. (uncheck all the things that show like lines and roads and points of interest)\n\nMake sure that the 'terrain' is on though. That should be the ONLY thing checked."+
                    "\n\nOnce this is all done, press next."))
    next(data_gen2_5)
    
def data_gen2_5():
    Text(text=split("Position the camera in a spot where you can view the entire area you want to ski. \n\nThe catch is, you must be facing ***perfectly*** "+
    "downwards otherwise this wont work. Use the view rotator (eye icon in the upper right) to rotate your view to be PERFECTLY facing down.\n\n\n\nDo NOOOTTT move the view at all from this point on. (cannot click and drag the world, cannot zoom in and out, cannot rotate the view, NOTHING)"))
    next(data_gen3)
def data_gen3():
    Text(text=split("Press the 'Add Polygon' button.\n\nMake the polygon span the entire area of your ski location. \n\nDo this WITHOUT moving your view\n\nNEVER CLOSE THE POLYGON'S WINDOW until the whole process is complete."))
    next(data_gen4)
def data_gen4():
    Text(text=split("Click the 'Style/Color' tab on the polygon's window.\n\nChange the area color to magenta r=255, g=0, b=255 (this color is chosen because it rarely blends with satellite photos)\n\nMust be ***EXACTLY*** this rgb value otherwise it won't work."))
    next(data_gen5)
def data_gen5():
    Text(text=split("Click the 'Altitude' tab.\n\nOpen the only drop down menu on this tab (should have the text 'Clamped to Ground').\n\nSelect 'Absolute'"))
    next(data_gen6)
def data_gen6():
    Text(text=split("Check the box saying 'Extend sides to ground'"))
    next(data_gen7)
def data_gen7():
    Text(text=split("Move the polygon's popup window so that it's not covering up any important parts of the mountain. You will not be able to move that window after this step.\n\nFind the text input/text box that is to the right of the label 'Altitude:'. (it should say '0m') \n\nWhen you press next, "+
                    "immediately switch over to Google Earth, hover your mouse over the center of that text box, and then do NOT move your mouse until I tell you you can. When "+
                    "you hear a noise, that means that the computer is actually recording the mouse location you have. After you "+
                    "hear that noise, wait a couple seconds, now you can move your mouse and come back to the program."))
    next(data_gen8)

def data_gen8():
    global altitude_box_location
    sleep(8)
    alert()
    altitude_box_location = pyautogui.position()
    Text(text=split("Okay great. From this point on, you may NOT move that polygon's window at all. NOR are you allowed to close it.\n\nRemember, you can NOT move the window, you can NOT close that window, and you can NOT move the google earth view."))
    next(data_gen9)
def data_gen9():
    Text(text=split("Now, we're gonna do that again, but with a different mouse position. This time when you press next,"+
                    "switch over to Google Earth, hover your mouse over the DROPDOWN MENU (the one that says 'absolute'), and then do NOT move your mouse until the noise."))
    next(data_gen10)
def data_gen10():
    global dropdown_menu_location
    sleep(8)
    alert()
    dropdown_menu_location = pyautogui.position()
    Text(text=split("Great! Now, when you press next, switch over to google earth (just like last time)" +
    "and move your mouse to the UPPER LEFT corner of the imaginary rectangle that encompasses your ski area. Wait for the sound.\n\nThe imaginary rectangle that encompasses your ski area must be within the magenta polygon"))
    next(data_gen11)
def data_gen11():
    global UL
    sleep(8)
    alert()
    UL = pyautogui.position()
    Text(text=split("Awesome. Now, when you press next, do the same thing, but just do it with the lower right corner this time."))
    next(data_gen12)
def data_gen12():
    global LR,screenshot_box,yes_tree,no_tree, im
    sleep(8)
    
    LR = pyautogui.position()
    screenshot_box = (UL[0],UL[1],LR[0],LR[1])
    print(screenshot_box)
    #take screenshot
    os.system("python capture.py screenshots/screenshot.png %d %d %d %d" % screenshot_box)
    
    im = image("screenshots/screenshot.png")
    sleep(1)
    alert()
    
    
    
    
    no_tree = []
    yes_tree = []
    Text(text=split("When you click next, you will be given an interface containing a screenshot from the screenshot "+
            "region you have just selected. Now, we are trying to tell the computer which parts of the map are trees "+
            "and which parts aren't. Use the arrow keys to navigate to places with and without trees. Press y to tell "+
            "the computer it is a tree. Press n to tell the computer it's not. Press r to restart. Press space to show the computer's " +
            "guess as to which parts have trees. When you're happy with the computer's tree locations, move on to the next round."))
    next(data_gen13)
def data_gen13():
    global im,trees,no_trees
    
    no_trees = im.copy()
    trees = im.copy()
    
    X()
    next(data_gen14)
def data_gen14():    
    global trees,min_elevation,max_elevation,world_name
    while True:
        layout = [[sg.Text("Give this topography a name:"), sg.Input("Ski Mountain")],
                        [sg.OK()]]
        window = sg.Window('', layout, size = (500,200))
        events,values = window.Read()
        name = values[0]
        world_name = name
        window.close()
        if "." in world_name:
            sg.Popup("Cannot use the dot character in the name.")
            continue
        name += ".csv"
        if name in os.listdir("./topographic/"):
            sg.Popup("Name already taken. Choose a different name.")
            continue
        else:
            break
    
    #write the trees image to csv
    f = open("./topographic/" + name + "tree", "w")
    pixels = trees.load()
    for y in range(trees.size[1]):
        if y != 0:
            f.write("\n")
        row = []
        for x in range(trees.size[0]):
            if pixels[x,y][0]==0 and pixels[x,y][1]==255 and pixels[x,y][2]==0:
                row.append(1)
            else:
                row.append(0)
        f.write(",".join([str(m) for m in row]))
    f.close()
    
    Text(text=split("Tree file complete. Now, press next and enter the minimum elevation (in meters) that your ski location has (you can "+
                    "go extra low to give margin if you want) and the highest elevation (in meters). You may want to hover your mouse pointer at different locations on google earth to check for the highest and lowest elevation.\n\nWarning: If what you say is the highest elevation is not actually the highest elevation in the area, then unexpected behavior will occur."))
    
            
    next(data_gen15)
def data_gen15():
    global min_elevation,max_elevation
    while 1:
        
        layout = [[sg.Text("Min elev (meters):"), sg.Input("400")],
                    [sg.Text("Max elev (meters):"), sg.Input("3000")],
                            [sg.OK()]]
        window = sg.Window('', layout, size = (500,200))
        events,values = window.Read()
        window.close()
        try:
            min_elevation = int(values[0])
            max_elevation = int(values[1])
            break
        except Exception as e:
            sg.Popup(str(e))
    Text(text=split("The next step is to make the elevation file. This "+
                    "might take 10-30 minutes. Just press next, IMMEDIATELY switch over to google earth. DONT MOVE THE MOUSE once you get to google earth."+
                    "Shortly after, you mouse will start moving on it's own. This is fine, it's just the algorithm "+
                    "collecting the elevation data. When the mouse stops moving on it's own for good, then come back to " +
                    "the game. If the next instructions are not available yet, then that means you still need to wait "+
                    "for the post processing to complete. If the next instructions are avaiable, then continue."))
    next(data_gen16)
def data_gen16():
    sleep(8)
    step = 3
    for elevation in range(min_elevation, max_elevation, step):
        pyautogui.moveTo(altitude_box_location[0], altitude_box_location[1])
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy(str(elevation))
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.moveTo(dropdown_menu_location[0], dropdown_menu_location[1])
        pyautogui.click()
        sleep(.01)
        os.system("python capture.py %s %d %d %d %d" % ("screenshots/"+world_name + "___" + str(elevation) + ".png", screenshot_box[0], screenshot_box[1], screenshot_box[2], screenshot_box[3]))
        
        
    grid = None
    
    points = set()
    
    #find magenta
    last_elev = 0
    for elevation in range(min_elevation, max_elevation, step):
        last_elev = elevation
    img = Image.open("screenshots/"+world_name + "___" + str(last_elev) + ".png")
    magenta = img.getpixel((0, 0))
    magenta = magenta[0], magenta[1], magenta[2]
    #trust that the upper left hand corner is magneta. #trust
    
    
    loading.progress_bar("Post processing...")
    for elevation in range(min_elevation, max_elevation, step):
        img = Image.open("screenshots/"+world_name + "___" + str(elevation) + ".png")
        if grid == None:
            grid = []
            for y in range(img.height):
                grid.append([])
                for x in range(img.width):
                    grid[y].append(None)
            for y in range(img.height):
                for x in range(img.width):
                    points.add((x,y))
        print("elevation", elevation)
        
        to_remove = set()
        for point in points:
            x,y=point
            if (img.getpixel((x, y)) == magenta) and grid[y][x]==None:
                grid[y][x] = elevation
                to_remove.add(point)
        print("Updated " + str(len(to_remove)) + " points")
        points = points-to_remove
        print("We have " + str(len(points)) + " points left")
        loading.update((elevation-min_elevation)/(max_elevation-min_elevation)*100)
    loading.update(100)
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == None:
                grid[y][x] = max_elevation
    
    
    f = open("./topographic/"+world_name+".csv", "w")
    for line in grid:
        output_line = ""
        for elev in line:
            output_line += str(elev) + ","
        output_line = output_line[0:-1]
        f.write(output_line+"\n")
    f.close()
    
    
    Text(text=split("All done! When you select 'new from topology', you should see your topology there! It will be a file called '" + world_name + ".csv'"))
class X(LooiObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.set_layer(0)
        self.speed = 1
    def step(self):
        global im,trees,no_trees,yes_tree,no_tree
        moved = False
        if self.key("right", "down"):
            self.x += int(self.speed)
            moved = True
        if self.key("left", "down"):
            self.x -= int(self.speed)
            moved = True
        if self.key("up", "down"):
            self.y -= int(self.speed)
            moved = True
        if self.key("down", "down"):
            self.y += int(self.speed)
            moved = True
        if moved:
            self.speed += .3
        else:
            self.speed = 1
        
        
        if self.x < 0: self.x = 0
        if self.x >= im.size[0]: self.x = im.size[0]-1
        if self.y < 0: self.y = 0
        if self.y >= im.size[1]: self.y = im.size[1]-1
        
        no_trees = im.copy()
        pixels = no_trees.load()
        
        x=self.x
        y=self.y
        
        if self.key("y", "pressed"):
            yes_tree.append([pixels[x,y][0],pixels[x,y][1],pixels[x,y][2]])
            nearest_neighbor()
        elif self.key("n", "pressed"):
            no_tree.append([pixels[x,y][0],pixels[x,y][1],pixels[x,y][2]])
            nearest_neighbor()
        elif self.key("r", "pressed"):
            no_tree = []
            yes_tree = []
            nearest_neighbor()
        
        
        for xx in range(no_trees.size[0]):
            pixels[xx,y] = (255,0,0)
        for yy in range(no_trees.size[1]):
            pixels[x,yy] = (255,0,0)
            
    def paint(self):
        global im,trees,no_trees
        if self.key("space","down"):
            self.draw_image(0,100, 1000,1000, trees)
        else:
            self.draw_image(0,100, 1000,1000, no_trees)
    
def color_distance(c1, c2):
    dist = (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2
    return dist**.5
def nearest_neighbor():
    loading.progress_bar()
    global im,yes_tree,no_tree,trees
    
    trees = im.copy()
    pixels = trees.load()
    
    
    for x in range(trees.size[0]):
        for y in range(trees.size[1]):
            rgb = pixels[x,y]
            
            closest_classification = False#false is no tree true is tree
            closest_dist = 99999999999999999999999999999
            
            for color in no_tree:
                dist = color_distance(color,rgb)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_classification = False
            for color in yes_tree:
                dist = color_distance(color,rgb)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_classification = True
            if closest_classification == True:
                pixels[x,y] = (0,255,0)
        if x % 50 == 0:
            loading.update(x/trees.size[0]*100)
    loading.update(100)
            
            
            
def next(next_fn):
    def nxt():
        kill_all()
        BackgroundPic()
        next_fn()
        _=Button(0, 0, 150, 100, "Quit", main_menu, Color(.6,.6,.6), black, 64)
        _.set_layer(0)
        _.depth = 10
    _=Button(1840, 970, 150, 100, "Next", nxt, Color(.6,.6,.6), black, 64)
    _.set_layer(0)
    _.depth = 10


def split(text):
    ret = []
    while len(text) > 0:
        for i in range(len(text)):
            if i == len(text)-1:
                ret.append(text)
                text = ""
                break
            if (i > 30 and text[i] == " ") or text[i] == "\n":
                ret.append(text[0:i])
                text = text[i+1:]
                break
    return "\n".join(ret)
class Text(LooiObject):
    def __init__(self, x=700, y=200, width=600, height=700, text="Label", color=light_gray, text_color=black, font_size=28, font = "Microsoft Sans Serif"):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text.split("\n")
        self.font_size = font_size
        self.font = font
        self.color = color
        self.text_color = text_color
        self.set_layer(0)
        
    def paint(self):
        y = 0
        for line in self.text:
            y += self.font_size
            self.draw_text(self.x + 5, y+self.y + 15, line, self.font_size, self.text_color, self.color, self.font)
            
            
        self.draw_rect(self.x, self.y, self.x + self.width, self.y + self.height, self.color)
