def init(width, height, grid_size):
    global WIDTH, HEIGHT, GRID_SIZE, sprites, cells, tags, animations, keys_registered, keys_pressed, mouse_motion

    WIDTH = width
    HEIGHT = height
    GRID_SIZE = grid_size

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
