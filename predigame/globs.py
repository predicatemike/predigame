import pygame, sys, os

def get_image_file(name):
    for ext in ['png', 'jpg', 'gif']:
        fname = 'backgrounds/' + name + '.' + ext
        if os.path.isfile(fname):
            return pygame.image.load(fname).convert()

    return None

def init(width, height, grid_size, background):
    global WIDTH, HEIGHT, GRID_SIZE, BACKGROUND, BACKGROUND_COLOR, sprites, cells, tags, animations, keys_registered, keys_pressed, mouse_motion

    WIDTH = width
    HEIGHT = height
    GRID_SIZE = grid_size
    BACKGROUND = background

    if isinstance(BACKGROUND, str):
        BACKGROUND_COLOR = (220, 220, 220)
        BACKGROUND = get_image_file(BACKGROUND)
        if BACKGROUND is None:
            sys.exit('Background image doesn\'t exist. File must be saved in backgounds directory: ' + background)
        else:
            #size background to fix screen
            BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
    else :
        BACKGROUND_COLOR = BACKGROUND

    sprites = []
    cells = {}
    tags = {}
    animations = []
    keys_registered = {
        'keydown': {},
        'keyup': {}
    }
    keys_pressed = []
    mouse_motion = []
