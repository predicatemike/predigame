WIDTH = 30
HEIGHT = 20
TITLE = 'Shooting Bullets Example'
BACKGROUND = 'grass'

maze(callback=partial(image, 'stone'))



def create_piggy(num=10):
   for x in range(num):
      pos = rand_pos()

      while at(pos) is not None:
         pos = rand_pose()

      piggy = actor('Piggy', pos, tag='piggy')
      piggy.wander(partial(graze, piggy), time=0.75)
create_piggy(15)

player = actor('Soldier-2', pos=(1, 1), tag = 'player', abortable=True)
player.speed(2).keys()
stop = False

def load():
	global stop
	stop = False

def stopit():
	global stop
	stop = True

def hit(bullet, obj):
	if obj != player:
		if isinstance(obj, Actor):
			obj.kill()
		elif isinstance(obj, Sprite):
			obj.fade(0.25)

def machine_gun():
	player.act(SHOOT, loop=1)
	pos = player.facing()
	bpos = player.pos
	bullet = image('bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
	bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))
	bullet.collides(sprites(), hit)
	if not stop:
		callback(machine_gun, 0.25)

keydown('space', machine_gun)
keydown('s', stopit)
keydown('l', load)
