WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

# the "main" part of our game
def spawn():

    # pick a random color
    target = choice([BLACK, ORANGE, AQUA, NAVY])

    # a virual "arc" -- three positions where
    # the object will move
    # arc[0]  bottom/off screen
    # arc[1] top of the arc
    # arc[2] bottom/off screen
    arc = rand_arc()

    # draw our sprite
    s = shape(CIRCLE, target, arc[0])

    # move to second and third points of arc
    # destroy if not hit
    s.move_to(arc[1], arc[2], callback = s.destroy)

    #tell this code to run again -- sometime between 100ms to 3secs
    callback(spawn, rand(0.1, 3))

# keep score (top left)
score(color = PURPLE)

# start the game in 1 second
callback(spawn, 1)

# register the 'r' key to reset the game
keydown('r', reset)  
