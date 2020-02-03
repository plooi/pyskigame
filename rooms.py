from pylooiengine import *
from pylooiengine.gui import *
import pylooiengine
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

class Launcher(LooiObject):
    def step(self):
        main_menu()
        self.deactivate()
Launcher()        

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
    map_editor = Button(800, 200, 400, 100, "Map Editor", new_world_1, Color(.6,.6,.6), black, 64)
    map_editor.button_depth = 10
    
    ski_mode = Button(800, 300, 400, 100, "Ski", load_room, Color(.6,.6,.6), black, 64)
    ski_mode.button_depth = 10
    
    abort = Button(800, 400, 400, 100, "Quit", lambda:quit(), Color(.6,.6,.6), black, 64)
    abort.button_depth = 10
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
    blank = Button(700, 250, 600, 100, "New Blank", blank_world, Color(.6,.6,.6), black, 64)
    blank.button_depth = 10
    data_file = Button(700, 350, 600, 100, "New From Topology", data_file_world, Color(.6,.6,.6), black, 64)
    data_file.button_depth = 10
    copy = Button(700, 450, 600, 100, "New Copy", create_copy, Color(.6,.6,.6), black, 64)
    copy.button_depth = 10
    load = Button(700, 550, 600, 100, "Load", load_existing_map_editor, Color(.6,.6,.6), black, 64)
    load.button_depth = 10
    back = Button(700, 650, 600, 100, "<--", main_menu, Color(.6,.6,.6), black, 64)
    back.button_depth = 10
    
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
    
    
    
        if values[0] in os.listdir("./worlds/"):
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
    for d in os.listdir("./worlds"):
        if os.path.isdir("./worlds/"+d):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose World to Load:                ')],
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
        
        if values[0] in os.listdir("./worlds/"):
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
    
    the_world = world_save.read("./worlds/"+event)
    the_world.properties["name"] = values[0]
    world_save.write(the_world)
    init_game_room(the_world)
    
def load_existing_map_editor():
    col = []
    for d in os.listdir("./worlds"):
        if os.path.isdir("./worlds/"+d):
            col.append([sg.Button(d)])
    col = sg.Column(col, size=(500,800), scrollable=True)
            
    layout = [[sg.Text('                Choose World to Copy:                ')],
                [col]]
    
    window = sg.Window('', layout, size=(500,800))
    event, values = window.Read()
    window.close()
    if event == None: return
    
    
    
    
    the_world = world_save.read("./worlds/"+event)
    init_game_room(the_world)
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
                  [sg.OK()] ]
        window = sg.Window('', layout)
        event, values = window.Read()
        window.close()
        if event == None: return
        
        if values[0] in os.listdir("./worlds/"):
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
        the_world = world.World().init_csv(values[0], "./topographic/" + choice)
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

    pylooiengine.main_window.set_fps(30)
    
    
    kill_all()
    
    #world.add_trees_elevation(1, 1,world.get_height()-1,world.get_width()-1)
    """try:
        l = Lift(world)
        l.build([100,100,[x/100 for x in range(10,100,7)],100,300], rope_speed = .2, terminal_speed = .05, chair_time_distance=50)
    except:
        pass
    """
    world.activate()
    game_ui.UI(world, "map editor").activate()






    








