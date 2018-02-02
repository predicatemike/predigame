#splats should be in the center
WIDTH = 32
HEIGHT = 6
TITLE = 'Animated Actors'

def register(p1):
	keydown('q', lambda: p1.act(SHOOT_BACK, FOREVER))
	keydown('w', lambda: p1.act(SHOOT_FRONT, FOREVER))
	keydown('e', lambda: p1.act(SHOOT_LEFT, FOREVER))
	keydown('r', lambda: p1.act(SHOOT_RIGHT, FOREVER))

	keydown('t', lambda: p1.act(THROW_BACK, FOREVER))
	keydown('y', lambda: p1.act(THROW_FRONT, FOREVER))
	keydown('u', lambda: p1.act(THROW_LEFT, FOREVER))
	keydown('i', lambda: p1.act(THROW_RIGHT, FOREVER))

	keydown('a', lambda: p1.act(DIE_BACK, FOREVER))
	keydown('s', lambda: p1.act(DIE_FRONT, FOREVER))
	keydown('d', lambda: p1.act(DIE_LEFT, FOREVER))
	keydown('f', lambda: p1.act(DIE_RIGHT, FOREVER))

	keydown('z', lambda: p1.act(IDLE_BACK, FOREVER))
	keydown('x', lambda: p1.act(IDLE_FRONT, FOREVER))
	keydown('c', lambda: p1.act(IDLE_LEFT, FOREVER))
	keydown('v', lambda: p1.act(IDLE_RIGHT, FOREVER))

	keydown('b', lambda: p1.act(IDLE_AIM_BACK, FOREVER))
	keydown('n', lambda: p1.act(IDLE_AIM_FRONT, FOREVER))
	keydown('m', lambda: p1.act(IDLE_AIM_LEFT, FOREVER))
	keydown(',', lambda: p1.act(IDLE_AIM_RIGHT, FOREVER))

	keydown('1', lambda: p1.act(WALK_BACK, FOREVER))
	keydown('2', lambda: p1.act(WALK_FRONT, FOREVER))
	keydown('3', lambda: p1.act(WALK_LEFT, FOREVER))
	keydown('4', lambda: p1.act(WALK_RIGHT, FOREVER))

	keydown('5', lambda: p1.act(WALK_AIM_BACK, FOREVER))
	keydown('6', lambda: p1.act(WALK_AIM_FRONT, FOREVER))
	keydown('7', lambda: p1.act(WALK_AIM_LEFT, FOREVER))
	keydown('8', lambda: p1.act(WALK_AIM_RIGHT, FOREVER))


offset = 2
actors = []
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
