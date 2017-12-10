import os.path, pygame, sys

def get_image_file(name):
    for ext in ['png', 'jpg', 'gif']:
        fname = 'images/' + name + '.' + ext
        if os.path.isfile(fname):
            return fname
    return None

def init(width, height, grid_size, background):
    global WIDTH, HEIGHT, GRID_SIZE, BACKGROUND, BACKGROUND_COLOR, sprites, cells, tags, animations, keys_registered, keys_pressed

    WIDTH = width
    HEIGHT = height
    GRID_SIZE = grid_size
    BACKGROUND = background

    if isinstance(BACKGROUND, str):
        BACKGROUND_COLOR = (220, 220, 220)
        image_file = get_image_file(BACKGROUND)
        if image_file is None:
            sys.exit('Background image doesn\'t exist. File must be saved in images directory ' + BACKGROUND)
        BACKGROUND = pygame.image.load(image_file)
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
