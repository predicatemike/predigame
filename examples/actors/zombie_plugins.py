# A Place for Gamer Customizations

time_left = 30

def setup(player, level_number):
   """ setup is called for every level. this is a place to add new things. """

   # create a black rectangle maze
   #maze(callback=partial(shape, RECT, BLACK))

   # create a stone Maze
   maze(callback=partial(image, 'stone'))

   # pick a single background
   #background('grass')

   # randomly pick a background
   #choices = ['grass', 'ville']
   #background(choice(choices))

   # pick a background for a level
   if level_number == 1:
      background('grass')
   elif level_number == 2:
      background('ville')
   else:
      background('stormy')

   # add a count down timer for 30 seconds
   global time_left
   time_left += 5
   timer(color=WHITE, value=time_left)

   # fill available space with coins
   # pig needs to claim coins
   # def claim(coin, player):
   #  coin.destroy()
   #fill(partial(image, 'coin'), 1, player, claim)

   def __put__(player, direction):
      """ put a block at the player's next location  """
      pos = player.next(direction)
      image('stone', pos, tag = 'wall')

   keydown('w', callback=partial(__put__, player, BACK))
   keydown('a', callback=partial(__put__, player, LEFT))
   keydown('s', callback=partial(__put__, player, FRONT))
   keydown('d', callback=partial(__put__, player, RIGHT))


def punch(level, player):
   print('future home of a punch')

def throw(level, player):
   print('future home of a throw')

def create_targets(num):
   for x in range(num):
      pos = rand_pos()
      while at(pos) is not None:
         pos = rand_pos()

      piggy = actor('Piggy', pos, tag='target')
      piggy.wander(partial(graze, piggy), time=0.75)

def shoot_(level, player):
   player.act(SHOOT, loop=1)
   target = player.next_object()

   # if it's a target and that target is alive
   if target and target.tag == 'target' and target.health > 0:
      target.kill()
      level.hit()

def shoot__(level, player):
   """ air shoot that will kill any actor or sprite """
   player.act(SHOOT, loop=1)
   target = player.next_object()
   if target and isinstance(target, Actor) and target.health > 0:
      target.kill()
      level.hit()
   elif target:
      target.fade(0.5)


def shoot(level, player, repeat=False):
   """ shoot real bullets """
   player.act(SHOOT, loop=1)
   pos = player.facing()
   bpos = player.pos
   bullet = image('bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
   bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))

   def __hit__(bullet, target):
      if target != player:
         bullet.destroy()
         if isinstance(target, Actor) and target.health > 0:
            target.kill()
            if target.tag == 'target' : level.hit()
         else:
            target.fade(0.5)
   bullet.collides(sprites(), __hit__)
   if not repeat:
      callback(partial(shoot, level, player, True), 0.2, repeat=5)

def get_player():
   # name of player sprite (must exist in actors/ directory)
   # return 'Soldier-2'

   # pick a random Soldier
   choices = ['Soldier-1', 'Soldier-2', 'Soldier-3', 'Soldier-4', 'Soldier-5',
              'Soldier-6', 'Soldier-7', 'Soldier-8', 'Soldier-9', 'Soldier-10']
   return choice(choices)
