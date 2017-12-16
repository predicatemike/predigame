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
	print(str(sprite.pos) + '-->' + str(pos) + ': is visible? ' + str(vis) + ' at ' + str(obj))
	if obj:
		print('here is ' + obj.tag)
		return False
		#if obj.tag == 'zombie1':
		#	end(obj, sprite)
		#	return True
		#else:
		#	return False
	elif not vis:
		return False
	else:
		return True

def wander(sprite) :
	obj_list = get('hero1')
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
		sprite.move_to(best)


h = image('hero', (1, 1), tag = 'hero1').speed(7).keys(precondition=evaluate)

for x in range(10):
	v = image('zombie', rand_pos(), tag = 'zombie' + str(x)).speed(7).wander(wander, time=0.5)

for y in range(HEIGHT):
    for x in range(WIDTH):
        if at((x,y)):
            continue
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y))

keydown('r', reset)

