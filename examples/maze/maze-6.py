WIDTH = 29
HEIGHT = 19
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
p = image('player', (1, 1)).speed(10).keys(precondition=evaluate)

# create a daedalus maze
maze(callback=partial(image, 'stone'))

# callback when player claims a coin
def claim(coin, player):
    coin.destroy()
    score(1)

# fill the empty cells with coins
fill(partial(image,'coin'), p, claim)

# keep score
score(color=WHITE)

def timer():
    text("OUT OF TIME")
    gameover()

# finish in 90 seconds
score(90, color=WHITE, pos=UPPER_RIGHT, method=TIMER, step=-1, goal=0, callback=timer)

# register the 'r' key for resetting the game
keydown('r', reset)
