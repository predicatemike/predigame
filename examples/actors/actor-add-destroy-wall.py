WIDTH = 31
HEIGHT = 19
TITLE = 'MAZE'
BACKGROUND = 'grass'

maze(callback=partial(image, 'stone'))

player = actor('Soldier-2', pos=(1, 1), tag = 'player', abortable=True)
player.speed(2).keys(precondition=player_physics)


def put(player, direction):
	""" put a block at the player's next location (it must be empty) """
	pos = player.next(direction)
	image('stone', pos, tag = 'wall')

keydown('w', callback=partial(put, player, BACK))
keydown('a', callback=partial(put, player, LEFT))
keydown('s', callback=partial(put, player, FRONT))
keydown('d', callback=partial(put, player, RIGHT))

def create_piggy(num=10):
   for x in range(num):
      pos = rand_pos()

      while at(pos) is not None:
         pos = rand_pose()

      piggy = actor('Piggy', pos, tag='piggy')
      piggy.wander(partial(graze, piggy), time=0.75)
create_piggy(15)

def shoot():
	player.act(SHOOT, loop=1)

	target = player.next_object()
	if target and isinstance(target, Actor):
		target.kill()
	elif target:
		target.fade(0.5)

keydown('space', shoot)
