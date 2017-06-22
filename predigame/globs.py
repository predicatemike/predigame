def init(width, height, grid_size):
    global WIDTH, HEIGHT, GRID_SIZE, background_color, sprites, animations, keys_registered

    WIDTH = width
    HEIGHT = height
    GRID_SIZE = grid_size
    background_color = (220, 220, 220)
    sprites = []
    animations = []
    keys_registered = {
        'keydown': {},
        'keyup': {}
    }
