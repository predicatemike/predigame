import random, math, os, sys
from types import ModuleType
from .Globals import Globals
from .Animation import Animation
from .constants import *

def load_module(path, api):
    src = open(path).read()
    code = compile(src, os.path.basename(path), 'exec', dont_inherit = True)

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__dict__.update(api.__dict__)
    sys.modules[name] = mod

    return code, mod

def register_cell(pos, s):
    """ helper function that builds the index of all sprites in a given cell """
    lst = []
    if pos in Globals.instance.cells:
        lst = Globals.instance.cells[pos]
    else:
        Globals.instance.cells[pos] = lst
    lst.append(s)

def register_keydown(key, callback):
    if key in Globals.instance.keys_registered['keydown']:
        Globals.instance.keys_registered['keydown'][key].add(callback)
    else:
        Globals.instance.keys_registered['keydown'][key] = set([callback])

def register_keyup(key, callback):
    if key in Globals.instance.keys_registered['keyup']:
        Globals.instance.keys_registered['keyup'][key].add(callback)
    else:
        Globals.instance.keys_registered['keyup'][key] = set([callback])

def animate(obj, duration = 1, callback = None, abortable=False, **kwargs):
    Globals.instance.animations.append(Animation(obj, duration, callback, abortable, **kwargs))

def at(pos):
    if pos in Globals.instance.cells:
        lst = Globals.instance.cells[pos]
        if len(lst) == 0:
            return None
        elif len(lst) == 1:
            return lst[0]
        else:
            return lst

def get(name):
    if name in Globals.instance.tags:
        return Globals.instance.tags[name]
    else:
        return []

def rand_pos(x_padding = 0, y_padding = 0, empty=False):
    grid_width = (Globals.instance.WIDTH / Globals.instance.GRID_SIZE) - math.ceil(x_padding)
    grid_height = (Globals.instance.HEIGHT / Globals.instance.GRID_SIZE) - math.ceil(y_padding)
    x = 0
    y = 0
    while True:
        x = random.randrange(0, grid_width)
        y = random.randrange(0, grid_height)

        if len(Globals.instance.sprites) >= grid_width * grid_height:
            break

        if at((x, y)) is None:
            break

    return x, y

def rand_maze(callback):
    from daedalus import Maze
    maze = Maze((Globals.instance.WIDTH/Globals.instance.GRID_SIZE), (Globals.instance.HEIGHT/Globals.instance.GRID_SIZE))
    maze.create_perfect()
    for x in range(int(Globals.instance.WIDTH/Globals.instance.GRID_SIZE)):
        for y in range(int(Globals.instance.HEIGHT/Globals.instance.GRID_SIZE)):
            if maze[x,y] == True:
                s = callback(pos=(x,y), tag='wall')
                register_cell((x,y), s)

def rand_color():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    #if (r, g, b) == globs.BACKGROUND:
    #    r, g, b = rand_color()
    return r, g, b

def rand_arc():
    p1 = rand_pos(1,4)
    p2 = rand_pos(1,4)
    mid_x = (p1[0] + p2[0]) / 2
    return (p1[0], (Globals.instance.HEIGHT/Globals.instance.GRID_SIZE)+1), (int(mid_x), 1), (p2[0], (Globals.instance.HEIGHT/Globals.instance.GRID_SIZE)+1)

def roundup(num, step):
    return int(math.ceil(num / float(step))) * step

def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start

def sign(num):
    return (1, -1)[num < 0]

def distance(p1, p2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(p1, p2)]))

def visible(p1):
    if p1[0] >= 0 and p1[1] >= 0 and p1[0] < (Globals.instance.WIDTH/Globals.instance.GRID_SIZE) and p1[1] < (Globals.instance.HEIGHT/Globals.instance.GRID_SIZE):
        return True
    else:
        return False

def score_pos(pos = UPPER_LEFT):
    """ return the grid position of the score sprite """
    return {
        UPPER_LEFT : (0.5, 0.5),
        UPPER_RIGHT: ((Globals.instance.WIDTH/Globals.instance.GRID_SIZE) - 0.5, 0.5),
        LOWER_LEFT:  (0.5, (Globals.instance.HEIGHT/Globals.instance.GRID_SIZE) - 1),
        LOWER_RIGHT: ((Globals.instance.WIDTH/Globals.instance.GRID_SIZE) - 0.5, (Globals.instance.HEIGHT/Globals.instance.GRID_SIZE) - 1)
    }.get(pos, UPPER_LEFT)

def sprites():
    """ return a list of all loaded sprites """
    return Globals.instance.sprites

def graze(sprite) :
    """ a sprite.wander() operation. randomly move around """
    x, y = sprite.pos
    choices    = [(x,y), (x, y-1), (x, y+1), (x+1, y), (x-1, y)]
    random.shuffle(choices)
    obstacles  = [at(p) for p in choices]
    visibility = [visible(p) for p in choices]

    for i in range(len(choices)):
        if obstacles[i] is None and visibility[i]:
            if choices[i] != (x, y):
                sprite.move((choices[i][0] - x, choices[i][1] - y))
                break

def track(sprite, player_sprite, pbad = 0.1) :
    """
        a sprite.wander() operation. attempt to a path that moves sprite closer to player_sprite.

        :param sprite: the sprite to automate movements.

        :param player_sprite: the player sprite to track.

        :param pbad: the probability to make a bad move. some number of bad moves are needed to

    """

    x, y = sprite.pos

    choices    = [(x, y), (x, y-1), (x, y+1), (x+1, y), (x-1, y)]
    distances  = [distance(p, player_sprite.pos) for p in choices]
    obstacles  = [at(p) for p in choices]
    visibility = [visible(p) for p in choices]

    best = None
    min_dist = 999999
    for i in range(len(choices)):
        if obstacles[i] is None and visibility[i]:
            #every now and then make a random "bad" move
            rnd = random.uniform(0, 1)
            if rnd <= pbad:
                best = choices[i]
                break
            elif distances[i] < min_dist:
                best = choices[i]
                min_dist = distances[i]
    if best is not None and best != (x,y):
        sprite.move((best[0] - x, best[1] - y))


def fill(obj, collide_obj = None, collide_callback = None) :
    """
        fills all white space with an object. object can be set to collide with something (collide_obj) in which case a callback would be invoked (collide_callback).

        :param obj: a callback (or partial) to a sprite to create in whitespace.

        :param collide_obj: an object or (list of objects) to check for collisions

        :param collide_callback: a callback function to invoke when collide_obj collides with obj.

    """
    for x in range(int(Globals.instance.WIDTH/Globals.instance.GRID_SIZE)):
        for y in range(int(Globals.instance.HEIGHT/Globals.instance.GRID_SIZE)):
            if at((x,y)) is None:
                o = obj(pos=(x,y))
                if collide_obj and collide_callback:
                    if isinstance(collide_obj, (list, tuple)):
                        for obj in collide_obj:
                            o.collides(obj, collide_callback)
                    else:
                        o.collides(collide_obj, collide_callback)
