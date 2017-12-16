# predigame example: the click ninja
# objective of the game is to survive the longest
# +5 points is given for each non-bomb successfully swiped
# -20 points is deducted if you miss


# create a game board 20x14 blocks
WIDTH = 20
HEIGHT = 14

# the title of this window
TITLE = 'Click Ninja'

# load 'background/board.jpg' as the 
# wallpaper background image
BACKGROUND = 'board'

# callback function
# this code will run if a bomb is clicked
def explode(s):

    # play sounds/scream.wav (it's scary)
    sound('scream')

    # print text on the center of the screen
    text('You Survived %s seconds' % time(), MAROON)

    # pause the game
    pause()

# callback function
# this code will run if you miss something
def hurt(s):

    # delete the sprite (we don't need it anymore)
    s.destroy()

    # subtract 20 points to score
    score(-20)

    # game is over if the score falls below zero
    if score() < 0:
        sound('scream')
        text('You Survived %s' % time(), MAROON)
        pause()

# callback function
# this code will run if you click on an object
def point(s):

    # play sounds/swoosh.wav
    sound('swoosh')

    # draw a splatting image at the position of
    # the sprite
    image('redsplat', s.pos, 2)

    # delete the sprite (we don't need it anymore)
    s.destroy()

    # add 5 points to score
    score(5)

# the "main" part of our game
def spawn():

    # all of our food
    # this is a python list where choice
    # picks one item at random
    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    # there is a 25% chance to draw a bomb
    if randint(1, 4) == 2:
        target = 'bomb'

    # a virual "arc" -- three positions where
    # the object will move
    # 1. bottom/off screen
    # 2. top of the arc
    # 3. bottom/off screen
    arc = rand_arc()

    # play sounds/launch.wav
    sound('launch')

    # draw our sprite
    s = image(target, arc[0], 2)

    # pick a random speed
    speed = randint(2, 10)

    # if our target is a bomb
    if target == 'bomb':
        # register the 'explode' callback function
        s.speed(speed).spin(0.2).clicked(explode)

        # move to second and third points of arc
        # destroy if not hit
        s.move_to(arc[1], arc[2], callback = s.destroy)

    else:
        # this is food
        # register the 'point' callback function
        s.speed(speed).clicked(point)

        # move to second and third points of arc
        # destroy if not hit
        s.move_to(arc[1], arc[2], callback = lambda: hurt(s))

    #tell this code to run again -- sometime between 100ms to 3secs
    callback(spawn, rand(0.1, 3))

# keep score (top left)
score(color = PURPLE)

# start the game
callback(spawn, rand(0.1, 3))

# register some keys
# r - rest game
keydown('r', reset)
