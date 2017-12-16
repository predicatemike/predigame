WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'

def evaluate(action, sprite, pos):
	obj = at(pos)
	if obj:
		if obj.tag == 'destination':
			return True
		else:
			return False
	else:
		return True

p = image('zombie', (1, 1)).speed(7).flip().keys(precondition=evaluate)

def win(b, p):
    text('YOU WIN', BLUE)
    pause()

for y in range(HEIGHT):
    for x in range(WIDTH):
        if (x, y) == (1, 1) or (x, y) == (28, 16):
            continue
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y))
    

d = shape(RECT, GREEN, (28, 16), tag='destination').collides(p, win)

keydown('r', reset)
