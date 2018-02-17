# A Place for Gamer Customizations

time_left = 30

def setup(player, level_number):
   """ setup is called for every level. this is a place to add new things. """

   # create a black rectangle maze
   #maze(callback=partial(shape, RECT, BLACK))

   # create a stone Maze
   maze(callback=partial(image, 'stone'))
   #for y in range(31):
   #   for x in range(19):
   #      if rand(1, 3) > 2.75:
   #         shape(RECT, RED, (x, y), tag='wall')


   # pick a random background (this may take a while)
   # background()
   # pick a single background
   #background(GRAY)

   # randomly pick a background
   choices = ['grass', 'ville']
   background(choice(choices))

   # pick a background for a level
   #if level_number == 1:
   #   background('grass')
   #elif level_number == 2:
   #   background('ville')
   #else:
   #   background('stormy')

   # add a count down timer for 30 seconds
   #global time_left
   #time_left += 5
   #timer(color=WHITE, value=time_left)

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

def throw(level, player, repeat=False):
   #print('future home of a throw')
   """ flame thrower """
   player.act(THROW, loop=1)
   pos = player.facing()
   bpos = player.pos
   beam = shape(ELLIPSE, RED, pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)

   def __hit__(beam, target):
      if target != player:
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   beam.collides(sprites(), __hit__)

   def __grow__(beam):
      beam.move_to(player.facing())
      beam.scale(1.1).speed(10)
      if beam.size > 20:
        beam.fade(1)

   if not repeat:
      callback(partial(__grow__, beam), wait=0.1, repeat=50)

def shoot_(level, player):
   player.act(SHOOT, loop=1)
   target = player.next_object()

   if target and isinstance(target, Actor):
      target.kill()

def shoot__(level, player):
   """ air shot that will kill any actor or sprite """
   player.act(SHOOT, loop=1)
   target = player.next_object()
   if target and isinstance(target, Actor):
      target.kill()
      level.hit()
   elif target and isinstance(target, Sprite):
      target.fade(0.5)

def shoot(level, player, repeat=False):
   """ shoot real bullets """
   player.act(SHOOT, loop=1)
   pos = player.facing()
   bpos = player.pos
   bullet = image('bullet', tag='bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
   bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))

   def __hit__(bullet, target):
      if target != player:
         bullet.destroy()
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   bullet.collides(sprites(), __hit__)
   if not repeat:
      callback(partial(shoot, level, player, True), wait=0.2, repeat=5)

def get_blue():
   """ create a blue (friendly) actor """
   return 'Piggy'

def get_red():
   """ create a red (hostile) actor """
   return "Zombie-1"

def get_player():
   # name of player sprite (must exist in actors/ directory)
   # return 'Soldier-2'

   # pick a random Soldier
   choices = ['Soldier-1', 'Soldier-2', 'Soldier-3', 'Soldier-4', 'Soldier-5',
              'Soldier-6', 'Soldier-7', 'Soldier-8', 'Soldier-9', 'Soldier-10']
   return choice(choices)
