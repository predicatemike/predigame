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

def left_to_right(s):
	s.move_to((WIDTH-1, s.pos[1]), callback=lambda: right_to_left(s))

def right_to_left(s):
	s.move_to((0, s.pos[1]), callback=lambda: left_to_right(s))

s = shape(RECT, MAROON, (0,5)).speed(8)
left_to_right(s)

s = shape(RECT, MAROON, (WIDTH-1, HEIGHT-5)).speed(8)
right_to_left(s)