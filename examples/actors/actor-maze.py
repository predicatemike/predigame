WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'
BACKGROUND = 'grass'

# TODO List
# Zombie mating
# Zombies attack player
# Zombied can attack wall

# Player throw and other movements
# proper animations for non-walking actions
# add more sprites

def evaluate(action, sprite, pos):
	obj = at(pos)
	if obj:
		if obj.tag == 'destination':
			return True
		else:
			print('object in the way at ' + str(pos))
			return False
	else:
		return True


# wander method for the piggies
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

GUN = 'gun'
class Gun(Thing):
	def __init__(self):
		self.damange = 100
		self.quantity = 10
	def use(self, actor, object = None):
		if self.quantity <= 0:
			return

		# air shot -- don't animate the bullet movement
		actor.act(SHOOT, loop=1)

		target = actor.next_object()
		if target and target.tag == 'wall':
			target.fade(0.5)
		elif target and target.tag == 'zombie':
			#stop other movements when dead
			target.act(DIE, loop=1).rate(1).fade(2)
			for x in range(5):
				create_zombie()

		self.quantity -= 1

PUNCH = 'punch'
class Punch(Thing):
	def __init__(self):
		self.damange = 100
	def use(self, actor, object = None):
		actor.act(THROW, loop=1)
		target = at(actor.next(actor.direction))
		if target is not None:
			target.fade(0.5)


p = actor('Soldier-2', (1, 1), tag = 'player', abortable=True).speed(2).keys(precondition=evaluate)
p.move_to((0,0))
p.rate(2)
p.take(GUN, Gun()).take(PUNCH, Punch())


for i in range(10):
	piggy = actor('Piggy', rand_pos(), tag = 'piggy')
	piggy.wander(partial(graze, piggy), time=0.4)

def lose(z, p):
	p.health = 0

def create_zombie():
	name = choice(['Zombie-1', 'Zombie-2', 'Zombie-3'])
	z = actor(name, (WIDTH-1, 0), tag = 'zombie')
	z.wander(partial(track, z, pbad=0.1), time=0.5)
	z.collides(p, lose)

def schedule_zombie():
	create_zombie()
	callback(schedule_zombie, 30)

# zombies come out of the zombie house
image('zombie_house', center=(WIDTH-1, 1), size=2)

# create three zombies
for x in range(3):
	create_zombie()

# draw some random walls
for y in range(HEIGHT):
    for x in range(WIDTH):
        if at((x,y)) or (x, y) == (0, 0) or (x, y) == (29, 17):
            continue
        if rand(1, 3) > 2.95:
            image('stone', (x, y), tag = 'wall').move_to((x,y))


# destination block
def win(b, p):
	if len(get('wall')) == 0:
		text('YOU WIN', BLUE)
	else:
		text('I SEE WALLS! YOU FAILED!', RED)
	gameover()
d = shape(RECT, GREEN, (29, 17), tag='destination').collides(p, win)


# player object for dropping a block
def put(p, direction):
	x, y = p.next(direction)
	if not at((x,y)):
		image('stone', (x, y), tag = 'wall').move_to((x,y))

callback(schedule_zombie, 30)
keydown('space', lambda: p.use(GUN))
keydown('p', lambda: p.use(PUNCH))
keydown('r', reset)
keydown('w', callback = lambda: put(p, BACK))
keydown('a', callback = lambda: put(p, LEFT))
keydown('s', callback = lambda: put(p, FRONT))
keydown('d', callback = lambda: put(p, RIGHT))
