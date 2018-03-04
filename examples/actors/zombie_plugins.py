# A Place for Gamer Customizations

def setup(player, level):
   """ setup is called for every level. this is a place to add new things. """

   maze(callback=partial(image, 'stone'))

   player.keys()
   def __wall_buster__(player, wall):
      wall.fade(0.25)
   player.collides(get('wall'), __wall_buster__)

   # randomly pick a background
   if level.level == 1:
      background('grass')
   elif level.level == 2:
      background('ville')
   else:
      background('stormy')

   player.take(Punch(player, trigger='1'))
   player.take(FlameThrower(player, trigger='2'))
   player.take(Grenade(player, trigger='3', distance=6, radius=20))
   player.take(MustardGas(player, trigger='4', distance=10, radius=20))
   player.take(AirGun(player, trigger='space'))
   player.take(MachineGun(player, trigger='5', distance=15, repeat=1))
   player.take(Landmine(player, trigger='6', delay=1))
   player.take(C4(player, trigger='7', detonate='8', distance=8, radius=10))


def blue_defend(actor):
   """ activate self defense """
   for direction in [BACK, FRONT, LEFT, RIGHT]:
      things = actor.next_object(direction=direction, distance=10)
      if things and has_tag(things, 'red'):
            actor.direction = direction
            actor.stop = True
            actor.act(HAPPY, 5)
            target = actor.next_object()
            if target and isinstance(target, Actor):
               target.kill()
            callback(partial(actor.act, IDLE, FOREVER), 5)

def get_blue():
   """ create a blue (friendly) actor """
   # return name of actor, grazing speed, self defense
   return 'Piggy', 2, blue_defend

def get_red():
   """ create a red (hostile) actor """
   # return name of actor, movement speed
   return 'Zombie-1', 2

def get_player():
   # name of player sprite (must exist in actors/ directory)
   # return 'Soldier-2'

   # pick a random Soldier
   choices = ['Soldier-1', 'Soldier-2', 'Soldier-3', 'Soldier-4', 'Soldier-5',
              'Soldier-6', 'Soldier-7', 'Soldier-8', 'Soldier-9', 'Soldier-10']
   return choice(choices)
