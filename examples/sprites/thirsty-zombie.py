WIDTH = 30
HEIGHT = 20
TITLE = 'Thirsty Zombie'

# load in the stormy background
BACKGROUND = 'stormy'

# create a zombie sprite. flip the sprite so the zombie faces to the right
zombie = image('zombie-2', (5, 15), size = 3).speed(10).flip()

# tell the zombie to follow the mouse movement
zombie.follow()

# keep track if the zombie is spinning
spinning = False

# zombie consumes a drink and explodes if it's a coke
def consume(target, zombie):

	# a spinning zombie cannot consume things
	if spinning:
		return

	# destroy the can
	target.destroy()

	if target.name == 'coke':
		# zombies don't like coke. end the game
		zombie.destroy()
		image('kaboom', center=(15, 10), size=25)
		gameover()
	else:
		# we added a sprite. increase score
		score(1)

# zombie misses the opportunity to take a drink and is thirsty.
def miss(target):

	# destroy the can
	target.destroy()

	# subtract a point if this was a sprite
	if target.name == 'sprite':
		score(-1)

	# we lost
	if score() < 0:
		text("TOTAL DEHYDRATION")
		zombie.rotate(90).pulse(time=2, size=2)
		gameover()

# this is a callback that throws a sprite or coke across the screen
def throw_soda():

	# pick a random position and select the y coordinate
	y_pos = rand_pos()[1]

	# create a soda and move it from right to left
	target = 'sprite'

	# roughly 50% of the cans are cokes
	if randint(1, 2) == 2:
		target = 'coke'

	# position the sprite off the right side of the screen
	# make it move fast (speed 10)
	# if the zombie hits the can, execute the "consume" callback
	s = image(target, (WIDTH+5, y_pos)).speed(10).collides(zombie, consume)

	# move the sprite to the left. execute callback "miss" if movement finishes
	s.move_to((-1, y_pos), callback = lambda: miss(s))

	# a callback to call the throw() function again
	callback(throw_soda, rand(0, 1.5))

# schedule the throw callback to run
callback(throw_soda, 1)

# this is a callback when the zombie is done spinning
def done_spinning():

	# the "global" variable is set to False (since we are done spinning)
	global spinning
	spinning = False

# this is a callback when the zombie is hit by a ball
def spinner(b, z):

	# the "global" variable is set to True (since we are spinning)
	global spinning
	spinning = True

	# destroy the ball
	b.destroy()

	# spin the zombie.. time probably can't go much smaller than 0.5
	# execute callback done_spinning after completing two rotations
	z.spin(time=0.5, rotations=2, callback=done_spinning)

# this is a callback function to launch the ball
def launch():

	# create a ball and position off the right side of the screen
	random_y_position = rand_pos()[1]

	# position balls off the screen, make them spin and move a little fast
	ball = image('ball', (WIDTH+5, random_y_position), size=2).spin(0.2).speed(5)

	# move right to left, destroy if movement completes
	ball.move_to((-5, random_y_position), callback=ball.destroy)

	# make the zombie spin if hit by a ball
	ball.collides(zombie, spinner)

	# prepare to launch another
	callback(launch, rand(0.2, 1))

# hitting 'b' starts launching balls!
keydown('b', launch)

# add this so we can keep score of the game
score(color=WHITE)

# press the r key to reset
keydown('r', reset)
