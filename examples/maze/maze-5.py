WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'

# a callback that keeps the player from running
# into walls. it's only acceptable to walk into
# an object marked as a "destination"
def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj:
        if obj.tag != 'wall':
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

# load a maze from a file
maze('2', partial(image, 'stone'))

# a callback function for when the player reaches
# the green destination
def win(b, p):
    text('YOU WIN', BLUE)
    gameover()

# draw a green destination cell on the bottom right
d = shape(RECT, GREEN, (WIDTH-1, HEIGHT-1), tag='destination')

# if the player reaches this cell, execute the 'win' callback
d.collides(p, win)

# callback when player claims a coin
def claim(coin, player):
    coin.destroy()
    score(1)

# fill the empty cells with coins
for x in range(WIDTH):
    for y in range(HEIGHT):
        if at((x, y)) is None:
            image('coin', (x,y)).collides(p, claim)

# keep score
score(color=BLUE)

# register the 'r' key for resetting the game
keydown('r', reset)
