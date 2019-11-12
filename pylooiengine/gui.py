import pylooiengine
from pylooiengine import *
import easygui

def text_input(prompt=""):
    return easygui.enterbox(prompt)
def alert(message="Alert", title="Alert"):
    easygui.msgbox(message, title)
class Rectangle(LooiObject):
    def __init__(self, x=0, y=0, width=100, height=100, color=light_gray, image=None):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        
    def paint(self):
        if image == None:
            self.draw_rect(self.x, self.y, self.x + self.width, self.y + self.height, self.color)
        else:
            self.draw_image(self.x, self.y, self.x + self.width, self.y + self.height, self.image)
class Label(LooiObject):
    def __init__(self, x=0, y=0, width=100, height=100, text="Label", color=light_gray, text_color=black, font_size=50, font = "Microsoft Sans Serif"):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font = font
        self.color = color
        self.text_color = text_color
        
    def paint(self):
        self.draw_text(self.x + 5, self.y + self.height/2, self.text, self.font_size, self.text_color, self.color, self.font)
        self.draw_rect(self.x, self.y, self.x + self.width, self.y + self.height, self.color)
class Button(LooiObject):
    def __init__(self, x=0, y=0, width=100, height=100, text="Button", action=lambda x: 0, color=light_gray, text_color=black, font_size=50, font="Microsoft Sans Serif"):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        
        self.color = None
        self.right_color = None
        self.bot_color = None
        self.text_color = None
        self.bot_color_lit = None
        self.right_color_lit = None
        self.color_lit = None
        
        self.button_depth = width/20
        self.set_color(color)
        self.set_text_color(text_color)
        self.text = text
        self.font_size = font_size
        self.font = font
        self.mouse_on = False
        self.pressed = False
    def set_color(self, color):
        self.color = color
        self.calculate_colors(color)
    def calculate_colors(self, button_color):
        self.right_color = button_color.lighter(.3)
        self.bot_color = button_color.darker(.3)
        self.bot_color_lit = self.bot_color.lighter(.2)
        self.right_color_lit = self.right_color.lighter(.2)
        self.color_lit = button_color.lighter(.2)
    def set_text_color(self, color):
        self.text_color = color
    def step(self):
        mouse_x, mouse_y = self.get_mouse_pos()
        if mouse_x >= self.x and mouse_x <= self.x+self.width+self.button_depth and mouse_y >= self.y and mouse_y <= self.y+self.height+self.button_depth:
            self.mouse_on = True
        else:
            self.mouse_on = False
        if self.pressed and self.mouse("left", "released"):
            self.action()
        if self.mouse("left", "down") and self.mouse_on:
            self.pressed = True
        else:
            self.pressed = False
    def paint(self):
        
        
        self.do_text()
        if self.pressed:
            self.draw_rect(self.x + self.button_depth, self.y + self.button_depth, self.x + self.button_depth + self.width, self.y + self.button_depth + self.height, self.color)
            self.draw_quad(
                            self.x, self.y, 
                            self.x + self.button_depth, self.y + self.button_depth, 
                            self.x + self.button_depth, self.y + self.height + self.button_depth, 
                            self.x, self.y + self.height + self.button_depth,
                            self.right_color)
            self.draw_quad(
                            self.x, self.y, 
                            self.x + self.button_depth, self.y + self.button_depth, 
                            self.x + self.width + self.button_depth, self.y + self.button_depth, 
                            self.x + self.width + self.button_depth, self.y, 
                            self.bot_color)
        elif self.mouse_on:
            self.draw_rect(self.x, self.y, self.x + self.width, self.y + self.height, self.color_lit)
            self.draw_quad(
                            self.x + self.width, self.y, 
                            self.x + self.width + self.button_depth, self.y, 
                            self.x + self.width + self.button_depth, self.y + self.height + self.button_depth, 
                            self.x + self.width, self.y + self.height,
                            self.right_color_lit)
            self.draw_quad(
                            self.x, self.y + self.height, 
                            self.x, self.y + self.height + self.button_depth,
                            self.x + self.width + self.button_depth, self.y + self.height + self.button_depth, 
                            self.x + self.width, self.y + self.height, 
                            self.bot_color_lit)
        else:
            self.draw_rect(self.x, self.y, self.x + self.width, self.y + self.height, self.color)
            self.draw_quad(
                            self.x + self.width, self.y, 
                            self.x + self.width + self.button_depth, self.y, 
                            self.x + self.width + self.button_depth, self.y + self.height + self.button_depth, 
                            self.x + self.width, self.y + self.height,
                            self.right_color)
            self.draw_quad(
                            self.x, self.y + self.height, 
                            self.x, self.y + self.height + self.button_depth,
                            self.x + self.width + self.button_depth, self.y + self.height + self.button_depth, 
                            self.x + self.width, self.y + self.height, 
                            self.bot_color)
    def do_text(self):
        if self.pressed:
            self.draw_text(self.x + 5 + self.button_depth, self.y + self.height/2 + self.button_depth + self.font_size/2, self.text, self.font_size, self.text_color, self.color, self.font)
        elif self.mouse_on:
            self.draw_text(self.x + 5, self.y + self.height/2 + self.font_size/2, self.text, self.font_size, self.text_color, self.color_lit, self.font)
        else:
            self.draw_text(self.x + 5, self.y + self.height/2 + self.font_size/2, self.text, self.font_size, self.text_color, self.color, self.font)
def do(b):
    print("hi")
def main():
    w = Window()
    Button(500,500,200,200,color=green,action=do)
    Label(1000,500,300,300,text="HI")
    Rectangle(0,0,500,500,image=image("../SnowTexture.png"))
    w.start()

if __name__ == "__main__": main()
