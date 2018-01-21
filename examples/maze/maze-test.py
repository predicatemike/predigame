WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE From File'

# load a sample maze
maze('1', partial(shape, RECT, RED))

# load another sample maze
maze('2', partial(image, 'stone'))


# center the player on the 0,0 grid cell
p = image('player', (0, 0)).speed(5).keys()
p.move_to((0, 0))

keydown('r', reset)