WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'
BACKGROUND = 'grass'
#FULLSCREEN = True

# TODO List
# Zombie mating
# Zombies attack player
# Zombied can attack wall
# Player throw and other movements

# proper animations for non-walking actions

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

p = actor('Soldier-2', (1, 1), tag = 'player', abortable=True).speed(2).keys(precondition=evaluate)
p.move_to((0,0))
p.rate(2)

def wander(sprite) :
	obj_list = get('player')
	hero = obj_list[0]
	x, y = sprite.pos
	#choices = [(up),(down),(left),(right)]
	choices    = [(x, y), (x, y-1), (x, y+1), (x+1, y), (x-1, y)]
	distances  = [distance(p, hero.pos) for p in choices]
	obstacles  = [at(p) for p in choices]
	visibility = [visible(p) for p in choices]
	#print('i am at ' + str(sprite.pos)) 
	#print('my choices are ' + str(choices))
	#print('with distances ' + str(distances))
	#print('and obstacles  ' + str(obstacles))
	#print('and visibility ' + str(visibility))
	best = None
	min_dist = 999999
	for i in range(len(choices)):
		if obstacles[i] is None and visibility[i]:
			#every now and then make a random "bad" move
			rnd = rand(1,10)
			if rnd > 8:
				#print('print making a random choice - ' + str(rnd))
				best = choices[i]
				break
			elif distances[i] < min_dist:
				best = choices[i]
				min_dist = distances[i]
	#print('my best option is ' + str(best))
	if best is not None and best != (x,y):
		vector = (best[0] - x, best[1] - y)
		sprite.move(vector)

def lose(z, p):
	p.life = 0

def create_zombie():
	name = choice(['Zombie-1', 'Zombie-2', 'Zombie-3'])
	z = actor(name, rand_pos(), tag = 'zombie')
	z.wander(wander, time=0.5)
	z.collides(p, lose)

def schedule_zombie():
	create_zombie()
	callback(schedule_zombie, 30)

for x in range(3):
	create_zombie()

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
	pause()
d = shape(RECT, GREEN, (29, 17), tag='destination').collides(p, win)


def shoot(p):
	# air shot -- don't animate the bullet movement
	p.act(SHOOT, loop=1)

	target = p.next_object()
	if target and target.tag == 'wall':
		target.fade(0.5)
	elif target and target.tag == 'zombie':
		#stop other movements when dead
		target.act(DIE, loop=1).rate(1).fade(2)
		for x in range(5):
			create_zombie()

def put(p, direction):
	x, y = p.next(direction)
	if not at((x,y)):
		image('stone', (x, y), tag = 'wall').move_to((x,y))

callback(schedule_zombie, 30)
keydown('space', lambda: shoot(p))
keydown('r', reset)
keydown('w', callback = lambda: put(p, BACK))
keydown('a', callback = lambda: put(p, LEFT))
keydown('s', callback = lambda: put(p, FRONT))
keydown('d', callback = lambda: put(p, RIGHT))
