WIDTH = 31
HEIGHT = 19
TITLE = 'Making Bacon'

# use a grass background
BACKGROUND = 'grass'

# how many piggies to create
PIGGIES = 10

# create a daedalus maze with stone images
maze(callback=partial(image, 'stone'))

# create a soldier on the bottom left grid cell
player = actor('Soldier-2', (1, HEIGHT-2), tag='player', abortable=True)

# have the solider attach to the keyboard arrows
# each move is "evaluated" to make sure the player
# doesn't walk through the wall
player.keys(precondition=player_physics)
# player moves at a speed of 5 with an animation rate of 2
# which flips the sprite image every other frame
player.speed(5).rate(2)

# create a piggy function
def create_piggy(num=PIGGIES):
   for x in range(num):
      pos = rand_pos()

      while at(pos) is not None:
         pos = rand_pose()

      piggy = actor('Piggy', pos, tag='piggy')

      # graze is a random walk
      piggy.wander(partial(graze, piggy), time=0.75)

# create some piggies
callback(create_piggy,0.1)

# shoot a weapon
def shoot():
	player.act(SHOOT, loop=1)

	#find the next object that is facing the player
	target = player.next_object()

	# if it's a piggy and that piggy is alive
	if target and target.tag == 'piggy' and target.health > 0:
		# kill the piggy
		target.health = 0
		# make the piggy disappear in 5 seconds
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

# keep track of the time
score(pos=LOWER_LEFT, method=TIMER, step=1, goal=1000)

# register the 'r' key for resetting the game
keydown('r', reset)
