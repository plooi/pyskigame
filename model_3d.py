import copy
from math import *

def main():
    p = [1,0,1]
    horizontal_rotate_around_origin(p, pi/4)
    print(p)
def copy_model(model):
    return copy.deepcopy(model)
def horizontal_rotate_around_origin(point, theta):
    theta *= -1
    x = point[0]*cos(theta)- point[2]*sin(theta)
    z = point[0]*sin(theta)+ point[2]*cos(theta)
    point[0] = x
    point[2] = z
def horizontal_rotate_model_around_origin(model, theta):
    for i in range(0, len(model), 5):
        horizontal_rotate_around_origin(model[i], theta)
        horizontal_rotate_around_origin(model[i+1], theta)
        horizontal_rotate_around_origin(model[i+2], theta)
        horizontal_rotate_around_origin(model[i+3], theta)
def move_model(model, x_mov, y_mov, z_mov):
    for i in range(0, len(model), 5):
        model[i][0] += x_mov
        model[i][1] += y_mov
        model[i][2] += z_mov
        
        model[i+1][0] += x_mov
        model[i+1][1] += y_mov
        model[i+1][2] += z_mov
        
        model[i+2][0] += x_mov
        model[i+2][1] += y_mov
        model[i+2][2] += z_mov
        
        model[i+3][0] += x_mov
        model[i+3][1] += y_mov
        model[i+3][2] += z_mov
def add_model_to_vertex_handler(model, vertex_handler):
    keys = []
    for i in range(0, len(model), 5):
        
        keys.append( vertex_handler.add_vertex(model[i], model[i+4]) )
        vertex_handler.add_vertex(model[i+1], model[i+4])
        vertex_handler.add_vertex(model[i+2], model[i+4])
        vertex_handler.add_vertex(model[i+3], model[i+4])
    return keys
def rm_model_from_vertex_handler(keys, vertex_handler):
    for key in keys:
        vertex_handler.rm_vertex(key)
        vertex_handler.rm_vertex(key+1)
        vertex_handler.rm_vertex(key+2)
        vertex_handler.rm_vertex(key+3)
        
        
        
            
if __name__ == "__main__": main()
