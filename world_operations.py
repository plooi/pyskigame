from tree import Tree


def fill_trees(world, z1, x1, z2, x2):
    for z in range(min([z1,z2]), max([z1,z2])):
        for x in range(min([x1,x2]), max([x1,x2])):
            Tree(z, x, world)
