import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from threading import Thread
from time import sleep
from random import random
from time import time
from PIL import Image
import numpy
from OpenGL.arrays import vbo
import array
import traceback
main_window = None
import math


def default_3d_view_setup():
    gluPerspective(45, (main_window.window_size[0]/main_window.window_size[1]), 0.1, 5000.0)



class Color:
     def __init__(self, r, g, b, a=1):
         self.a = a
         self.r = r
         self.g = g
         self.b = b
     def to_tuple(self, form="RGB"):
         if form == "RGB":
             return (self.r, self.g, self.b)
         elif form == "ARGB":
             return (self.a, self.r, self.g, self.b)
         elif form == "RGBA":
             return (self.r, self.g, self.b, self.a)
         else:
             fail("%s is not a valid form for a color" % (form,))
     def to_tuple_255(self, form="RGB"):
         r = int(self.r * 255)
         g = int(self.g * 255)
         b = int(self.b * 255)
         if form == "RGB":
             return (r, g, b)
         elif form == "ARGB":
             return (a, r, g, b)
         elif form == "RGBA":
             return (r, g, b, a)
         else:
             fail("%s is not a valid form for a color" % (form,))
     def lighter(self, brightness_increase):
         return Color(reg(self.r + brightness_increase), reg(self.g + brightness_increase), reg(self.b + brightness_increase))
     def darker(self, brightness_decrease):
         return Color(reg(self.r - brightness_decrease), reg(self.g - brightness_decrease), reg(self.b - brightness_decrease))
     def copy(self):
         return Color(self.r,self.g,self.b,self.a)

def reg(x):
    if x > 1:
        return 1
    elif x < 0:
        return 0
    else:
        return x

white = Color(1,1,1)
black = Color(0,0,0)
red = Color(1,0,0)
green = Color(0,.85,0)
blue = Color(0,0,1)
light_brown = Color(.8,.5,.33)
dark_brown = Color(.5, .27, .1)
yellow = Color(1,1,0)
purple = Color(.6,0,.81)
orange = Color(1,.6,0)
light_blue = Color(.45,.8, .95)
light_gray = Color(.8,.8,.8)
dark_gray = Color(.4,.4,.4)
peach = Color(1, .85, .7)
pink = Color(1,.75,.8)
magenta = Color(1,0,1)



def main():
    pass

class Window():
    def __init__(self, window_width=1000, window_height=600, internal_size=(1920,1080), fps=30):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.window_size = (window_width, window_height)
        self.internal_size = internal_size
        self.view_origin_x_in_window = None
        self.view_origin_y_in_window = None
        self.view_width = None
        self.view_height = None
        
        self.mipmap_max_level = 3
        
        self.fps = fps
        self.seconds_per_frame = 1/self.fps
        
        self.display = pygame.display.set_mode(self.window_size, DOUBLEBUF|OPENGL|pygame.RESIZABLE)
        self.unlayered_looi_objects = []
        self.layered_looi_objects = []
        self.transfer_to_unlayered_looi_objects = []
        self.transfer_to_layered_looi_objects = []
        self.to_remove = []
        
        
        global main_window
        main_window = self
        
        self.mouse = {
            "down" : [False, False, False],
            "pressed" : [False, False, False],
            "released" : [False, False, False]
        }
        self.keys = {
            "down" : [False]*len(pygame.key.get_pressed()),
            "pressed" : [False]*len(pygame.key.get_pressed()),
            "released" : [False]*len(pygame.key.get_pressed()),
        }
        self.update_view_dimensions()
        
        
        self.sounds = {}
        
        pygame.mixer.init()
    
    def start(self):
        keysdown = [False]*len(pygame.key.get_pressed())
        
        while True:
            start_time = time()
            self.scroll_up = False
            self.scroll_down = False
            for event in pygame.event.get():
                #if event.type == pygame.QUIT:
                #    pygame.quit()
                #    quit()
                if event.type == pygame.VIDEORESIZE:
                    self.window_size = (event.w, event.h)
                    surface = pygame.display.set_mode(self.window_size, DOUBLEBUF|OPENGL|pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    keysdown[event.key] = True
                if event.type == pygame.KEYUP:
                    keysdown[event.key] = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scroll_up = True
                    elif event.button == 5:
                        self.scroll_down = True
                    
                    
            #mouse
            mouse_buttons_pressing = pygame.mouse.get_pressed()
            for i in range(3):
                if mouse_buttons_pressing[i] == True:# is it pressing now?
                    if self.mouse["down"][i] == True:#was it down before?
                        self.mouse["pressed"][i] = False
                        self.mouse["down"][i] = True
                        self.mouse["released"][i] = False
                    else:
                        #it was not down before
                        self.mouse["pressed"][i] = True
                        self.mouse["down"][i] = True
                        self.mouse["released"][i] = False
                else:
                    #it is not down now
                    if self.mouse["down"][i] == True:#was it down before?
                        self.mouse["pressed"][i] = False
                        self.mouse["down"][i] = False
                        self.mouse["released"][i] = True
                    else:
                        #it was not down before
                        self.mouse["pressed"][i] = False
                        self.mouse["down"][i] = False
                        self.mouse["released"][i] = False
                    
                
            #keys
            keys = keysdown
            
            for i in range(len(keys)):
                if keys[i] == True:# is it down now?
                    if self.keys["down"][i] == True:#was it down before?
                        self.keys["pressed"][i] = False
                        self.keys["down"][i] = True
                        self.keys["released"][i] = False
                    else:
                        #it was not down before
                        self.keys["pressed"][i] = True
                        self.keys["down"][i] = True
                        self.keys["released"][i] = False
                else:
                    #it is not down now
                    if self.keys["down"][i] == True:#was it down before?
                        self.keys["pressed"][i] = False
                        self.keys["down"][i] = False
                        self.keys["released"][i] = True
                    else:
                        #it was not down before
                        self.keys["pressed"][i] = False
                        self.keys["down"][i] = False
                        self.keys["released"][i] = False
            
            
            #drawing and stepping
            glClearColor(1,1,1,1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glDepthFunc(GL_LESS)
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_MODELVIEW)
            
            
            glAlphaFunc(GL_GREATER, 0.1);
            glEnable(GL_ALPHA_TEST);
            glBlendEquation(GL_FUNC_ADD)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND);
            
            self.draw_borders()
            
            self.layered_looi_objects.sort(key = lambda looi_object: looi_object.get_layer())
            for looi_object in self.layered_looi_objects: looi_object.step()
            for looi_object in self.unlayered_looi_objects: looi_object.step()
            for looi_object in self.layered_looi_objects: looi_object.paint()
            for looi_object in self.unlayered_looi_objects: looi_object.paint()
            
            
            
            
            
            strict_remove_all(self.transfer_to_unlayered_looi_objects, self.layered_looi_objects)
            strict_remove_all(self.transfer_to_layered_looi_objects, self.unlayered_looi_objects)
            self.layered_looi_objects += self.transfer_to_layered_looi_objects
            self.unlayered_looi_objects += self.transfer_to_unlayered_looi_objects
            self.transfer_to_layered_looi_objects.clear()
            self.transfer_to_unlayered_looi_objects.clear()
            
            strict_remove_all(self.to_remove, self.layered_looi_objects)
            strict_remove_all(self.to_remove, self.unlayered_looi_objects)
            self.to_remove.clear()
            
            pygame.display.flip()
            while time() - start_time < self.seconds_per_frame:
                sleep(.000000001)
            
        return self
        
        
    def get_num_active_looi_objects(self):
        return len(self.layered_looi_objects) + len(self.unlayered_looi_objects)
    def get_layered_looi_objects(self):
        return self.layered_looi_objects
    def get_unlayered_looi_objects(self):
        return self.unlayered_looi_objects
    def layer_switch(self, looi_object):
        
        if strict_in(looi_object, self.unlayered_looi_objects) and is_num(looi_object.get_layer()):
            self.transfer_to_layered_looi_objects.append(looi_object)
        elif strict_in(looi_object, self.layered_looi_objects) and (looi_object.get_layer()==None):
            self.transfer_to_unlayered_looi_objects.append(looi_object)
        elif strict_in(looi_object, self.transfer_to_unlayered_looi_objects) and is_num(looi_object.get_layer()):
            self.transfer_to_layered_looi_objects.append(looi_object)
            strict_remove(looi_object, self.transfer_to_unlayered_looi_objects)
        elif strict_in(looi_object, self.transfer_to_layered_looi_objects) and (looi_object.get_layer()==None):
            self.transfer_to_unlayered_looi_objects.append(looi_object)
            strict_remove(looi_object, self.transfer_to_layered_looi_objects)
    def remove_looi_object(self, looi_object):
        if strict_in(looi_object, self.transfer_to_unlayered_looi_objects):
            strict_remove(looi_object, self.transfer_to_unlayered_looi_objects)
            self.to_remove.append(looi_object)
            return
        if strict_in(looi_object, self.transfer_to_layered_looi_objects):
            strict_remove(looi_object, self.transfer_to_layered_looi_objects)
            self.to_remove.append(looi_object)
            return
        if (strict_in(looi_object, self.to_remove) 
            or 
            (not strict_in(looi_object, self.layered_looi_objects) and not strict_in(looi_object, self.unlayered_looi_objects))  ):
            fail("Cannot remove this looi object as it is not currently active")
        
        
        self.to_remove.append(looi_object)
    def add_looi_object(self, looi_object):
        if is_num(looi_object.get_layer()):
            if (strict_in(looi_object, self.transfer_to_layered_looi_objects) 
                or 
                strict_in(looi_object, self.layered_looi_objects)):
                fail("Cannot add this looi object as it has already been added")
            self.transfer_to_layered_looi_objects.append(looi_object)
        elif looi_object.get_layer() == None:
            if (strict_in(looi_object, self.transfer_to_unlayered_looi_objects) 
                or 
                strict_in(looi_object, self.unlayered_looi_objects)):
                fail("Cannot add this looi object as it has already been added")
            self.transfer_to_unlayered_looi_objects.append(looi_object)
        else:
            fail("Invalid layer type " + str(type(looi_object.get_layer())))
        if strict_in(looi_object, self.to_remove):
            strict_remove(looi_object, self.to_remove)
    
    
    def set_fps(self, fps):
        self.fps = fps
        self.seconds_per_frame = 1/self.fps
    def get_window_size(self): return self.window_size
    def set_window_size(self, size): 
        self.window_size = size
        surface = pygame.display.set_mode(self.window_size, DOUBLEBUF|OPENGL|pygame.RESIZABLE)
    def get_internal_size(self): return self.internal_size
    def set_internal_size(self, size): self.internal_size = size
    def get_view_size(self): return self.view_width, self.view_height
    
    def update_view_dimensions(self):
        #larger number means wider window, number close to 0 means taller window
        internal_ratio = self.get_internal_size()[0]/self.get_internal_size()[1]
        window_ratio = self.get_window_size()[0]/self.get_window_size()[1]
        if internal_ratio == window_ratio:
            #internal dimensions are perfect, we just need to scale it
            self.view_origin_x_in_window = 0
            self.view_origin_y_in_window = 0
            self.view_width = self.window_size[0]
            self.view_height = self.window_size[1]
        elif internal_ratio > window_ratio:
            #internal dimensions are wider and window is taller
            self.view_width = self.window_size[0]
            self.view_height = self.internal_size[1] * self.view_width/self.internal_size[0]
            self.view_origin_x_in_window = 0
            self.view_origin_y_in_window = (self.window_size[1] - self.view_height)/2
        elif internal_ratio < window_ratio:
            #internal dimensions are taller and window is wider
            self.view_height = self.window_size[1]
            self.view_width = self.internal_size[0] * self.view_height/self.internal_size[1]
            self.view_origin_y_in_window = 0
            self.view_origin_x_in_window = (self.window_size[0] - self.view_width)/2
    
    def draw_borders(self):
        #larger number means wider window, number close to 0 means taller window
        internal_ratio = self.get_internal_size()[0]/self.get_internal_size()[1]
        window_ratio = self.get_window_size()[0]/self.get_window_size()[1]
        if internal_ratio == window_ratio:
            #internal dimensions are perfect, we just need to scale it
            self.view_origin_x_in_window = 0
            self.view_origin_y_in_window = 0
            self.view_width = self.window_size[0]
            self.view_height = self.window_size[1]
        elif internal_ratio > window_ratio:
            #internal dimensions are wider and window is taller
            self.view_width = self.window_size[0]
            self.view_height = self.internal_size[1] * self.view_width/self.internal_size[0]
            self.view_origin_x_in_window = 0
            self.view_origin_y_in_window = (self.window_size[1] - self.view_height)/2
            self.draw_rect(0, 0, self.window_size[0], self.view_origin_y_in_window, black)
            self.draw_rect(0, self.view_origin_y_in_window + self.view_height, self.window_size[0], self.window_size[1], black)
        elif internal_ratio < window_ratio:
            #internal dimensions are taller and window is wider
            self.view_height = self.window_size[1]
            self.view_width = self.internal_size[0] * self.view_height/self.internal_size[1]
            self.view_origin_y_in_window = 0
            self.view_origin_x_in_window = (self.window_size[0] - self.view_width)/2
            self.draw_rect(0, 0, self.view_origin_x_in_window, self.window_size[1], black)
            self.draw_rect(self.view_origin_x_in_window + self.view_width, 0, self.window_size[0], self.window_size[1], black)
    def window_x_to_opengl_coord(self, x):
        return x/self.window_size[0] * 2 - 1
    def window_y_to_opengl_coord(self, y):
        return - (y/self.window_size[1] * 2 - 1)
    def internal_x_to_window_x(self, x):
        return x/self.internal_size[0] * self.view_width + self.view_origin_x_in_window
    def internal_y_to_window_y(self, y):
        return y/self.internal_size[1] * self.view_height + self.view_origin_y_in_window
    def convert_internal_x(self, x):
        return self.window_x_to_opengl_coord(self.internal_x_to_window_x(x))
    def convert_internal_y(self, y):
        return self.window_y_to_opengl_coord(self.internal_y_to_window_y(y))
    def internal_length_to_window_length(self, l):
        return l/self.internal_size[0]  * self.view_width
    def window_length_to_opengl_length(self, l):
        return l/self.window_size[0] * 2 - 1
    def convert_internal_length(self, l):
        return self.window_length_to_opengl_length(self.internal_length_to_window_length(l))
        
    def window_x_to_internal_x(self, x):
        return (x - self.view_origin_x_in_window)/self.view_width * self.internal_size[0]
    def window_y_to_internal_y(self, y):
        return (y - self.view_origin_y_in_window)/self.view_height * self.internal_size[1]
    
    def draw_rect(self, x1, y1, x2, y2, color):
        color = color.to_tuple()
        x1 = self.window_x_to_opengl_coord(x1)
        y1 = self.window_y_to_opengl_coord(y1)
        x2 = self.window_x_to_opengl_coord(x2)
        y2 = self.window_y_to_opengl_coord(y2)
        glPushMatrix()
        glBegin(GL_QUADS)
        glColor3fv(color)
        glVertex2f(x1,y1)
        glVertex2f(x2,y1)
        glVertex2f(x2,y2)
        glVertex2f(x1,y2)
        glEnd()
        glPopMatrix()
    def play_sound(self, sound, volume, fade_ms, maxtime):
        s = sound
        s.set_volume(volume)
        s.play(fade_ms=fade_ms, maxtime=maxtime)
        return s
    def new_sound(self, filename, volume):
        s = pygame.mixer.Sound(filename)
        s.set_volume(volume)
        return s
        


    
    
class LooiObject:
    def __init__(self, layer=None, active=True):
    
        if main_window == None: fail("Tried to create LooiObject, but no Window object exists for the LooiObject to reside in.")
        ####else: self.my_window = main_window
        
        self.contained_looi_objects = []
        self.layer = layer
        self.active = active
        
        if self.active:
            ####self.my_window.add_looi_object(self)
            main_window.add_looi_object(self)
        self.xx = 0
        
    def step(self): pass
    def paint(self): pass
    def upon_activation(self): pass
    def upon_deactivation(self): pass
    def add(self, contained_looi_object):
        self.contained_looi_objects.append(contained_looi_object)
    def remove(self, contained_looi_object):
        while strict_in(contained_looi_object, self.contained_looi_objects):
            strict_remove(contained_looi_object, self.contained_looi_objects)
    def activate(self):
        if not self.active:
            try:
                self.get_my_window().add_looi_object(self)
            except Exception as e:
                raise(e)
            self.active = True
            for contained_looi_object in self.contained_looi_objects:
                contained_looi_object.activate()
            self.upon_activation()
        
    def deactivate(self):
        if self.active:
            self.active = False
            try:
                self.get_my_window().remove_looi_object(self)
            except Exception as e:
                raise (e)
            for contained_looi_object in self.contained_looi_objects:
                contained_looi_object.deactivate()
            self.upon_deactivation()
    def is_active(self):
        return self.active
    def get_my_window(self):
        return main_window
    def get_mouse_pos(self):
        x,y = pygame.mouse.get_pos()
        x = self.get_my_window().window_x_to_internal_x(x)
        y = self.get_my_window().window_y_to_internal_y(y)
        return x,y
    def mouse(self, button, action="down"):
        button = {
            "left" : 0,
            "middle" : 1,
            "right" : 2,
            0 : 0,
            1 : 1,
            2 : 2
        }[button]
        return self.get_my_window().mouse[action][button]
    def key(self, key, action="down"):
        if type(key) == type(1):
            pass#it's a key code
        elif type(key) == type(""):
            if len(key) == 1 and key.isalpha():
                key = getattr(pygame, "K_"+key.lower())
            else:
                key = getattr(pygame, "K_"+key.upper())
        else:
            fail("incorrect type for 'key' argument. Must be string or int key code")
        return self.get_my_window().keys[action][key]
    def set_layer(self, layer):
        check(layer == None or is_num(layer))
        
        old_layer = self.layer
        self.layer = layer
        
        self.get_my_window().layer_switch(self)
    def get_layer(self):
        return self.layer
    
    def draw_line(self, x1, y1, x2, y2, color, line_width = 3):
        color = color.to_tuple()
        x1 = self.get_my_window().convert_internal_x(x1)
        y1 = self.get_my_window().convert_internal_y(y1)
        x2 = self.get_my_window().convert_internal_x(x2)
        y2 = self.get_my_window().convert_internal_y(y2)
        line_width = self.get_my_window().internal_length_to_window_length(line_width)
        
        glPushMatrix()
        
        glLineWidth((line_width))
        glBegin(GL_LINES)
        glColor3fv(color)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glEnd()
        
        glPopMatrix()
    def draw_rect(self, x1, y1, x2, y2, color, filled=True, line_width = 3):
        color = color.to_tuple()
        x1 = self.get_my_window().convert_internal_x(x1)
        y1 = self.get_my_window().convert_internal_y(y1)
        x2 = self.get_my_window().convert_internal_x(x2)
        y2 = self.get_my_window().convert_internal_y(y2)
        line_width = self.get_my_window().internal_length_to_window_length(line_width)
        glPushMatrix()
        if filled:
            glBegin(GL_QUADS)
        else:
            glLineWidth((line_width))
            glBegin(GL_LINE_LOOP)
        glColor3fv(color)
        glVertex2f(x1,y1)
        glVertex2f(x2,y1)
        glVertex2f(x2,y2)
        glVertex2f(x1,y2)
        glEnd()
        glPopMatrix()
    def draw_quad(self, x1, y1, x2, y2, x3, y3, x4, y4, color, filled=True, line_width = 3):
        color = color.to_tuple()
        x1 = self.get_my_window().convert_internal_x(x1)
        y1 = self.get_my_window().convert_internal_y(y1)
        x2 = self.get_my_window().convert_internal_x(x2)
        y2 = self.get_my_window().convert_internal_y(y2)
        x3 = self.get_my_window().convert_internal_x(x3)
        y3 = self.get_my_window().convert_internal_y(y3)
        x4 = self.get_my_window().convert_internal_x(x4)
        y4 = self.get_my_window().convert_internal_y(y4)
        line_width = self.get_my_window().internal_length_to_window_length(line_width)
        glPushMatrix()
        if filled:
            glBegin(GL_QUADS)
        else:
            glLineWidth((line_width))
            glBegin(GL_LINE_LOOP)
        glColor3fv(color)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glVertex2f(x3,y3)
        glVertex2f(x4,y4)
        glEnd()
        glPopMatrix()
    def draw_circle(self, x1, y1, x2, y2, color, filled=True, line_width = 3, precision=100):
        color = color.to_tuple()
        x1 = self.get_my_window().convert_internal_x(x1)
        y1 = self.get_my_window().convert_internal_y(y1)
        x2 = self.get_my_window().convert_internal_x(x2)
        y2 = self.get_my_window().convert_internal_y(y2)
        line_width = self.get_my_window().internal_length_to_window_length(line_width)
        
        height_radius = abs(y1-y2)/2
        width_radius = abs(x1-x2)/2
        center_x = (x1+x2)/2
        center_y = (y1+y2)/2
        
        glPushMatrix()
        if filled:
            glBegin(GL_POLYGON)
        else:
            glLineWidth((line_width))
            glBegin(GL_LINE_LOOP)
            
        glColor3fv(color)
        
        for i in range(precision+1):
            angle = 2 * math.pi * i / precision
            x = center_x + math.cos(angle) * width_radius
            y = center_y + math.sin(angle) * height_radius
            glVertex2d(x,y)
        
        glEnd()
        glPopMatrix()
    def draw_image(self, x1, y1, x2, y2, image):
        x1 = self.get_my_window().convert_internal_x(x1)
        y1 = self.get_my_window().convert_internal_y(y1)
        x2 = self.get_my_window().convert_internal_x(x2)
        y2 = self.get_my_window().convert_internal_y(y2)
        
        glPushMatrix()
        
        if type(image) == type(()):
            ix, iy, image = image
        else:
            ix, iy, image = image.size[0], image.size[1], image.tobytes("raw", "RGBA", 0, -1)
        ID = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        
        
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        
        
        glEnable(GL_TEXTURE_2D)
        
        
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        
        #gluPerspective(45, (self.get_my_window().window_size[0]/self.get_my_window().window_size[1]), 0.1, 50.0)
        
        glBegin(GL_QUADS)
        """
        glTexCoord2f(0.0, 0.0)
        glVertex2fv((x1,y1))
        glTexCoord2f(1.0, 0.0)
        glVertex2fv((x2,y1))
        glTexCoord2f(1.0, 1.0)
        glVertex2fv((x2,y2))
        glTexCoord2f(0.0, 1.0)
        glVertex2fv((x1,y2))
        """
        glTexCoord2f(0.0, 1.0)
        glVertex2fv((x1,y1))
        glTexCoord2f(1.0, 1.0)
        glVertex2fv((x2,y1))
        glTexCoord2f(1.0, 0.0)
        glVertex2fv((x2,y2))
        glTexCoord2f(0.0, 0.0)
        glVertex2fv((x1,y2))
        glEnd()
        
        glDeleteTextures([ID])
        #http://pyopengl.sourceforge.net/context/tutorials/nehe6.html
        
        
        glPopMatrix()
    def draw_text(self, x, y, textString, font_size=64, color=black, background_color=white, font = "Microsoft Sans Serif"):
        color = color.to_tuple_255()
        background_color = background_color.to_tuple_255()
        x = self.get_my_window().convert_internal_x(x)
        y = self.get_my_window().convert_internal_y(y)
        font_size = int(self.get_my_window().internal_length_to_window_length(font_size))
        glPushMatrix()
        font = pygame.font.SysFont(font, font_size)
        textSurface = font.render(textString, True, color, background_color)     
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glRasterPos3d(x, y, 0)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
        glPopMatrix()
    def draw_line_3d(self, x1, y1, z1, x2, y2, z2, color, line_width = 3, setup_3d=default_3d_view_setup):
        #line_width = self.get_my_window().internal_length_to_window_length(line_width)
        color = color.to_tuple()
        glPushMatrix()
        
        setup_3d()
        
        glLineWidth((line_width))
        glBegin(GL_LINES)
        glColor3fv(color)
        glVertex3f(x1,y1,z1)
        glVertex3f(x2,y2,z2)
        glEnd()
        
        glPopMatrix()
    def draw_image_3d(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, image, setup_3d=default_3d_view_setup):
        glPushMatrix()
        
        if type(image) == type(()):
            ix, iy, image = image
        else:
            ix, iy, image = image.size[0], image.size[1], image.tobytes("raw", "RGBA", 0, -1)
        ID = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        
        
        glTexImage2D(
            GL_TEXTURE_2D, 0, 4, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        
        
        glEnable(GL_TEXTURE_2D)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)#USED TO BE GL_NEAREST
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)#USED TO BE GL_NEAREST
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, self.get_my_window().mipmap_max_level)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3fv((x1,y1,z1))
        glTexCoord2f(1.0, 0.0)
        glVertex3fv((x2,y2,z2))
        glTexCoord2f(1.0, 1.0)
        glVertex3fv((x3,y3,z3))
        glTexCoord2f(0.0, 1.0)
        glVertex3fv((x4,y4,z4))
        
        glEnd()
        
        glDeleteTextures([ID])
        #http://pyopengl.sourceforge.net/context/tutorials/nehe6.html
        
        
        glPopMatrix()
    def draw_quad_3d(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, color, setup_3d=default_3d_view_setup):
        color = color.to_tuple()
        glPushMatrix()
        glColor3fv(color)
        setup_3d()
        #glTranslatef(0.0,.5, -x/50)
        #glRotatef(0, 1, -2, 0)
        glBegin(GL_QUADS)
        glVertex3fv((x1,y1,z1))
        glVertex3fv((x2,y2,z2))
        glVertex3fv((x3,y3,z3))
        glVertex3fv((x4,y4,z4))
        glEnd()
        glPopMatrix()
    def draw_quad_array_3d(self, vertices, colors, setup_3d=default_3d_view_setup):
        glPushMatrix()
        setup_3d()
        
        
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_COLOR_ARRAY);
        
        
        
        glVertexPointerf(vertices);
        glColorPointerf(colors)
        glDrawArrays(GL_QUADS, 0, len(vertices));
        
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_COLOR_ARRAY);
        
        glPopMatrix()
    def draw_image_array_3d(self, vertices, texutre_coords, image, bytes, setup_3d=default_3d_view_setup):
        glPushMatrix()
        
        ix, iy = image.size[0], image.size[1]
        
        image = bytes
        
        ID = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        
        glTexImage2D(
            GL_TEXTURE_2D, 0, 4, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        
        
        
        glEnable(GL_TEXTURE_2D)
        
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)#USED TO BE GL_NEAREST
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)#USED TO BE GL_NEAREST
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, self.get_my_window().mipmap_max_level)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        glBindTexture(GL_TEXTURE_2D, ID)
        
        glGenerateMipmap(GL_TEXTURE_2D)
        
        setup_3d()
        
        
        
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_TEXTURE_COORD_ARRAY);
        
        glVertexPointerf(vertices);
        glTexCoordPointerf(texutre_coords);
        glDrawArrays(GL_QUADS, 0, len(vertices));
        
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_TEXTURE_COORD_ARRAY);
        
        glDeleteTextures([ID])
        
        glPopMatrix()
    
    def draw_quad_array_2d(self, vertices, colors, setup = lambda:0):
        glPushMatrix()
        setup()
        
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_COLOR_ARRAY);
        
        
        
        glVertexPointerf(vertices);
        glColorPointerf(colors)
        
        glScale(2/self.get_my_window().internal_size[0]*self.get_my_window().view_width/self.get_my_window().window_size[0], 
        -2/self.get_my_window().internal_size[1]*self.get_my_window().view_height/self.get_my_window().window_size[1],0 )
        
        
        glTranslatef(-self.get_my_window().internal_size[0]/2,-self.get_my_window().internal_size[1]/2,0)
        
        glDrawArrays(GL_QUADS, 0, len(vertices));
        
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_COLOR_ARRAY);
        
        glPopMatrix()
        """
        def window_x_to_opengl_coord(self, x):
            return x/self.window_size[0] * 2 - 1
        def window_y_to_opengl_coord(self, y):
            return - (y/self.window_size[1] * 2 - 1)
        def internal_x_to_window_x(self, x):
            return x/self.internal_size[0] * self.view_width + self.view_origin_x_in_window
        def internal_y_to_window_y(self, y):
            return y/self.internal_size[1] * self.view_height + self.view_origin_y_in_window
        """
    def events(self):
        return pygame.event.get()
    
    def play_sound(self, sound, volume=.5, fade_ms=0, maxtime=9999999):
        return self.get_my_window().play_sound(sound, volume, fade_ms, maxtime)
    def new_sound(self, filename, volume=.5):
        return self.get_my_window().new_sound(filename,volume)
    
        
            






class CheckException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
def check(bool, msg="Check failed"):
    if type(msg) != type(""):
        raise CheckException("parameter 'msg' to function 'check' should have been a string")
    if bool:
        pass #good
    else:
        raise CheckException(msg)
def fail(msg):
    raise Exception(msg)
def is_num(object): 
    return type(object) == type(1) or type(object) == type(1.0)
def strict_in(item, list_):
    for x in list_:
        if x is item:
            return True
    return False
def strict_remove(item, list_):
    for i in range(len(list_)):
        if list_[i] is item:
            del list_[i]
            return
    raise Exception("Item " + str(item) + " is not in the list. Cannot remove anything")
def strict_remove_all(items, list_):
    i = 0
    while i < len(list_):
        for item in items:
            if item is list_[i]:
                del list_[i]
                i -= 1
                break
        i += 1
def abs(x):
    return x if x >= 0 else -x

def image(file_name):
    i = Image.open(file_name)
    pixels = i.load()
    #print(type(pixels[0][0]))
    if len(pixels[0,0]) == 3:
        i.putalpha(255)
    return i












if __name__ == "__main__": main()
