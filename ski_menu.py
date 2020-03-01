from pylooiengine import *
from pylooiengine.gui import *
import pylooiengine
from lift import *
import game_ui
from world_operations import *
from model_3d import *
import lift
import lift_util
import world_save
import rooms
from collections import OrderedDict
from models import *
from util import get_angle
from rock import *


class Menu(LooiObject):
    def __init__(self, ui):
        super().__init__()
        self.set_layer(2)
        self.ui = ui
        
        if self.ui.game_mode == "ski":
            self.btn7 = Button(x = 1240, y=760, width=80, height=80, font_size=10, text="", image=image("Save Icon.png"), action=save, action_parameter=self)
            self.btn7.set_layer(-2)
            self.add(self.btn7)
            
            self.btn8 = Button(x = 1320, y=760, width=80, height=80, font_size=10, text="", image=image("Exit Icon.png"), action=exit, action_parameter=self)
            self.btn8.set_layer(-2)
            self.add(self.btn8)
        
        self.btn9 = Button(x = 1160, y=760, width=80, height=80, font_size=10, text="", image=image("Settings Icon.png"), action=settings, action_parameter=self)
        self.btn9.set_layer(-2)
        self.add(self.btn9)
        
       
        
        self.x1 = 500
        self.y1 = 100
        self.x2 = 1500
        self.y2 = 900
        self.menu_color = Color(.9,.95,.9)
        
        
        
        
    def paint(self):
        self.draw_rect(self.x1, self.y1, self.x2, self.y2, self.menu_color)

def settings(menu):

    setting = OrderedDict()
    setting["Line of Sight"] = menu.ui.world.view.line_of_sight
    setting["Line of Sight 2"] = menu.ui.world.properties["line_of_sight2"]
    setting["Rotation Speed"] = menu.ui.world.view.rot_spd
    setting["Chair Time Interval Detachable"] = menu.ui.world.properties["chair_time_distance_detachable"]
    setting["Chair Time Interval Gondola"] = menu.ui.world.properties["chair_time_distance_gondola"]
    setting["Chair Time Interval Fixed Grip"] = menu.ui.world.properties["chair_time_distance_fixed"]
    
    
    col = []
    for key in setting:
        setting[key] = str(setting[key])
        col.append([sg.Text(key), sg.Input(setting[key])])
    
    col = sg.Column(col, size=(500,800), scrollable=True)
    
    layout = [    [sg.OK(), sg.Cancel()],
                  [sg.Text("Name: %s" % menu.ui.world.properties["name"])],
                  [col],
                   ]
    window = sg.Window('', layout, size = (500,800))
    event, values = window.Read()
    
    
    
    new_settings = OrderedDict()
    i = 0
    for key in setting:
        new_settings[key] = values[i]
        i += 1
    
    window.close()
    
    def same(key):
        return new_settings[key] == setting[key]
    def nsame(key):
        return not same(key)
    
    if event == "OK":
        try:
            #do all the non-reload settings first...
            menu.ui.world.view.line_of_sight = float(new_settings["Line of Sight"])
            menu.ui.world.view.rot_spd = float(new_settings["Rotation Speed"])
            menu.ui.world.properties["chair_time_distance_detachable"] = float(new_settings["Chair Time Interval Detachable"])
            menu.ui.world.properties["chair_time_distance_gondola"] = float(new_settings["Chair Time Interval Gondola"])
            menu.ui.world.properties["chair_time_distance_fixed"] = float(new_settings["Chair Time Interval Fixed Grip"])
            menu.ui.world.properties["line_of_sight2"] = float(new_settings["Line of Sight 2"])
            
            
            #then do the settings that require lifts to redo chairs
            if nsame("Chair Time Interval Detachable") or nsame("Chair Time Interval Gondola") or nsame("Chair Time Interval Fixed Grip"):
                for chairlift in lift.active_lifts:
                    if chairlift.rope_speed != chairlift.terminal_speed:#if detachable
                        if chairlift.super_blurry_chair_model == gondola_model_4:#if gondola
                            chairlift.set_chair_time_distance(menu.ui.world.properties["chair_time_distance_gondola"])
                        else:
                            chairlift.set_chair_time_distance(menu.ui.world.properties["chair_time_distance_detachable"])
                    else:#if fixed grip
                        chairlift.set_chair_time_distance(menu.ui.world.properties["chair_time_distance_fixed"])
        except Exception as e:
            traceback.print_exc()
            sg.Popup(str(e))            
            
        
                
        
    
def save(menu):
    world_save.write(menu.ui.world, writepath="../saves/")
def exit(menu):
    
    layout = [[sg.Text("Save or not?")],
                        [sg.Yes(), sg.No()]]
    window = sg.Window('', layout, size = (500,300))
    event, _ = window.Read()
    window.close()
    
    if event == "Yes":
        save(menu)
    if event == None:
        return
    menu.ui.stop_sounds()
    #code for exiting:
    for looi_object in pylooiengine.main_window.unlayered_looi_objects+main_window.layered_looi_objects+main_window.transfer_to_unlayered_looi_objects+main_window.transfer_to_layered_looi_objects:
        looi_object.deactivate()
    
    rooms.main_menu()



