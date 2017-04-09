import random, math
from . import globs

def register_keydown(key, callback):
    if key in globs.keys_registered['keydown']:
        globs.keys_registered['keydown'][key].add(callback)
    else:
        globs.keys_registered['keydown'][key] = set([callback])

def rand_pos():
    x = random.randrange(0, globs.WIDTH / globs.GRID_SIZE)
    y = random.randrange(0, globs.HEIGHT / globs.GRID_SIZE)
    return x, y

def rand_color():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    if (r, g, b) == globs.background_color:
        r, g, b = rand_color()
    return r, g, b

def roundup(num, step):
    return int(math.ceil(num / float(step))) * step
