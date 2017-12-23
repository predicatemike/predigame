# predigame example: the click ninja
# objective of the game is to survive the longest

# create a game board 20x14 blocks with a title
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

# load 'background/board.jpg' as the wallpaper
BACKGROUND = 'board'

# this callback code will run if a bomb is clicked
def explode(s):

    # play sounds/scream.wav (it's scary)
    sound('scream')

    # print text on the center of the screen
    text('You Survived %s' % time(), MAROON)

    # pause the game
    pause()

# this callbak code will run if you miss something
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

# this callback code will run if you click on an object
def point(s):

    # play sounds/swoosh.wav
    sound('swoosh')

    # draw a splatting image at the position of the strike
    image('redsplat', s.pos, 2)

    # delete the sprite (we don't need it anymore)
    s.destroy()

    # add 5 points to score
    score(5)

# this callback code will run if you click on the taco
def taco(s):

    # play sounds/swoosh.wav
    sound('swoosh')

    # delete the sprite (we don't need it anymore)
    s.destroy()

    # add 50 points to score
    score(50)

# the "main" part of our game
def spawn():

    # pick a random speed
    speed = randint(2, 10)

    # pick a random size
    size = randint(1,4)

    # picks one item at random
    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    # there is a 25% chance to draw a bomb
    if randint(1, 4) == 2:
        target = 'bomb'

    # there is a 10% chance to draw a taco
    # override size
    if randint(1, 10) == 5:
        target = 'taco'
        size = 3

    # a virual "arc" -- three positions where
    # the object will move
    # 1. bottom/off screen
    # 2. top of the arc
    # 3. bottom/off screen
    arc = rand_arc()

    # play sounds/launch.wav
    sound('launch')

    # draw our sprite
    s = image(target, arc[0], size)

    # if our target is a bomb
    if target == 'bomb':
        # register the 'explode' callback function
        s.speed(speed).spin(0.2).clicked(explode)

        # move to second and third points of arc, destroy at end
        s.move_to(arc[1], arc[2], callback = s.destroy)

    # if our target is a taco
    elif target == 'taco':

        # register the 'taco' callback function
        s.speed(5).spin().clicked(taco)

        # move to second and third points of arc, destroy at end
        s.move_to((-10, -2), (-5, HEIGHT/2), (WIDTH+1, HEIGHT/2), callback = s.destroy)

    else:
        # register the 'point' callback function
        s.speed(speed).clicked(point)

        # move to second and third points of arc, call hurt if not hit
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
