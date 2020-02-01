from pylooiengine import *
from pylooiengine.gui import *
from lift import *
import game_ui
from world_operations import *
from model_3d import *
import lift
import world_save

def test(menu):
    world_save.write(menu.ui.world)

class Menu(LooiObject):
    def __init__(self, ui):
        super().__init__()
        self.set_layer(2)
        self.ui = ui
        
        self.btn1 = Button(x = 520, y=120, width=80, height=80, font_size=10, text="", image=image("High Speed Quad Icon.png"), action=LiftBuild, action_parameter=self)
        self.btn1.set_layer(-2)
        self.add(self.btn1)
        
        
        self.btn2 = Button(x = 520, y=200, width=80, height=80, font_size=10, text="", image=image("Tree Icon.png"), action=TreeAdd, action_parameter=(self, .1))
        self.btn2.set_layer(-2)
        self.add(self.btn2)
        
        self.btn3 = Button(x = 520, y=280, width=80, height=80, font_size=10, text="", image=image("Tree Icon2.png"), action=TreeAdd, action_parameter=(self, .3))
        self.btn3.set_layer(-2)
        self.add(self.btn3)
        
        self.btn4 = Button(x = 520, y=360, width=80, height=80, font_size=10, text="", image=image("Tree Icon3.png"), action=TreeAdd, action_parameter=(self, .5))
        self.btn4.set_layer(-2)
        self.add(self.btn4)
        
        self.btn5 = Button(x = 520, y=440, width=80, height=80, font_size=10, text="", image=image("Chainsaw.png"), action=Chainsaw, action_parameter=self)
        self.btn5.set_layer(-2)
        self.add(self.btn5)
        
        self.btn6 = Button(x = 520, y=520, width=80, height=80, font_size=10, text="", image=image("Select.png"), action=Select, action_parameter=self)
        self.btn6.set_layer(-2)
        self.add(self.btn6)
        
        self.btn7 = Button(x = 820, y=520, width=80, height=80, font_size=10, text="", image=image("Select.png"), action=test, action_parameter=self)
        self.btn7.set_layer(-2)
        self.add(self.btn7)
        
        
        self.x1 = 500
        self.y1 = 100
        self.x2 = 1500
        self.y2 = 900
        self.menu_color = Color(.9,.95,.9)
        
        
        self.current_action = None
        
        
    def paint(self):
        self.draw_rect(self.x1, self.y1, self.x2, self.y2, self.menu_color)
    """
    def upon_activation(self):
        super().upon_activation()
        if self.current_action != None:
            self.current_action.decativate()
    """


    
    
class MapEdit(LooiObject):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
    def world(self):
        return self.menu.ui.world
    def upon_deactivation(self):
        super().upon_deactivation()
        self.menu.ui.enable_crosshairs(False)
        self.menu.current_action = None
        self.menu.ui.interface_mode = "menu"
        game_ui.set_mouse_mode("normal")
        self.menu.activate()
    
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
        distance_between_poles = 23
        #end
        
        l.build([p1[0],p1[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],p2[0],p2[1]])
        

class TreeAdd(TwoPointEdit):
    def __init__(self, param):
        menu, density = param
        super().__init__(menu, "Select corner 1", "Select corner 2")
        self.density = density
    def execute(self, p1, p2):
        fill_trees_circular(self.world(), p1[0], p1[1], p2[0], p2[1], self.density)



class Chainsaw(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1, p2):
        chainsaw_circular(self.world(), p1[0], p1[1], p2[0], p2[1])
        

class Select(TwoPointEdit):
    def __init__(self, menu):
        super().__init__(menu)
    def execute(self, p1, p2):
        z1 = p1[0]
        x1 = p1[1]
        
        z2 = p2[0]
        x2 = p2[1]
        for z in range(min([z1,z2]), max([z1,z2])+1):
            for x in range(min([x1,x2]), max([x1,x2])+1):
                objs = self.world().quads[z][x].containedObjects
                for obj in objs:
                    
                    if isinstance(obj, lift.Terminal):
                        game_ui.set_mouse_mode("normal")
                        the_lift = obj.chairlift
                        layout = [
                            [sg.Button("Delete"), sg.Text("                              ")],
                            [sg.Text("             ")] ,
                            [sg.Text("             ")] ,
                            [sg.Text("             ")] ,
                            [sg.Text("             ")] ,
                            [sg.Text("             ")] ,
                        
                        
                        
                        ]
                        
                        
                        window = sg.Window("Chairlift", layout, size=(500,800))
                        event, values = window.Read()
                        
                        #insert code that affects the chairlift here
                        if event == "Delete":
                            the_lift.delete()
                        
                        
                        
                        window.close()
                        return
                        
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
        
        



