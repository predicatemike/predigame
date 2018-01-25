WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'
BACKGROUND = 'grass'

# create a soldier actor with keyboard movements 
# these movements that can be aborted (if other movements are made)
player = actor('Soldier-2', (1, 1), tag='player', abortable=True).keys(immediate=True)

# player moves at a speed of 2 with an animation rate of 2
# which flips the sprite image every other move
player.speed(50).rate(2)

# wander method for the piggies
# move this to utils
def graze(sprite) :
	x, y = sprite.pos
	choices    = [(x,y), (x, y-1), (x, y+1), (x+1, y), (x-1, y)]
	shuffle(choices)
	obstacles  = [at(p) for p in choices]
	visibility = [visible(p) for p in choices]	

	for i in range(len(choices)):
		if obstacles[i] is None and visibility[i]:
			if choices[i] != (x, y):
				sprite.move((choices[i][0] - x, choices[i][1] - y))
				break

# create some piggies
def create_piggy():
    piggy = actor('Piggy', rand_pos(), tag='piggy')
    piggy.wander(graze, time=0.4)
    callback(create_piggy, rand(0, 2))
callback(create_piggy, 1)


# air shot -- don't animate the bullet movement
def shoot():
	player.act(SHOOT, loop=1)
	target = player.next_object()
	if target and target.tag == 'piggy':
		#stop other movements when dead
		target.act(DIE, loop=1).rate(1).fade(2)

# register the 'r' key for resetting the game
keydown('r', reset)
keydown('space', shoot)
