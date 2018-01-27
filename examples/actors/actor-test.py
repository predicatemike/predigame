WIDTH = 30
HEIGHT = 18
TITLE = 'Making Bacon'

# use a grass background
BACKGROUND = 'grass'

# how many piggies to create
PIGGIES = 10

# create a daedalus maze with stone images
maze(callback=partial(image, 'stone'))

# a callback that keeps the player from running
# into walls. 
def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj and obj.tag == 'wall':
    	return False
    else:
        return True

# create a soldier on the bottom left grid cell
player = actor('Soldier-2', (0, HEIGHT-1), tag='player', abortable=True)

# have the solider attach to the keyboard arrows
# each move is "evaluated" to make sure the player
# doesn't walk through the wall
player.keys(precondition=evaluate)

# player moves at a speed of 5 with an animation rate of 2
# which flips the sprite image every other frame
player.speed(5).rate(2).move_to((0, HEIGHT-1))

# create a piggy function
def create_piggy(num):
	for x in range(num):
		pos = rand_pos()
		piggy = actor('Piggy', pos, tag='piggy')
		piggy.move_to((pos))
		# graze is a random walk
		piggy.wander(graze, time=0.4)

# create some piggies
create_piggy(PIGGIES)

# shoot a weapon
def shoot():
	player.act(SHOOT, loop=1)

	#find the next object that is facing the player
	target = player.next_object()

	# if it's a piggy and that piggy is alive
	if target and target.tag == 'piggy' and target.health > 0:
		# kill the piggy
		target.health = 0
		# make the piggy disappear in 10 seconds
		target.destruct(5)
		# get a point
		score(1)

	# check to see if there are any piggys left
	if score() == PIGGIES:
		text('Time for some BACON!! (%s secs)' % time(), color=BLACK)

# register space to shoot
keydown('space', shoot)

#we're keeping score
score()

# register the 'r' key for resetting the game
keydown('r', reset)


