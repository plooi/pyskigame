from pylooiengine import *
from pylooiengine.gui import *
from lift import *
import game_ui
from world_operations import *
class Menu(LooiObject):
    def __init__(self, ui):
        super().__init__()
        self.set_layer(2)
        self.ui = ui
        
        self.btn1 = Button(x = 520, y=120, width=80, height=80, font_size=10, text="", image=image("High Speed Quad Icon.png"), action=lift_button, action_parameter=self)
        self.btn1.set_layer(-2)
        self.add(self.btn1)
        
        
        self.btn2 = Button(x = 520, y=200, width=80, height=80, font_size=10, text="", image=image("Tree Icon.png"), action=tree_button, action_parameter=self)
        self.btn2.set_layer(-2)
        self.add(self.btn2)
        
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
def lift_button(menu):
    menu.ui.enable_crosshairs(True)
    game_ui.set_mouse_mode("3D")
    menu.ui.interface_mode = "can_move_temporarily"
    menu.deactivate()
    menu.current_action = LiftBuild(menu)
    

    
    
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
    
class LiftBuild(MapEdit):
    def __init__(self, menu):
        super().__init__(menu)
        self.stage = "select bottom"
        self.bottom = None
        self.top = None
        
    def step(self):
        if self.mouse("left", "released"):
            if self.stage == "select bottom":
                self.bottom = self.world().get_view_pointing()
                if self.bottom != None:
                    self.stage = "select top"
            elif self.stage == "select top":
                self.top = self.world().get_view_pointing()
                if self.top != None:
                    self.stage = "done"
                    l = Lift(self.world())
                    
                    
                    #calculate pole positions
                    z1 = self.bottom[0]*self.world().properties["horizontal_stretch"]
                    z2 = self.top[0]*self.world().properties["horizontal_stretch"]
                    x1 = self.bottom[1]*self.world().properties["horizontal_stretch"]
                    x2 = self.top[1]*self.world().properties["horizontal_stretch"]
                    distance = ((z2-z1)**2 + (x2-x1)**2) ** .5#total distance
                    distance_between_poles = 23
                    #end
                    
                    
                    
                    l.build([self.bottom[0],self.bottom[1],[x/distance for x in range(int(distance_between_poles), int(distance-distance_between_poles), int(distance_between_poles))],self.top[0],self.top[1]])
                    
                    self.deactivate()
            
    def paint(self):
        if self.stage == "select bottom":
            self.draw_text(800, 100, "Select Bottom")
        if self.stage == "select top":
            self.draw_text(800, 100, "Select Top")
            




def tree_button(menu):
    menu.ui.enable_crosshairs(True)
    game_ui.set_mouse_mode("3D")
    menu.ui.interface_mode = "can_move_temporarily"
    menu.deactivate()
    menu.current_action = TreeAdd(menu)


class TreeAdd(MapEdit):
    def __init__(self, menu):
        super().__init__(menu)
        self.stage = "select corner 1"
        self.c1 = None
        self.c2 = None
        
    def step(self):
        if self.mouse("left", "released"):
            if self.stage == "select corner 1":
                self.c1 = self.world().get_view_pointing()
                if self.c1 != None:
                    self.stage = "select corner 2"
            elif self.stage == "select corner 2":
                self.c2 = self.world().get_view_pointing()
                if self.c2 != None:
                    self.stage = "done"
                    fill_trees(self.world(), self.c1[0], self.c1[1], self.c2[0], self.c2[1])
                    self.deactivate()
            
    def paint(self):
        if self.stage == "select corner 1":
            self.draw_text(800, 100, "Select Corner")
        if self.stage == "select corner 2":
            self.draw_text(800, 100, "Select Other Corner")
            
    



