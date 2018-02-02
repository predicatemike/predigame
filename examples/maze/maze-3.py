WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'

# a callback that keeps the player from running
# into walls. it's only acceptable to walk into
# an object marked as a "destination"
def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj:
        if obj.tag == 'destination':
            return True
        else:
            return False
    else:
        return True


# create a sprite based on the "player" image
# position at the top left corner. control the
# sprite with the arrow keys while checking a
# precondition to make sure we don't walk into
# walls. the speed of the sprite enables "graceful"
# movement with the keyboard
p = image('player', (0, 0)).speed(5).keys(precondition=evaluate)

# center the player on the 0,0 grid cell
p.move_to((0, 0))


# these two nested for loops iterate over
# every grid cell on the canvas
for y in range(HEIGHT):
    for x in range(WIDTH):
    	# don't create a block on the location of
    	# the player OR the location of the green cell
        if (x, y) == (0, 0) or (x, y) == (29, 16):
            continue
        # make a random decision to color the cell red
        # this number can be adjusted to make the cells
        # smaller or larger.
        if rand(1, 3) > 2.5:
            image('stone', (x, y)).move_to((x,y))

# a callback function for when the player reaches
# the green destination
def win(b, p):
    text('YOU WIN', BLUE)
    gameover()

# draw a green destination cell on the bottom right
d = shape(RECT, GREEN, (WIDTH-1, HEIGHT-1), tag='destination')

# if the player reaches this cell, execute the 'win' callback
d.collides(p, win)

# register the 'r' key for resetting the game
keydown('r', reset)
