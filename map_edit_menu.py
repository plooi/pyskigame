from pylooiengine import *
from pylooiengine.gui import *
import pylooiengine
from lift import *
import game_ui
from world_operations import *
from model_3d import *
import lift
import lift_util
import lodge
import world_save
import rooms
from collections import OrderedDict
from models import *
from util import get_angle
from rock import *
from stop_selecting_exception import StopSelectingException
import traceback
import building
from landmark import Landmark
from world_object import WorldObject
from bump import *
import mission_center
from tree import Tree


build_hs_terminal_model = hs_terminal_design_gray
build_fg_terminal_model = terminal_design_2



class Menu(LooiObject):
    def __init__(self, ui):
        super().__init__()
        self.set_layer(2)
        self.ui = ui
        
        
        self.btn31 = Button(x = 1240, y=120, width=70, height=70, font_size=12, text="botend", action=bot_button, action_parameter=self)
        self.btn31.set_layer(-2)
        self.add(self.btn31)
        
        self.btn32 = Button(x = 1320, y=120, width=70, height=70, font_size=12, text="topend", action=top_button, action_parameter=self)
        self.btn32.set_layer(-2)
        self.add(self.btn32)
        
        self.btn1 = Button(x = 680, y=120, width=70, height=70, font_size=10, text="", image=image("D-4C Icon.png"), action=LiftBuild, action_parameter=self)
        self.btn1.set_layer(-4)
        self.add(self.btn1)
        
        self.btn10 = Button(x = 520, y=120, width=70, height=70, font_size=10, text="", image=image("D-8G Icon.png"), action=GondolaBuild, action_parameter=self)
        self.btn10.set_layer(-2)
        self.add(self.btn10)
        self.btn11 = Button(x = 760, y=120, width=70, height=70, font_size=10, text="", image=image("C4 Icon.png"), action=C4Build, action_parameter=self)
        self.btn11.set_layer(-5)
        self.add(self.btn11)
        
        self.btn12 = Button(x = 840, y=120, width=70, height=70, font_size=10, text="", image=image("C3 Icon.png"), action=C3Build, action_parameter=self)
        self.btn12.set_layer(-6)
        self.add(self.btn12)
        
        self.btn13 = Button(x = 920, y=120, width=70, height=70, font_size=10, text="", image=image("C2 Icon.png"), action=C2Build, action_parameter=self)
        self.btn13.set_layer(-7)
        self.add(self.btn13)
        
        self.btn14 = Button(x = 600, y=120, width=70, height=70, font_size=10, text="", image=image("D-6C Icon.png"), action=D_6CBuild, action_parameter=self)
        self.btn14.set_layer(-3)
        self.add(self.btn14)
        
        self.btn15 = Button(x = 1000, y=120, width=70, height=70, font_size=10, text="", image=image("T Bar Icon.png"), action=TBarBuild, action_parameter=self)
        self.btn15.set_layer(-8)
        self.add(self.btn15)
        
        self.btn2 = Button(x = 520, y=200, width=70, height=70, font_size=10, text="", image=image("Tree Icon.png"), action=TreeAdd, action_parameter=(self, .01))
        self.btn2.set_layer(-2)
        self.add(self.btn2)
        
        self.btn3 = Button(x = 600, y=200, width=70, height=70, font_size=10, text="", image=image("Tree Icon2.png"), action=TreeAdd, action_parameter=(self, .06))
        self.btn3.set_layer(-2)
        self.add(self.btn3)
        
        self.btn4 = Button(x = 680, y=200, width=70, height=70, font_size=10, text="", image=image("Tree Icon3.png"), action=TreeAdd, action_parameter=(self, .2))
        self.btn4.set_layer(-2)
        self.add(self.btn4)
        
        self.btn100 = Button(x = 920, y=200, width=70, height=70, font_size=10, text="", image=image("Tree Filter Icon.png"), action=TreeFilter, action_parameter=self)
        self.btn100.set_layer(-2)
        self.add(self.btn100)
        
        self.btn5 = Button(x = 760, y=200, width=70, height=70, font_size=10, text="", image=image("Chainsaw.png"), action=Chainsaw, action_parameter=self)
        self.btn5.set_layer(-2)
        self.add(self.btn5)
        
        self.btn20 = Button(x = 840, y=200, width=70, height=70, font_size=10, text="", image=image("Chainsaw Straight.png"), action=ChainsawStraight, action_parameter=self)
        self.btn20.set_layer(-2)
        self.add(self.btn20)
        
        self.btn6 = Button(x = 520, y=600, width=70, height=70, font_size=10, text="", image=image("Select.png"), action=Select, action_parameter=self)
        self.btn6.set_layer(-2)
        self.add(self.btn6)
        
        self.btn7 = Button(x = 1240, y=760, width=70, height=70, font_size=10, text="", image=image("Save Icon.png"), action=save, action_parameter=self)
        self.btn7.set_layer(-2)
        self.add(self.btn7)
        
        self.btn8 = Button(x = 1320, y=760, width=70, height=70, font_size=10, text="", image=image("Exit Icon.png"), action=exit, action_parameter=self)
        self.btn8.set_layer(-2)
        self.add(self.btn8)
        
        self.btn30 = Button(x = 1320, y=680, width=70, height=70, font_size=10, text="", image=image("textures/Telemetry.png"), action=Measure, action_parameter=self)
        self.btn30.set_layer(-2)
        self.add(self.btn30)
        
        self.btn9 = Button(x = 1160, y=760, width=70, height=70, font_size=10, text="", image=image("Settings Icon.png"), action=settings, action_parameter=self)
        self.btn9.set_layer(-2)
        self.add(self.btn9)
        
        
        self.btn16 = Button(x = 520, y=280, width=70, height=70, font_size=10, text="", image=image("Mountain Icon.png"), action=HillMod, action_parameter=self)
        self.btn16.set_layer(-2)
        self.add(self.btn16)
        
        
        self.btn17 = Button(x = 600, y=280, width=70, height=70, font_size=10, text="", image=image("Smooth Icon.png"), action=SmoothMod, action_parameter=self)
        self.btn17.set_layer(-2)
        self.add(self.btn17)
        
        self.btn18 = Button(x = 680, y=280, width=70, height=70, font_size=10, text="", image=image("Plateau Icon.png"), action=PlateauMod, action_parameter=self)
        self.btn18.set_layer(-2)
        self.add(self.btn18)
        
        
        self.btn19 = Button(x = 760, y=280, width=70, height=70, font_size=10, text="", image=image("Path Icon.png"), action=PathMod, action_parameter=self)
        self.btn19.set_layer(-2)
        self.add(self.btn19)
        
        self.btn21 = Button(x = 520, y=360, width=70, height=70, font_size=10, text="", image=image("Rock Icon.png"), action=PlaceRock, action_parameter=self)
        self.btn21.set_layer(-2)
        self.add(self.btn21)
        
        self.btn23 = Button(x = 600, y=360, width=70, height=70, font_size=10, text="", image=image("Big Rock Icon.png"), action=PlaceRock2, action_parameter=self)
        self.btn23.set_layer(-2)
        self.add(self.btn23)
        
        self.btn24 = Button(x = 680, y=360, width=70, height=70, font_size=10, text="", image=image("textures/Bumps Icon.png"), action=PlaceBumps, action_parameter=self)
        self.btn24.set_layer(-2)
        self.add(self.btn24)
        
        self.btn25 = Button(x = 760, y=360, width=70, height=70, font_size=10, text="", image=image("textures/Remove Bumps Icon.png"), action=RemoveBumps, action_parameter=self)
        self.btn25.set_layer(-2)
        self.add(self.btn25)
        
        self.btn22 = Button(x = 520, y=440, width=70, height=70, font_size=10, text="", image=image("Building Icon.png"), action=Building, action_parameter=self)
        self.btn22.set_layer(-2)
        self.add(self.btn22)
        
        self.btn28 = Button(x = 600, y=440, width=70, height=70, font_size=10, text="", image=image("textures/Lodge Icon.png"), action=BuildLodge, action_parameter=self)
        self.btn28.set_layer(-2)
        self.add(self.btn28)
        
        self.btn29 = Button(x = 680, y=440, width=70, height=70, font_size=10, text="", image=image("textures/Hut Icon.png"), action=BuildHut, action_parameter=self)
        self.btn29.set_layer(-2)
        self.add(self.btn29)
        
        self.btn26 = Button(x = 520, y=520, width=70, height=70, font_size=10, text="", image=image("textures/Landmark Icon.png"), action=PlaceLandmark, action_parameter=self)
        self.btn26.set_layer(-2)
        self.add(self.btn26)
        
        self.btn27 = Button(x = 600, y=520, width=70, height=70, font_size=10, text="", image=image("textures/Mission Center Icon.png"), action=PlaceMissionCenter, action_parameter=self)
        self.btn27.set_layer(-2)
        self.add(self.btn27)
        
        
        self.x1 = 500
        self.y1 = 100
        self.x2 = 1500
        self.y2 = 900
        self.menu_color = Color(.9,.95,.9)
        
        
        self.current_action = None
        
        
        
    def paint(self):
        self.draw_rect(self.x1, self.y1, self.x2, self.y2, self.menu_color)
        
def top_button(menu):
    if menu.btn32.text == "topend":
        menu.btn32.text = "topmid"
    else:
        menu.btn32.text = "topend"

def bot_button(menu):
    if menu.btn31.text == "botend":
        menu.btn31.text = "botmid"
    else:
        menu.btn31.text = "botend"
        
def get_mids(menu):
    if menu.btn32.text == "topend" and menu.btn31.text == "botend": return "neither"
    if menu.btn32.text == "topmid" and menu.btn31.text == "botend": return "topmid"
    if menu.btn32.text == "topend" and menu.btn31.text == "botmid": return "botmid"
    if menu.btn32.text == "topmid" and menu.btn31.text == "botmid": return "both"
    fail("???")

def settings(menu):
    
    global build_hs_terminal_model
    global build_fg_terminal_model
    
    
    
    setting = OrderedDict()
    setting["Horizontal Stretch*"] = menu.ui.world.properties["horizontal_stretch"]
    setting["Vertical Stretch*"] = menu.ui.world.properties["vertical_stretch"]
    setting["Sub Chunk Squares"] = menu.ui.world.properties["sub_chunk_squares"]
    setting["Sun Angle*"] = menu.ui.world.properties["sun_angle"]
    setting["Chunk Size*"] = menu.ui.world.properties["chunk_size"]
    setting["Scenery Angle"] = menu.ui.world.properties["scenery_angle"]
    setting["Scenery Height"] = menu.ui.world.properties["scenery_height"]
    setting["Scenery Radius"] = menu.ui.world.properties["scenery_radius"]
    setting["Scenery Segments"] = menu.ui.world.properties["scenery_segments"]
    setting["Scenery Lower Bound"] = menu.ui.world.properties["scenery_lower_stretch"]
    setting["Line of Sight"] = menu.ui.world.view.line_of_sight
    setting["Line of Sight 2"] = menu.ui.world.properties["line_of_sight2"]
    setting["Line of Sight 3"] = menu.ui.world.properties["line_of_sight3"]
    setting["Movement Speed"] = menu.ui.world.view.speed
    setting["Rotation Speed"] = menu.ui.world.view.rot_spd
    setting["Chair Time Interval Detachable"] = menu.ui.world.properties["chair_time_distance_detachable"]
    setting["Chair Time Interval Gondola"] = menu.ui.world.properties["chair_time_distance_gondola"]
    setting["Chair Time Interval Fixed Grip"] = menu.ui.world.properties["chair_time_distance_fixed"]
    setting["Map Editor: Lift Build Pole Distance"] = menu.ui.world.properties["build_chair_pole_distance(map_editor)"]
    setting["Map Editor: Line Thickness"] = menu.ui.world.properties["line_thickness(map_editor)"]
    setting["Map Editor: Terrain Mod Step Size"] = menu.ui.world.properties["terrain_mod_step_size(map_editor)"]
    setting["Map Editor: Bump Placement Chance"] = menu.ui.world.properties["bump_placement_chance(map_editor)"]
    

    
    """
    "chair_time_distance_detachable" : 210,
            "chair_time_distance_gondola" : 300,
            "chair_time_distance_fixed" : 390
    """
    
    col = []
    for key in setting:
        setting[key] = str(setting[key])
        col.append([sg.Text(key), sg.Input(setting[key])])
    
    #FOR ADDING NEW TERMINALS, CHANGE HERE
    col.append([sg.Text("Map Editor: High Speed Terminal Model ("+find_name(build_hs_terminal_model)+")"), sg.Combo(values=["hs_terminal_design_gray", "hs_terminal_design_red","hs_terminal_design_green","hs_terminal_design_blue"], size=(35,10))])
    col.append([sg.Text("Map Editor: Fixed Grip Terminal Model ("+find_name(build_fg_terminal_model)+")"), sg.Combo(values=["terminal_design_2","fg_terminal_design_red","fg_terminal_design_green","fg_terminal_design_blue","fg_terminal_design_black"], size=(35,10))])
    col.append([sg.Text("Change Background"), sg.Input(), sg.FilesBrowse()])
    
    
    
    
    
    
    
    col = sg.Column(col, size=(1000,800), scrollable=True)
    
    layout = [    [sg.OK(), sg.Cancel(), sg.Button("Ok+Reset")],
                  [sg.Text("Settings with the * next to them will not take effect until a reset occurs.")],
                  [sg.Text("    Name: %s" % menu.ui.world.properties["name"])],
                  [sg.Text("    Width: %s" % (menu.ui.world.get_width_floors()*menu.ui.world.properties["horizontal_stretch"]))],
                  [sg.Text("    Height: %s" % (menu.ui.world.get_height_floors()*menu.ui.world.properties["horizontal_stretch"]))],
                  [sg.Text("    Width(Squares): %s" % (menu.ui.world.get_width_floors()))],
                  [sg.Text("    Height(Squares): %s" % (menu.ui.world.get_height_floors()))],
                  [col],
                   ]
    window = sg.Window('', layout, size = (1000,800))
    event, values = window.Read()
    
    
    
    new_settings = OrderedDict()
    i = 0
    for key in setting:
        new_settings[key] = values[i]
        i += 1
    hs_tm = values[i]
    i+=1
    fg_tm = values[i]
    i+=1
    background_file=values[i]
    
    window.close()
    
    def same(key):
        return new_settings[key] == setting[key]
    def nsame(key):
        return not same(key)
    
    if event == "OK" or event=="Ok+Reset":
        try:
            #do all the non-reload settings first...
            menu.ui.world.view.line_of_sight = float(new_settings["Line of Sight"])
            menu.ui.world.view.speed = float(new_settings["Movement Speed"])
            menu.ui.world.view.rot_spd = float(new_settings["Rotation Speed"])
            menu.ui.world.properties["chair_time_distance_detachable"] = float(new_settings["Chair Time Interval Detachable"])
            menu.ui.world.properties["chair_time_distance_gondola"] = float(new_settings["Chair Time Interval Gondola"])
            menu.ui.world.properties["chair_time_distance_fixed"] = float(new_settings["Chair Time Interval Fixed Grip"])
            menu.ui.world.properties["line_thickness(map_editor)"] = float(new_settings["Map Editor: Line Thickness"])
            menu.ui.world.properties["terrain_mod_step_size(map_editor)"] = float(new_settings["Map Editor: Terrain Mod Step Size"])
            menu.ui.world.properties["build_chair_pole_distance(map_editor)"] = float(new_settings["Map Editor: Lift Build Pole Distance"])
            menu.ui.world.properties["bump_placement_chance(map_editor)"] = float(new_settings["Map Editor: Bump Placement Chance"])
            menu.ui.world.properties["line_of_sight2"] = float(new_settings["Line of Sight 2"])
            menu.ui.world.properties["line_of_sight3"] = float(new_settings["Line of Sight 3"])
            menu.ui.world.properties["scenery_angle"] = float(new_settings["Scenery Angle"])
            menu.ui.world.properties["scenery_height"] = float(new_settings["Scenery Height"])
            menu.ui.world.properties["scenery_radius"] = float(new_settings["Scenery Radius"])
            menu.ui.world.properties["scenery_segments"] = float(new_settings["Scenery Segments"])
            menu.ui.world.properties["scenery_lower_stretch"] = float(new_settings["Scenery Lower Bound"])
            
            
            #hs terminal model
            #FOR ADDING NEW TERMINALS, CHANGE HERE
            
            if hs_tm == "hs_terminal_design_gray": build_hs_terminal_model=hs_terminal_design_gray
            if hs_tm == "hs_terminal_design_red": build_hs_terminal_model=hs_terminal_design_red
            if hs_tm == "hs_terminal_design_green": build_hs_terminal_model=hs_terminal_design_green
            if hs_tm == "hs_terminal_design_blue": build_hs_terminal_model=hs_terminal_design_blue
            
            if fg_tm == "terminal_design_2": build_fg_terminal_model=terminal_design_2
            if fg_tm == "fg_terminal_design_red": build_fg_terminal_model=fg_terminal_design_red
            if fg_tm == "fg_terminal_design_green": build_fg_terminal_model=fg_terminal_design_green
            if fg_tm == "fg_terminal_design_blue": build_fg_terminal_model=fg_terminal_design_blue
            if fg_tm == "fg_terminal_design_gray": build_fg_terminal_model=fg_terminal_design_gray
            if fg_tm == "fg_terminal_design_black": build_fg_terminal_model=fg_terminal_design_black
            
            
            if background_file.lower() in ["none","no","blank","empty","nothing"]:
                menu.ui.world.pan_background = None
            try:
                new_back = image(background_file)
                menu.ui.world.pan_background = new_back,new_back.tobytes("raw", "RGBA", 0, -1)
            except:
                pass
            
            
            
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
                    #chairlift.update_object_account()
                            
            menu.ui.world.properties["sub_chunk_squares"] = int(new_settings["Sub Chunk Squares"])
            if nsame("Sub Chunk Squares"):
                if event != "Ok+Reset":
                    sg.Popup("Please wait for all chunks to reset.")
                    for z in range(menu.ui.world.get_height_chunks()):
                        for x in range(menu.ui.world.get_width_chunks()):
                            menu.ui.world.chunks[z][x].colors_changed = True
            
            
            # settings involving reset
            
            
            
            if event=="Ok+Reset":
                menu.ui.world.properties["sun_angle"] = float(new_settings["Sun Angle*"])
                menu.ui.world.properties["horizontal_stretch"] = float(new_settings["Horizontal Stretch*"])
                menu.ui.world.properties["vertical_stretch"] = float(new_settings["Vertical Stretch*"])
                menu.ui.world.reset(new_chunk_size = int(new_settings["Chunk Size*"]))
                world_save.write(menu.ui.world)
                
                
        except Exception as e:
            traceback.print_exc()
            sg.Popup(str(e))
                
                
        
    
def save(menu):
    world_save.write(menu.ui.world)
def exit(menu):
    
    layout = [[sg.Text("Save or not?")],
                        [sg.Yes(), sg.No()]]
    window = sg.Window('', layout, size = (500,300))
    event, _ = window.Read()
    window.close()
    
    if event == "Yes":
        save(menu)
    elif event == None:
        return
        
    menu.ui.stop_sounds()
    #code for exiting:
    #print("going to deactivate",pylooiengine.main_window.unlayered_looi_objects+main_window.layered_looi_objects+main_window.transfer_to_unlayered_looi_objects+main_window.transfer_to_layered_looi_objects)
    for looi_object in pylooiengine.main_window.unlayered_looi_objects+main_window.layered_looi_objects+main_window.transfer_to_unlayered_looi_objects+main_window.transfer_to_layered_looi_objects:
        try:
            looi_object.deactivate()
        except:
            raise Exception("Cannot remove this looiobject " + str(looi_object) + "see because it's active variable is " + str(looi_object.active))
    
    rooms.main_menu()
    """
    main_window.unlayered_looi_objects = []
    main_window.layered_looi_objects = []
    main_window.transfer_to_unlayered_looi_objects = []
    main_window.transfer_to_layered_looi_objects = []
    main_window.to_remove = []
    """


    
    
class MapEdit(LooiObject):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.live_pointer = Pointer(self.world(), 0, 0)
    def world(self):
        return self.menu.ui.world
    def live_pointer_update(self):
        live_point = self.world().get_view_pointing()
        if live_point != None:
            self.live_pointer.z = live_point[0]
            self.live_pointer.x = live_point[1]
    def upon_deactivation(self):
        super().upon_deactivation()
        self.menu.ui.enable_crosshairs(False)
        self.menu.current_action = None
        self.menu.ui.interface_mode = "menu"
        game_ui.set_mouse_mode("normal")
        self.menu.activate()
        self.live_pointer.deactivate()
class Measure(MapEdit):
    def __init__(self, menu):
        super().__init__(menu)
        self.set_layer(9999)
        menu.ui.enable_crosshairs(True)
        game_ui.set_mouse_mode("3D")
        menu.ui.interface_mode = "can_move_temporarily"
        menu.deactivate()
        
        hs = self.world().properties["horizontal_stretch"]
        self.x1, self.y1, self.z1 = int(self.world().view.x), self.world().get_elevation_continuous(self.world().view.z/hs,self.world().view.x/hs)*self.world().properties["vertical_stretch"], int(self.world().view.z)
        self.x2=0
        self.y2=0
        self.z2=0
    def step(self):
        if self.mouse("left","pressed"):
            self.deactivate()
    def paint(self):
        point = self.world().get_view_pointing()
        if point == None:
            return
        elev = self.world().get_elevation(point[0],point[1],scaled=True)
        
        hs = self.world().properties["horizontal_stretch"]
        self.x2, self.y2, self.z2 = point[1]*hs, elev, point[0]*hs
        
        
        
        
        
        self.draw_line_3d(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, green, 5, setup_3d=self.world().get_setup_3d_close())
        
        
        
        x1=self.x1
        x2=self.x2
        y1=self.y1
        y2=self.y2
        z1=self.z1
        z2=self.z2
        
        size = 20
        font = "Courier New"
        line = 50
        inc = 24
        self.draw_text(0,line,"x=%d, y=%d, z=%d"%(x2,y2,z2), font_size = size, font = font)
        line+=inc
        self.draw_text(0,line,"grid_x=%d, grid_y=%d, grid_z=%d"%(x2/hs,y2/self.world().properties["vertical_stretch"],z2/hs), font_size = size, font=font)
        
        dx = x2-x1
        dy = y2-y1
        dz = z2-z1
        dground = (dx**2+dz**2)**.5
        if dx == 0:
            hr = math.pi/2 if dz > 0 else -math.pi/2
        else:
            hr = math.atan(dz/dx)
        if dx < 0:
            hr += math.pi
        
        hr=-hr#flip for computer coordinates
        if hr < 0:
            hr += 2*math.pi
        vr = math.atan(dy/dground)
        
        line+=inc
        self.draw_text(0,line,"ground_angle= %f pi, vertical_angle=%f pi"%(hr/math.pi, vr/math.pi), font_size = size, font=font)
        
        q=constants["scaled_distance_to_meters"]
        d3d = ((z1-z2)**2+(x1-x2)**2+(y1-y2)**2)**.5
        line+=inc
        self.draw_text(0,line,"ground_distance=%f, 3d_distance=%f, real_world_ground_distance_meters=%f, real_world_3d_distance_meters=%f"%(dground,d3d,dground*q,d3d*q), font_size = size, font=font)
        
        line+=inc
        self.draw_text(0,line,"real_world_ground_distance_miles=%f, real_world_3d_distance_miles=%f"%(dground*q*.000621,d3d*q*.000621), font_size = size, font=font)

class OnePointEdit(MapEdit):
    def __init__(self, menu, message1="Select point"):
        super().__init__(menu)
        self.stage = "select point"
        self.p1 = None
        self.message1 = message1
        
        
        menu.ui.enable_crosshairs(True)
        game_ui.set_mouse_mode("3D")
        menu.ui.interface_mode = "can_move_temporarily"
        menu.deactivate()
        menu.current_action = self
        
    def step(self):
        self.live_pointer_update()
        if self.mouse("left", "pressed") or self.mouse("left", "released"):
            if self.stage == "select point":
                self.p1 = self.world().get_view_pointing()
                if self.p1 != None:
                    self.execute(self.p1)
                    self.deactivate()
                    
    def paint(self):
        if self.stage == "select point":
            self.draw_text(800, 100, self.message1)
            
    #abstract method
    def execute(self, p1):
        pass


class TwoPointEdit(MapEdit):
    def __init__(self, menu, message1="Select point 1", message2="Select point 2"):
        super().__init__(menu)
        self.stage = "select p1"
        self.p1 = None
        self.p2 = None
        self.message1 = message1
        self.message2 = message2
        self.pointer = None
        
        
        menu.ui.enable_crosshairs(True)
        game_ui.set_mouse_mode("3D")
        menu.ui.interface_mode = "can_move_temporarily"
        menu.deactivate()
        menu.current_action = self
    
    def step(self):
        self.live_pointer_update()
            
        
    
    
        if self.mouse("left", "pressed") or self.mouse("left", "released"):
            if self.stage == "select p1":
                self.p1 = self.world().get_view_pointing()
                if self.p1 != None:
                    self.stage = "select p2"
                    self.pointer = Pointer(self.world(), self.p1[0], self.p1[1])
            elif self.stage == "select p2":
                self.p2 = self.world().get_view_pointing()
                if self.p2 != None:
                    self.stage = "done"
                    self.execute(self.p1, self.p2)
                    self.pointer.deactivate()
                    self.deactivate()
    def paint(self):
        if self.stage == "select p1":
            self.draw_text(800, 100, self.message1)
        if self.stage == "select p2":
            self.draw_text(800, 100, self.message2)
            
    #abstract method
    def execute(self, p1, p2):
        pass
        
        

"""
Start Map Edits
"""
class Building(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select location", "Select angle")
      
    def execute(self, p1, p2):
        game_ui.set_mouse_mode("normal")
        layout = [
            [sg.Text("Design:"), sg.Combo(values=building_models, size=(50,10))],
            [sg.Text("Params:"), sg.Multiline(default_text="{}", size=(300,10))],
            [sg.OK()]
            
            ]
        window = sg.Window('', layout, size = (500,800))
        event, values = window.Read()
        window.close()
        if event == "OK":
            try:
                #print(values)
                rot = get_angle(p1[0], p1[1], p2[0], p2[1])
                design = eval(values[0])
                params = eval(values[1])
                b = building.Building(p1[0], p1[1], self.world(), design, params, rot)
            except Exception as e:
                sg.Popup(str(e))
                traceback.print_exc()
class PlaceMissionCenter(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select location", "Select angle")
      
    def execute(self, p1, p2):
        rot = get_angle(p1[0], p1[1], p2[0], p2[1])
        mission_center.MissionCenter(z=p1[0], x=p1[1], world=self.world(), rotation=rot)
            
class BuildLodge(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select location", "Select angle")
      
    def execute(self, p1, p2):
        rot = get_angle(p1[0], p1[1], p2[0], p2[1])
        lodge.Lodge(z=p1[0], x=p1[1], world=self.world(), rotation=rot)
class BuildHut(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select location", "Select angle")
      
    def execute(self, p1, p2):
        rot = get_angle(p1[0], p1[1], p2[0], p2[1])
        lodge.Hut(z=p1[0], x=p1[1], world=self.world(), rotation=rot)
            
                
class PlaceBumps(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
      
    def execute(self, p1, p2):
        place_bumps(self.world(), p1[0], p1[1], p2[0], p2[1], chance = self.world().properties["bump_placement_chance(map_editor)"])
class RemoveBumps(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
      
    def execute(self, p1, p2):
        remove_bumps(self.world(), p1[0], p1[1], p2[0], p2[1])

class LiftBuild(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
      
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], chair_time_distance = self.world().properties["chair_time_distance_detachable"], terminal_model=build_hs_terminal_model, mids=get_mids(self.menu))

class GondolaBuild(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
      
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], chair_model=gondola_model_1, blurry_chair_model=gondola_model_2, super_blurry_chair_model=gondola_model_4, chair_riding_model = gondola_model_1_riding, chair_time_distance = self.world().properties["chair_time_distance_gondola"], terminal_speed="gondola_terminal_speed", rope_speed="gondola_rope_speed", terminal_model=build_hs_terminal_model, mids=get_mids(self.menu))
        
        
        
class C4Build(TwoPointEdit):#quad moves a bit faster than the other fixed grip chairs
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], terminal_speed="fixed_grip_terminal_speed", rope_speed="fixed_grip_rope_speed", terminal_model=build_fg_terminal_model, chair_time_distance = self.world().properties["chair_time_distance_fixed"])
class D_6CBuild(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], chair_model = sixpack_model_1, blurry_chair_model = sixpack_model_2, super_blurry_chair_model=sixpack_model_3, chair_time_distance = self.world().properties["chair_time_distance_detachable"], chair_riding_model = sixpack_model_1, terminal_model=build_hs_terminal_model, mids=get_mids(self.menu))

class C3Build(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], terminal_speed="fixed_grip_terminal_speed", rope_speed="fixed_grip_rope_speed", terminal_model=build_fg_terminal_model, chair_model = triple_model_1, blurry_chair_model = triple_model_2, super_blurry_chair_model=triple_model_3, chair_time_distance = self.world().properties["chair_time_distance_fixed"], chair_riding_model = triple_model_1)
class C2Build(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], terminal_speed="fixed_grip_terminal_speed", rope_speed="fixed_grip_rope_speed", terminal_model=build_fg_terminal_model, chair_model = double_model_1, blurry_chair_model = double_model_2, super_blurry_chair_model=double_model_3, chair_time_distance = self.world().properties["chair_time_distance_fixed"], chair_riding_model = double_model_1)
class TBarBuild(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu, "Select bottom", "Select top")
    def execute(self, p1, p2):
        l = Lift(self.world())
        
        
        #calculate pole positions
        z1 = p1[0]*self.world().properties["horizontal_stretch"]
        z2 = p2[0]*self.world().properties["horizontal_stretch"]
        x1 = p1[1]*self.world().properties["horizontal_stretch"]
        x2 = p2[1]*self.world().properties["horizontal_stretch"]
        distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
        distance_between_poles = self.world().properties["build_chair_pole_distance(map_editor)"]
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]], terminal_speed="fixed_grip_terminal_speed", rope_speed="fixed_grip_rope_speed", terminal_model=build_fg_terminal_model, chair_model = tbar_model_1, blurry_chair_model = tbar_model_1, super_blurry_chair_model=tbar_model_1,pole_model=pole_design_2, chair_time_distance = self.world().properties["chair_time_distance_fixed"], chair_riding_model = tbar_model_1)


#terminal_design_2
class TreeAdd(TwoPointEdit):
    def __init__(self, param):
        menu, density = param
        super().__init__(menu, "Select corner 1", "Select corner 2")
        self.density = density
    def execute(self, p1, p2):
        fill_trees_circular(self.world(), p1[0], p1[1], p2[0], p2[1], self.density)
def TreeFilter(menu):
    layout = [
    [sg.Text("Filtering trees helps reduce lag by thinning out dense patches of trees.")],
    [sg.Text("Remove all trees with "), sg.Input(7)], 
    [sg.Text(" or more nearby trees (max 20 nearby trees for fully surrounded tree)")],
    [sg.Text("You may want to save before carrying through with this operation.")],
    [sg.OK(), sg.Cancel()],
    ]
    window = sg.Window('', layout, size = (700,300))
    event, values = window.Read()
    window.close()
    if event == None or event == "Cancel":
        return
    try:
        trees_to_remove = []
        threshold = int(values[0])
        for z in range(2, menu.ui.world.get_height_floors()-2):
            for x in range(2, menu.ui.world.get_width_floors()-2):
                for obj in list(menu.ui.world.quads[z][x].containedObjects):
                    if isinstance(obj, Tree):
                        
                        #count adjacent trees
                        adjacent_trees = 0
                        for zz,xx in [(z-1,x-1),(z-1,x),(z-1,x+1),(z,x-1),(z,x+1),(z+1,x-1),(z+1,x),(z+1,x+1),
                                        (z-2,x-1),(z-2,x),(z-2,x+1),(z+2,x-1),(z+2,x),(z+2,x+1),
                                        (z-1,x-2),(z,x-2),(z+1,x-2),(z-1,x+2),(z,x+2),(z+1,x+2)]:
                            for obj2 in list(menu.ui.world.quads[zz][xx].containedObjects):
                                if isinstance(obj2, Tree):
                                    adjacent_trees += 1
                            
                        if adjacent_trees >= threshold: trees_to_remove.append(obj)
                            
                        break
        for tree in trees_to_remove:
            tree.delete()
    except Exception as e:
        sg.Popup(str(e))
                                
                            
                        
                        
        



class Chainsaw(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1, p2):
        chainsaw_circular(self.world(), p1[0], p1[1], p2[0], p2[1])
        
class ChainsawStraight(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1, p2):
        chainsaw_straight(self.world(), p1[0], p1[1], p2[0], p2[1], self.world().properties["line_thickness(map_editor)"])
class Select(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1, p2):
        z1 = p1[0]
        x1 = p1[1]
        
        z2 = p2[0]
        x2 = p2[1]
        
        midz = (z1+z2)/2
        midx = (x1+x2)/2
        
        radius = ((midz-z1)**2 + (midx-x1)**2)**.5
        
        
        selectables = []
        for z in range(int(midz-radius), int(midz+radius)+1):
            for x in range(int(midx-radius), int(midx+radius)+1):
                if ((z-midz)**2 + (x-midx)**2)**.5 <= radius and self.world().valid_floor(z, x):
                    objs = self.world().quads[z][x].containedObjects
                    for obj in objs:
                        
                        if isinstance(obj, Terminal):
                            game_ui.set_mouse_mode("normal")
                            the_lift = obj.chairlift
                            selectables.append(the_lift)
                            
                        elif isinstance(obj, Selectable):
                            game_ui.set_mouse_mode("normal")
                            selectables.append(obj)
                        elif isinstance(obj, WorldObject):
                            game_ui.set_mouse_mode("normal")
                            selectables.append(obj)
        if len(selectables) <= 70:
            try:
                seen_lift = False
                for selectable in selectables:
                    
                    if isinstance(selectable, Lift):
                        if seen_lift:
                            continue
                        else:
                            seen_lift=True
                    selectable.open_menu()
                    
            except StopSelectingException:
                layout = [[sg.Text("aborted")]]
                window = sg.Window("", layout, size=(250, 150))
                event, values = window.Read()
                window.close()
        else:
            sg.Popup("Cannot select more than 70 objects. Try again.")

"""
terrain edits
"""
class TerrainMod(TwoPointEdit):
    def __init__(self, menu, message1="Select point 1", message2="Select point 2", message3="Up and down arrows to move. Left click to exit.", num_pointers=8):
        super().__init__(menu, message1, message2)
        self.pointers = []
        
        self.num_pointers = num_pointers
        self.message3 = message3
    def execute(self, p1, p2):
        
        z1=p1[0]
        x1=p1[1]
        z2=p2[0]
        x2=p2[1]
        
        
        
        center_z = (z1+z2)/2
        center_x = (x1+x2)/2
        
        angle = get_angle(z2,x2,z1,x1)
        radius = ((z1-z2) ** 2 + (x1-x2) ** 2)**.5 /2
        
        
        angle_between_pointers = 1/self.num_pointers * 2*math.pi
        for i in range(1,self.num_pointers):
            angle_to_this_pointer = angle + i * angle_between_pointers
            
        
            pointerz = int(center_z - math.sin(angle_to_this_pointer) * radius)
            pointerx = int(center_x + math.cos(angle_to_this_pointer) * radius)
            
            if self.world().valid_point(pointerz, pointerx):
                self.pointers.append(Pointer(self.world(), pointerz, pointerx))
        
            
        
    def step(self):
        self.live_pointer_update()
        if self.stage == "modify terrain":
            if self.key("up", "down"):
                self.up()
            if self.key("down", "down"):
                self.down()
            if self.mouse("left", "pressed") or self.mouse("left", "released"):
                self.stage = "done"
                self.pointer.deactivate()
                for pointer in self.pointers:
                    pointer.deactivate()
                self.deactivate()
                natural_bumps(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1])
        if self.mouse("left", "pressed") or self.mouse("left", "released"):
            if self.stage == "select p1":
                self.p1 = self.world().get_view_pointing()
                if self.p1 != None:
                    self.stage = "select p2"
                    self.pointer = Pointer(self.world(), self.p1[0], self.p1[1])
            elif self.stage == "select p2":
                self.p2 = self.world().get_view_pointing()
                if self.p2 != None:
                    
                    self.execute(self.p1, self.p2)
                    self.stage = "modify terrain"
                    remove_natural_bumps(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1])
                    
        
    def up():pass
    def down():pass
    def paint(self):
        if self.stage == "select p1":
            self.draw_text(800, 100, self.message1)
        if self.stage == "select p2":
            self.draw_text(800, 100, self.message2)
        if self.stage == "modify terrain":
            self.draw_text(400, 100, self.message3)
        
class HillMod(TerrainMod):
    def __init__(self, menu):
        super().__init__(menu)
    def up(self):
        raise_hill(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1], self.world().properties["terrain_mod_step_size(map_editor)"])
    def down(self):
        raise_hill(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1], -self.world().properties["terrain_mod_step_size(map_editor)"])
        
        
        
class SmoothMod(TerrainMod):
    def __init__(self, menu):
        super().__init__(menu)
    def up(self):
        smooth(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1])
    def down(self):
        smooth(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1])
        
        
class PlateauMod(TerrainMod):
    def __init__(self, menu):
        super().__init__(menu)
    def up(self):
        plateau(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1], self.world().properties["terrain_mod_step_size(map_editor)"])
    def down(self):
        plateau(self.world(), self.p1[0], self.p1[1], self.p2[0], self.p2[1], -self.world().properties["terrain_mod_step_size(map_editor)"])
class PathMod(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1, p2):
        path(self.world(), p1[0], p1[1], p2[0], p2[1], self.world().properties["line_thickness(map_editor)"])
class PlaceRock(OnePointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, point):
        Rock(z=point[0], x=point[1], world=self.world())
class PlaceWorldObject(OnePointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, point):
        WorldObject(world=self.world(), z=point[0], x=point[1], model=rock_design_2, model_type="std")
class PlaceRock2(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1,p2):
        cliffs(self.world(),p1[0], p1[1], p2[0], p2[1])
class PlaceLandmark(OnePointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, point):
        Landmark(z=point[0], x=point[1], world=self.world())
"""
End map edits
"""

def pointer_model(
            width = 4,
            height = 10,
            color1 = [0,0,1],
            color2 = [0,1,0]
        ):
    
    return [
    [-width/2, 0, 0], [-width/2, 0, 0], [width/2, 0, 0], [0, -height, 0], color1,
    [0, 0, -width/2], [0, 0, -width/2], [0, 0, width/2], [0, -height, 0], color2,
    ]
"""
This thing just is a graphical pointer that points to a spot in the ground

x and z are unscaled values
"""
class Pointer(LooiObject):
    def __init__(self, world, z, x):
        super().__init__()
        self.z = z
        self.x = x
        self.world = world
        self.rotation = 0
        self.rotation_speed = math.pi/40
        
    def step(self):
        model = pointer_model()
        horizontal_rotate_model_around_origin(model, self.rotation)
        move_model(model, self.x*self.world.properties["horizontal_stretch"], self.world.get_elevation(self.z, self.x, scaled = True) + 15, self.z*self.world.properties["horizontal_stretch"])
        add_model_to_world_mobile(model, self.world)
        self.rotation += self.rotation_speed
        




