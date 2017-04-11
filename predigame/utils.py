import random, math
from . import globs

def register_keydown(key, callback):
    if key in globs.keys_registered['keydown']:
        globs.keys_registered['keydown'][key].add(callback)
    else:
        globs.keys_registered['keydown'][key] = set([callback])

def rand_pos():
    grid_width = globs.WIDTH / globs.GRID_SIZE
    grid_height = globs.HEIGHT / globs.GRID_SIZE
    x = 0
    y = 0
    while True:
        x = random.randrange(0, grid_width)
        y = random.randrange(0, grid_height)

        if len(globs.sprites) >= grid_width * grid_height:
            break

        for sprite in globs.sprites:
            if sprite.rect.x / globs.GRID_SIZE == x and sprite.rect.y / globs.GRID_SIZE == y:
                break
        else:
            break

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
