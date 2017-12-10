from time import sleep

WIDTH = 30
HEIGHT = 18
TITLE = 'ZOMBIE'

def end(b, p):
    p.destroy()
    text('GAME OVER', BLACK)

def evaluate(action, sprite, pos):
	obj = at(pos)
	vis = visible(pos)
	if obj:
		return True
	elif not vis:
		return False
	else:
		return True

def wander(sprite) :
	obj_list = get('hero1')
	hero = obj_list[0]
	x, y = sprite.pos
	choices    = [(x, y), (x, y-1), (x, y+1), (x+1, y), (x-1, y)]
	distances  = [distance(p, hero.pos) for p in choices]
	obstacles  = [at(p) for p in choices]
	visibility = [visible(p) for p in choices]
	best = None
	min_dist = 999999
	for i in range(len(choices)):
		if obstacles[i] is None and visibility[i]:
			#every now and then make a random "bad" move
			rnd = rand(1,10)
			if rnd > 8:
				best = choices[i]
				break
			elif distances[i] < min_dist:
				best = choices[i]
				min_dist = distances[i]
	if best is not None and best != (x,y):
		sprite.move_to(best)


h = image('hero', (1, 1), tag = 'hero1').speed(7).keys(precondition=evaluate)

for x in range(50):
	v = image('scary_thing', rand_pos(), tag = 'zombie' + str(x)).speed(7).wander(wander, time=0.5)

for y in range(HEIGHT):
    for x in range(WIDTH):
        if at((x,y)):
            continue
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y))

shape(RECT, GREEN, (29, 17))
keydown('r', reset)

