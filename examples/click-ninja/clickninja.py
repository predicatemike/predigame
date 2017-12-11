import math
from predigame.constants import * 

WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'
BACKGROUND = 'board'

def explode(s):
    text('You Survived %s seconds' % time(), MAROON)
    pause()

def hurt(s):
    s.destroy()
    score(-20)
    if score() < 0:
        text('You Survived %s' % time(), MAROON)
        pause()

def point(s):
    image('redsplat', s.pos, 2)
    s.destroy()
    score(5)

def spawn():
    target = choice(['bomb', 'bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])
    arc = rand_arc()
    if target == 'bomb':
        s = image(target, arc[0], 2)
        s.speed(5).clicked(explode)
        s.move_to(arc[1], arc[2], callback = s.destroy)
    else:
        s = image(target, arc[0], 2)
        s.speed(5).clicked(point)
        s.move_to(arc[1], arc[2], callback = lambda: hurt(s))
    callback(spawn, rand(0.5, 3))

score(color = PURPLE)

callback(spawn, rand(0.5, 3))
keydown('r', reset)
