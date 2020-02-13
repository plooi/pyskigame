from pylooiengine import *


class WorldObject(LooiObject):
    def __init__(self, *args):
        super().__init__(active=False)
        self.world = args["world"]
        
        #z and x are the non scaled coordinates of the world object. Quad z x is where this object is pinned
        self.z = args["z"]
        self.x = args["x"]
        if not self.world.valid_floor(self.z, self.x):
            raise Exception("Invalid z and x position " + str(self.x) + " " + str(self.z) + ". World dimensions are h%d w%d" % (self.world.get_height_floors(), self.world.get_width_floors()))
        self.world.quads[self.z][self.x].containedObjects.append(self)
        
        
        #active can be "always" "never" "line_of_sight" "texture_distance"
        if "active" in args:
            if args["active"] == "always":
                self.activate()
            else:
                args["active"] = "never"
                #"activate" it in other ways that's NOT by adding it as an active looi object
            
    