WIDTH = 30
HEIGHT = 20
TITLE = 'Thirsty Zombie'

# create a zombie sprite. flip the sprite so the zombie faces to the right
zombie = image('zombie-2', (5, 15), size = 3).speed(10).keys().flip().follow()

# zombie consumes a drink and explodes if it's a coke
def consume(target, zombie):
	target.destroy()

	if target.name == 'coke':
		zombie.destroy()
		image('kaboom', (15, 10), size=25)
		gameover()
	else:
		score(1)

# zombie misses the opportunity to take a drink and is thirsty.
def miss(target):
	target.destroy()
	
	# subtract a point if this was a sprite
	if target.name == 'sprite':
		score(-1)

	if score() < 0:
		text("TOTAL DEHYDRATION")
		zombie.rotate(90)
		gameover()

def throw():
	# pick a random position and select the y coordinate
	y_pos = rand_pos()[1]

	# create a soda and move it from right to left
	target = 'sprite'
	if randint(1, 2) == 2:
		target = 'coke'		
	s = image(target, (WIDTH+5, y_pos)).speed(10).collides(zombie, consume)
	s.move_to((-1, y_pos), callback = lambda: miss(s))

	# a callback to call the throw() function again
	callback(throw, rand(0, 1.5))

# schedule the throw callback to run
callback(throw, rand(1,2))

score()

keydown('r', reset)

