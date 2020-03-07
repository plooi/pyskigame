from pylooiengine import *
from pylooiengine.gui import *
import pylooiengine
import pygame
import easygui
import world
from lift import Lift

from model_3d import *
import os
from time import sleep
import pygame
import game_ui
import PySimpleGUI as sg
import traceback
from random import random
from math import sin,cos
from tree import Tree
import world_save
import shutil

class Launcher(LooiObject):
    def step(self):
        main_menu()
        self.deactivate()
Launcher()        

class BackgroundPic(LooiObject):
    def __init__(self):
        super().__init__()
        self.img = image("textures/MainMenu.png")
        self.set_layer(1000)
    def paint(self):
        self.draw_image(0,0,self.get_my_window().get_internal_size()[0],self.get_my_window().get_internal_size()[1], self.img)

def kill_all():
    for looi_object in pylooiengine.main_window.unlayered_looi_objects+main_window.layered_looi_objects:
        looi_object.deactivate()
    """
    for l in main_window.unlayered_looi_objects:
        l.deactivate()
    for l in main_window.layered_looi_objects:
        l.deactivate()
    """

def main_menu():
    kill_all()
    BackgroundPic()
    map_editor = Button(800, 200, 400, 85, "Map Editor", new_world_1, Color(.6,.6,.6), black, 64)
    map_editor.button_depth = 10
    map_editor.set_layer(0)
    
    ski_mode = Button(800, 300, 400, 85, "Ski", ski_room, Color(.6,.6,.6), black, 64)
    ski_mode.button_depth = 10
    ski_mode.set_layer(0)
    
    scan = Button(800, 400, 400, 85, "Scan Terrain", lambda:data_gen.data_gen(), Color(.6,.6,.6), black, 64)
    scan.button_depth = 10
    scan.set_layer(0)
    
    delete_ = Button(800, 500, 400, 85, "Delete", delete_stuff, Color(.6,.6,.6), black, 64)
    delete_.button_depth = 10
    delete_.set_layer(0)
    
    abort = Button(800, 600, 400, 85, "Quit", lambda:quit(), Color(.6,.6,.6), black, 64)
    abort.button_depth = 10
    abort.set_layer(0)

def delete_stuff():
    kill_all()
    BackgroundPic()
    
    del_ski_ = Button(600, 250, 800, 85, "Delete a Ski World", del_ski, Color(.6,.6,.6), black, 64)
    del_ski_.set_layer(0)
    del_ski_.button_depth = 10
    del_map_ = Button(600, 350, 800, 85, "Delete a Map Editor World", del_map, Color(.6,.6,.6), black, 64)
    del_map_.set_layer(0)
    del_map_.button_depth = 10
    del_elev_ = Button(600, 450, 800, 85, "Delete an Elevation CSV", del_elev, Color(.6,.6,.6), black, 64)
    del_elev_.set_layer(0)
    del_elev_.button_depth = 10
    back = Button(600, 650, 800, 85, "<--", main_menu, Color(.6,.6,.6), black, 64)
    back.set_layer(0)
    back.button_depth = 10
def del_ski():
    layout = [[sg.Button(ski_world)] for ski_world in os.listdir("../saves")]
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None:return
    if os.path.isdir("../recycle/"+event):shutil.rmtree("../recycle/"+event)
    if os.path.isfile("../recycle/"+event):os.remove("../recycle/"+event)
    shutil.move("../saves/"+event, "../recycle")
def del_map():
    layout = [[sg.Button(ski_world)] for ski_world in os.listdir("../worlds")]
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None:return
    if os.path.isdir("../recycle/"+event):shutil.rmtree("../recycle/"+event)
    if os.path.isfile("../recycle/"+event):os.remove("../recycle/"+event)
    shutil.move("../worlds/"+event, "../recycle")
def del_elev():
    layout = [[sg.Button(ski_world)] for ski_world in os.listdir("./topographic")]
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None:return
    if os.path.isdir("../recycle/"+event):shutil.rmtree("../recycle/"+event)
    if os.path.isfile("../recycle/"+event):os.remove("../recycle/"+event)
    shutil.move("./topographic/"+event, "../recycle")
    
def ski_room():
    kill_all()
    BackgroundPic()
    new = Button(700, 250, 600, 85, "New Game", new_ski_world, Color(.6,.6,.6), black, 64)
    new.set_layer(0)
    new.button_depth = 10
    load = Button(700, 350, 600, 85, "Load", load_existing_ski_world, Color(.6,.6,.6), black, 64)
    load.set_layer(0)
    load.button_depth = 10
    back = Button(700, 650, 600, 85, "<--", main_menu, Color(.6,.6,.6), black, 64)
    back.set_layer(0)
    back.button_depth = 10
    
    

def new_ski_world():
    col = []
    for d in os.listdir("../worlds"):
        if os.path.isdir("../worlds/"+d):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose World to Ski On:                ')],
                [col]]
    
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None: return
    
    
    while 1:
        layout = [
                  [sg.Text('Name:'), sg.Input(event)],
                  [sg.OK()] ]
        window = sg.Window('', layout)
        _event, values = window.Read()
        window.close()
        if _event == None: return
        
        if values[0] in os.listdir("../saves/"):
            layout = [
                          [sg.Text('A world of this name already exists. Would you like to OVERWRITE it?')],
                          [sg.Yes(), sg.No()] ]
            window = sg.Window('', layout)
            _event, _values = window.Read()
            window.close()
            if _event == None or _event == "No":
                continue
            elif _event == "Yes":
                break
        else:
            break
    def job():
        the_world = world_save.read("../worlds/"+event)
        the_world.properties["name"] = values[0]
        world_save.write(the_world, writepath="../saves/")
        init_ski_room(the_world)
    LoadingScreen(job)
def load_existing_ski_world():
    col = []
    for d in os.listdir("../saves"):
        if os.path.isdir("../saves/"+d):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose World to Load:                ')],
                [col]]
    
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None: return
    
    
    
    def job():
        the_world = world_save.read("../saves/"+event)
        init_ski_room(the_world)
    
    LoadingScreen(job)

def load_room():
    layout = [[sg.Text('Enter a Number')],
          [sg.Input()],
          [sg.OK()] ]

    window = sg.Window('Enter a number example', layout)
    event, values = window.Read()
    window.close()
    print(values)
    
def new_world_1():
    kill_all()
    BackgroundPic()
    blank = Button(700, 250, 600, 85, "New Blank", blank_world, Color(.6,.6,.6), black, 64)
    blank.set_layer(0)
    blank.button_depth = 10
    data_file = Button(700, 350, 600, 85, "New From Topology", data_file_world, Color(.6,.6,.6), black, 64)
    data_file.set_layer(0)
    data_file.button_depth = 10
    copy = Button(700, 450, 600, 85, "New Copy", create_copy, Color(.6,.6,.6), black, 64)
    copy.set_layer(0)
    copy.button_depth = 10
    load = Button(700, 550, 600, 85, "Load", load_existing_map_editor, Color(.6,.6,.6), black, 64)
    load.set_layer(0)
    load.button_depth = 10
    back = Button(700, 650, 600, 85, "<--", main_menu, Color(.6,.6,.6), black, 64)
    back.set_layer(0)
    back.button_depth = 10
    
    

class LoadingScreen(LooiObject):
    def __init__(self, job):
        kill_all()
        super().__init__()
        self.i=0
        self.job = job
    def paint(self):
        #loading gui
        bg = Color(.9,.9,1)
        self.draw_text(550,800,"Loading...", background_color=bg,font_size = 100,font = "Goudy Stout")
        self.draw_rect(0,0,self.get_my_window().get_internal_size()[0],self.get_my_window().get_internal_size()[1], bg)
        
            
        
        
        
        
        
        self.i+=1
        if self.i==2:
            self.job()
            self.deactivate()
            
        
def blank_world():
    
    values = ["My World", "100", "100"]
    while 1:
        layout = [
                  [sg.Text('Name:'), sg.Input(str(values[0]))],
                  [sg.Text('Width:'), sg.Input(str(values[1]))],
                  [sg.Text('Height:'), sg.Input(str(values[2]))],
                  [sg.OK()] ]
        window = sg.Window('', layout, size = (500,800))
        event, values = window.Read()
        window.close()
        if event==None: return
    
    
    
        if values[0] in os.listdir("../worlds/"):
            layout = [
                          [sg.Text('A world of this name already exists. Would you like to OVERWRITE it?')],
                          [sg.Yes(), sg.No()] ]
            window = sg.Window('', layout)
            event, _values = window.Read()
            window.close()
            if event == None or event == "No":
                #reprompt the thing again
                continue
            elif event == "Yes":
                break
        else:
            break
            
    try:
        the_world = world.World().init(values[0], int(values[1]), int(values[2]))#, elevation_function=lambda z,x:sin(x/30)*300+sin(z/15)*150
        world_save.write(the_world)
    except Exception as e:
        sleep(1)
        traceback.print_exc()
        easygui.msgbox(str(e))
        return
    init_game_room(the_world)
def create_copy():
    col = []
    for d in os.listdir("../worlds"):
        if os.path.isdir("../worlds/"+d):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose World to Copy:                ')],
                [col]]
    
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None: return
    
    
    while 1:
        layout = [
                  [sg.Text('Name:'), sg.Input(event)],
                  [sg.OK()] ]
        window = sg.Window('', layout)
        _event, values = window.Read()
        window.close()
        if _event == None: return
        
        if values[0] in os.listdir("../worlds/"):
            layout = [
                          [sg.Text('A world of this name already exists. Would you like to OVERWRITE it?')],
                          [sg.Yes(), sg.No()] ]
            window = sg.Window('', layout)
            _event, _values = window.Read()
            window.close()
            if _event == None or _event == "No":
                continue
            elif _event == "Yes":
                break
        else:
            break
    def job():
        the_world = world_save.read("../worlds/"+event)
        the_world.properties["name"] = values[0]
        world_save.write(the_world)
        init_game_room(the_world)
    LoadingScreen(job)
    
def load_existing_map_editor():
    col = []
    for d in os.listdir("../worlds"):
        if os.path.isdir("../worlds/"+d):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose World to Load:                ')],
                [col]]
    
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None: return
    
    
    def job():
        the_world = world_save.read("../worlds/"+event)
        init_game_room(the_world)
    LoadingScreen(job)
    
    
def data_file_world():
    
    col = []
    for d in os.listdir("./topographic"):
        if d.endswith(".csv"):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose Topography:                ')],
                [col]]
    
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
            
    choice = event
    
    
    if event == None: return
    while 1:
        layout = [
                  [sg.Text('Name:'), sg.Input(event)],
                  [sg.Text('Tree density (value from 0 to 1):'), sg.Input(".4")],
                  [sg.OK()] ]
        window = sg.Window('', layout)
        event, values = window.Read()
        window.close()
        if event == None: return
        
        try:
            tree_density = float(values[1])
        except:
            sg.Popup("Invalid tree density")
            continue
            
        
        if values[0] in os.listdir("../worlds/"):
            layout = [
                          [sg.Text('A world of this name already exists. Would you like to OVERWRITE it?')],
                          [sg.Yes(), sg.No()] ]
            window = sg.Window('', layout)
            event, _values = window.Read()
            window.close()
            if event == None or event == "No":
                continue
            elif event == "Yes":
                break
        else:
            break
    
    
    try:
        the_world = world.World().init_csv(values[0], "./topographic/" + choice, tree_chance=tree_density)
        world_save.write(the_world)
    except Exception as e:
        sleep(1)
        traceback.print_exc()
        easygui.msgbox(str(e))
        return
    
    init_game_room(the_world)
"""
def new_world():
    
    class NewWorldPrompt(LooiObject):
        def step(self):
            res = easygui.choicebox(msg="Would you like to start with a blank world or a world generated by topographic data?", choices=["Blank", "Data File"])
            if res == "Blank":
                
            elif res == "Data File":
                
                
            else:
                main_menu()
            self.deactivate()
    n = NewWorldPrompt()
"""
def init_game_room(world):
    game_ui.set_mouse_mode("3D")
    pylooiengine.main_window.set_fps(30)#REDUNDANT but i'm too scared to remove it lol
    kill_all()
    world.activate()
    game_ui.UI(world, "map editor").activate()
    
def init_ski_room(world):
    game_ui.set_mouse_mode("3D")
    pylooiengine.main_window.set_fps(30)#REDUNDANT but i'm too scared to remove it lol
    kill_all()
    world.activate()
    game_ui.UI(world, "ski").activate()




import data_gen

    








