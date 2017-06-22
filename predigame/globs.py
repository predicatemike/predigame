def init(width, height, fps, grid_size):
    global WIDTH, HEIGHT, FPS, GRID_SIZE, background_color, sprites, animations, keys_registered

    WIDTH = width
    HEIGHT = height
    FPS = fps
    GRID_SIZE = grid_size
    background_color = (220, 220, 220)
    sprites = []
    animations = []
    keys_registered = {
        'keydown': {},
        'keyup': {}
    }
