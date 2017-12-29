WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'
BACKGROUND = 'grass'
#FULLSCREEN = True
#SIZE = 75
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

p = actor('Soldier-2', (1, 1), tag = 'player', directions=4, abortable=True).speed(2).keys(precondition=evaluate)
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

actor('Zombie-1', rand_pos(), tag = 'zombie1', directions=4).wander(wander, time=0.5)
actor('Zombie-2', rand_pos(), tag = 'zombie2', directions=4).wander(wander, time=0.5)
actor('Zombie-3', rand_pos(), tag = 'zombie3', directions=4).wander(wander, time=0.5)

def win(b, p):
    text('YOU WIN', BLUE)
    pause()

for y in range(HEIGHT):
    for x in range(WIDTH):
        if (x, y) == (1, 1) or (x, y) == (28, 16):
            continue
        if rand(1, 3) > 2.5:
            image('stone', (x, y)).move_to((x,y))

    
# destination block
d = shape(RECT, GREEN, (28, 16), tag='destination').collides(p, win)

def shoot(p):
	p.act(SHOOT, loop=1)
	# add a little buffer to the position to center the bullet
	x, y = p.pos
	fx, fy = p.facing()
	bullet = shape(CIRCLE, BLACK, (x+0.5, y+0.5), 0.25).speed(20)
	bullet.move_to((fx+0.5, fy+0.5))

keydown('space', lambda: shoot(p))
keydown('r', reset)
