WIDTH = 30
HEIGHT = 20
TITLE = 'Sprites Demo'


text("Shape Sprites", BLACK, pos = (0,0), size = 1.25)

# create a circle
shape(CIRCLE, RED, (2, 2))

# create a big blue circle next to the red one
shape(CIRCLE, BLUE, (5, 1), 3)

# create a 2x2 ORANGE square at position (10,2)
shape(RECT, ORANGE, (10, 2), (2,2))

# create a 6x1 rectangle
shape(RECT, AQUA, (15, 2), (6, 1))

# create a custom colored (r, g, b) ELLIPSE
shape(ELLIPSE, (134, 134, 134), (23, 2), (5, 2))

text("Image Sprites", BLACK, pos = (0, 6), size = 1.25)

image('sprite', (2, 8))
image('coke', (7, 8), size = 2)
image('zombie-1', (13,9), size = 5)
image('zombie-2', (19,9), size = 5)

text("Sprite Effects", BLACK, pos = (0, 12), size = 1.25)

image('sprite', (2,14)).spin(time=1)
image('sprite', (7,14)).pulse(time=0.5, size=3)
image('coke', (13, 15), size = 2).speed(1).float(distance=1)

def doit(s):
	s.destroy()
	image('kaboom', (15, 10), size=25)

image('clickme', (19, 15), size = 2).pulse(time=0.05, size= 1.25).clicked(doit)


s = image('coke', (13, 15), size = 2)
s.speed(1).bouncy().spin().pulse().clicked(s.destroy)

def eatit(z, s):
	s.destroy()
	z.scale(1.2)


image('zombie-1', (28, 18), size = 2).keys().collides(sprites(), eatit)
image('zombie-2', (25, 18), size = 2).keys(right='d', left='a', up='w', down='s').collides(sprites(), eatit)
keydown('r', reset)

