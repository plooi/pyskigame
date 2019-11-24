from pylooiengine import *
from pylooiengine.gui import *
from lift import *
class Menu(LooiObject):
    def __init__(self, player):
        super().__init__(active = False)
        self.set_layer(1)
        self.player = player
        
        self.btn1 = Button(x = 520, y=120, width=80, height=80, font_size=10, text="Lift", action=lift_button, action_parameter=self)
        self.btn1.deactivate()
        self.btn1.set_layer(0)
        self.add(self.btn1)
        
        self.x1 = 500
        self.y1 = 100
        self.x2 = 1500
        self.y2 = 900
        self.menu_color = Color(.9,.95,.9)
        
        
        self.current_action = None
    def paint(self):
        self.draw_rect(self.x1, self.y1, self.x2, self.y2, self.menu_color)
    
    def upon_activation(self):
        super().upon_activation()
        if self.current_action != None:
            self.current_action.decativate()
def lift_button(menu):
    menu.player.end_menu()
    LiftBuild(menu)
class MapEdit(LooiObject):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
    def world(self):
        return self.menu.player.world
    
class LiftBuild(MapEdit):
    def __init__(self, menu):
        super().__init__(menu)
        self.stage = "select bottom"
        self.bottom = None
        self.top = None
        self.menu.player.enable_crosshairs(True)
    def step(self):
        if self.mouse("left", "released"):
            if self.stage == "select bottom":
                self.bottom = self.world().get_player_pointing()
                if self.bottom != None:
                    self.stage = "select top"
            elif self.stage == "select top":
                self.top = self.world().get_player_pointing()
                if self.top != None:
                    self.stage = "done"
                    l = Lift(self.world())
                    l.build([self.bottom[0],self.bottom[1],[x/100 for x in range(10,100,7)],self.top[0],self.top[1]], rope_speed = .2, terminal_speed = .05, chair_time_distance=50)
                    
                    self.deactivate()
            
    def paint(self):
        if self.stage == "select bottom":
            self.draw_text(800, 100, "Select Bottom")
        if self.stage == "select top":
            self.draw_text(800, 100, "Select Top")
            
    def upon_deactivation(self):
        super().upon_deactivation()
        self.menu.player.enable_crosshairs(False)











