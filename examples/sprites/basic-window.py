WIDTH = 30
HEIGHT = 20
TITLE = 'Window Demo'

# turn on the grid lines
grid()

# place on center of screen
text("Understanding Grid Coordinates", color=BLACK, size = 2.0)
text("this is a 30 x 20 window", color=BLACK, pos=(WIDTH/2-7, HEIGHT/2+1), size = 1.75)

# top/left
shape(RECT, RED, (0, 0))
text("(0, 0)", RED, pos = (0,1), size = 1.25)

# bottom/left
shape(RECT, BLUE, (0, HEIGHT-1))
text("(0, " + str(HEIGHT-1) + ")", BLUE, pos = (0, HEIGHT-2), size=1.25)

# top/right
shape(RECT, PINK, (WIDTH-1, 0))
text("(" + str(WIDTH-1) + ", 0)", PINK, pos = (WIDTH-2.5,1), size = 1.25)

# bottom/right
shape(RECT, PURPLE, (WIDTH-1, HEIGHT-1))
text("(" + str(WIDTH-1) + ", " + str(HEIGHT-1) + ")", PURPLE, pos = (WIDTH-3,HEIGHT-2), size = 1.25)

# instruct the sprite to move left to right
# when finished invoke callback for right_to_left
def left_to_right(s):
	# s.pos[1] is the y-axis
	s.move_to((WIDTH-1, s.pos[1]), callback=lambda: right_to_left(s))

# instruct the sprite to move right to left
# when finished invoke callback for left_to_right
def right_to_left(s):
	s.move_to((0, s.pos[1]), callback=lambda: left_to_right(s))

# shape will move left to right and back
# this one appears above the text
s = shape(RECT, MAROON, (0,5)).speed(8)
left_to_right(s)

# shape will move right to and back
# this one appears below the text
s = shape(RECT, MAROON, (WIDTH-1, HEIGHT-5)).speed(8)
right_to_left(s)

# this is a callback function to launch the ball
def launch():
	# create a ball and position off the right side of the screen
	random_y_position = rand_pos()[1]

	# we can't see WIDTH+5
	ball = image('ball', (WIDTH+5, random_y_position), size=2).spin(0.2).speed(5)

	# move the ball to the left, destroy after movement complete
	ball.move_to((-5, random_y_position), callback=ball.destroy)

	# prepare to launch another
	callback(launch, rand(0, 0.5))

# hitting 'b' starts launching balls!
keydown('b', launch)
