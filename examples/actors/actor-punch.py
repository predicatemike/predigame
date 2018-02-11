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

def punch():
    player.act(THROW, loop=1)
    target = at(player.next(player.direction))
    if isinstance(target, Actor):
        target.kill()
    elif isinstance(target, Sprite):
        target.fade(0.5)

keydown('p', punch)
