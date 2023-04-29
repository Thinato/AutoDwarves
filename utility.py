from math import hypot

# get distance between two points
def dist(a, b):
    return hypot(a.pos.x - b.pos.x, a.pos.y - b.pos.y)