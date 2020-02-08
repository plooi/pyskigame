import model_3d







def ski_model(
    ski_width = .1,
    ski_length = 2.1,
    ski_distance = .4,
    ski_color = [1,0,0]):
    return [  
    
    [-ski_length/2, 0,-ski_distance/2-ski_width/2], [ski_length/2, 0,-ski_distance/2-ski_width/2], [ski_length/2,0,-ski_distance/2+ski_width/2], [-ski_length/2, 0,-ski_distance/2+ski_width/2], ski_color,
    [-ski_length/2, 0,+ski_distance/2-ski_width/2], [ski_length/2, 0,+ski_distance/2-ski_width/2], [ski_length/2,0,+ski_distance/2+ski_width/2], [-ski_length/2, 0,+ski_distance/2+ski_width/2], ski_color,
    ]
    




def draw_skis(game_ui, model_func = ski_model):
    model = model_func()
    model_3d.horizontal_rotate_model_around_origin(model, game_ui.world.properties["ski_direction"])
    model_3d.move_model(model, game_ui.world.view.x, game_ui.world.view.y-game_ui.world.properties["player_height"]+.1, game_ui.world.view.z)
    model_3d.add_model_to_world_mobile(model, game_ui.world)
    
    
models = {
"Red Basic" : ski_model

}
