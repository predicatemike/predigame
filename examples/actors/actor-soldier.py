#splats should be in the center
WIDTH = 32
HEIGHT = 6
TITLE = 'Animated Actors'

actors = []

def act(action, seq):
	for a in actors:
		a.act(action, seq)

def register(p1):
	keydown('q', partial(act, SHOOT_BACK, FOREVER))
	keydown('w', partial(act, SHOOT_FRONT, FOREVER))
	keydown('e', partial(act, SHOOT_LEFT, FOREVER))
	keydown('r', partial(act, SHOOT_RIGHT, FOREVER))

	keydown('t', partial(act, THROW_BACK, FOREVER))
	keydown('y', partial(act, THROW_FRONT, FOREVER))
	keydown('u', partial(act, THROW_LEFT, FOREVER))
	keydown('i', partial(act, THROW_RIGHT, FOREVER))

	keydown('a', partial(act, DIE_BACK, FOREVER))
	keydown('s', partial(act, DIE_FRONT, FOREVER))
	keydown('d', partial(act, DIE_LEFT, FOREVER))
	keydown('f', partial(act, DIE_RIGHT, FOREVER))

	keydown('z', partial(act, IDLE_BACK, FOREVER))
	keydown('x', partial(act, IDLE_FRONT, FOREVER))
	keydown('c', partial(act, IDLE_LEFT, FOREVER))
	keydown('v', partial(act, IDLE_RIGHT, FOREVER))

	keydown('b', partial(act, IDLE_AIM_BACK, FOREVER))
	keydown('n', partial(act, IDLE_AIM_FRONT, FOREVER))
	keydown('m', partial(act, IDLE_AIM_LEFT, FOREVER))
	keydown(',', partial(act, IDLE_AIM_RIGHT, FOREVER))

	keydown('1', partial(act, WALK_BACK, FOREVER))
	keydown('2', partial(act, WALK_FRONT, FOREVER))
	keydown('3', partial(act, WALK_LEFT, FOREVER))
	keydown('4', partial(act, WALK_RIGHT, FOREVER))

	keydown('5', partial(act, WALK_AIM_BACK, FOREVER))
	keydown('6', partial(act, WALK_AIM_FRONT, FOREVER))
	keydown('7', partial(act, WALK_AIM_LEFT, FOREVER))
	keydown('8', partial(act, WALK_AIM_RIGHT, FOREVER))


offset = 2

for i in range(10):
	a = actor('Soldier-'+str(i+1), center=(offset, 3), size=5)
	register(a)
	actors.append(a)
	offset = offset + 3


frame_rate = 1
def slower():
	global frame_rate
	frame_rate = frame_rate + 1
	print(frame_rate)
	for a in actors:
		a.rate(frame_rate)

def faster():
	global frame_rate
	frame_rate = frame_rate - 1
	print(frame_rate)
	for a in actors:
		a.rate(frame_rate)

keydown('=', slower)
keydown('-', faster)
