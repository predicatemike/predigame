import random, math, os, sys
from types import ModuleType
from . import globs
from .Animation import Animation

def load_module(path, api):
    src = open(path).read()
    code = compile(src, os.path.basename(path), 'exec', dont_inherit = True)

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__dict__.update(api.__dict__)
    sys.modules[name] = mod

    return code, mod

def register_keydown(key, callback):
    if key in globs.keys_registered['keydown']:
        globs.keys_registered['keydown'][key].add(callback)
    else:
        globs.keys_registered['keydown'][key] = set([callback])

def animate(obj, duration = 1, callback = None, **kwargs):
    globs.animations.append(Animation(obj, duration, callback, **kwargs))

def rand_pos(x_padding = 0, y_padding = 0):
    grid_width = (globs.WIDTH / globs.GRID_SIZE) - math.ceil(x_padding)
    grid_height = (globs.HEIGHT / globs.GRID_SIZE) - math.ceil(y_padding)
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

def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start

def sign(num):
    return (1, -1)[num < 0]
