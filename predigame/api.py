from functools import partial
from random import uniform as rand
from random import randint
from random import choice, shuffle
from .predigame import actor, image, maze, shape, background, sound, text, grid, time, callback, score, reset_score, destroyall, pause, resume, gameover, reset, quit, screenshot
from .constants import *
from .utils import register_keydown as keydown, at, get
from .utils import animate, rand_pos, rand_arc, distance, visible, sprites, graze, track, fill
from .Thing import Thing
