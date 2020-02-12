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
def horizontal_rotate_track_around_origin(track, theta):
    for i in range(0, len(track.points)):
        horizontal_rotate_around_origin(track.points[i], theta)
        
def horizontal_rotate_model_around_origin(model, theta, gradient_model=False):
    point_size = 8 if gradient_model else 5
    for i in range(0, len(model), point_size):
        horizontal_rotate_around_origin(model[i], theta)
        horizontal_rotate_around_origin(model[i+1], theta)
        horizontal_rotate_around_origin(model[i+2], theta)
        horizontal_rotate_around_origin(model[i+3], theta)
def move_point(point, x_mov, y_mov, z_mov):
    point[0] += x_mov
    point[1] += y_mov
    point[2] += z_mov
def move_track(track, x_mov, y_mov, z_mov):
    for i in range(0, len(track.points)):
        track.points[i][0] += x_mov
        track.points[i][1] += y_mov
        track.points[i][2] += z_mov
def move_model(model, x_mov, y_mov, z_mov, gradient_model=False):
    point_size = 8 if gradient_model else 5
    for i in range(0, len(model), point_size):
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
def add_model_to_world_fixed(model, world, anchor_z, anchor_x, object=None, gradient_model=False):
    keys = []
    if object != None:
        world.quads[anchor_z][anchor_x].containedObjects.append(object)
    if gradient_model:
        for i in range(0, len(model), 8):
            keys.append(
                world.add_fixed_quad(model[i], model[i+1], model[i+2], model[i+3], (model[i+4],model[i+5],model[i+6],model[i+7]), anchor_z, anchor_x, object=None)
                )
    else:
        for i in range(0, len(model), 5):
            keys.append(
                world.add_fixed_quad(model[i], model[i+1], model[i+2], model[i+3], model[i+4], anchor_z, anchor_x, object=None)
                )
        
    return keys
def rm_model_from_world_fixed(keys, world, anchor_z, anchor_x, object=None):
    if object != None:
        world.quads[anchor_z][anchor_x].containedObjects.remove(object)
    for key in keys:
        world.remove_fixed_quad(key, anchor_z, anchor_x, None)
        
def add_model_to_world_mobile(model, world):
    for i in range(0, len(model), 5):
        world.add_mobile_quad(model[i], model[i+1], model[i+2], model[i+3], model[i+4])
    
        
            
if __name__ == "__main__": main()
