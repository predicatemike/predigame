# A Place for Gamer Customizations

def setup(player, level):
   """ setup is called for every level. this is a place to add new things. """
   callback(level.create_blue, wait=1)
   # create a black rectangle maze
   #maze(callback=partial(shape, RECT, BLACK))

   # create a stone Maze
   maze(callback=partial(image, 'stone'))
   #for y in range(31):
   #   for x in range(19):
   #      if rand(1, 3) > 2.75:
   #         shape(RECT, RED, (x, y), tag='wall')

   player.keys()

   def __wall_buster__(player, wall):
      wall.fade(0.25)
   player.collides(get('wall'), __wall_buster__)

   # pick a random background (this may take a while)
   # background()
   # pick a single background
   #background(GRAY)

   # randomly pick a background
   if level.level == 1:
      background('grass')
   elif level.level == 2:
      background('ville')
   else:
      background('stormy')

   #callback(level.create_red, wait=1, repeat=5)
   #callback(level.create_blue, wait=1, repeat=5)
   #callback(level.create_red, wait=1, repeat=FOREVER)
   #callback(level.create_red, wait=randint(10,20), repeat=FOREVER)

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
   #timer(color=WHITE, value=30*level_number)

   # fill available space with coins
   # pig needs to claim coins
   # def claim(coin, player):
   #  coin.destroy()
   #fill(partial(image, 'coin'), 1, player, claim)

   def __drop__(player):
      """ put a landmine right where the player is standing """
      mine = image('mine', player.pos, tag = 'mine')

      def __hit__(mine, target):
         """ mine hits something and that something dies """
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)

      def __explode__(mine, sprite):
         """ explode the mine """
         if mine != sprite:
            mine.collides(sprites(), __hit__)
            callback(partial(mine.fade, 2), 1)
      # wait three seconds to activate the mine
      callback(partial(mine.collides, sprites(), __explode__), wait=3)
   keydown('m', callback=partial(__drop__, player))

   def __direction__(player, direction):
      """ change the players direction  """
      player.direction = direction
      player.act(IDLE, FOREVER)

   keydown('left', callback=partial(__direction__,player, LEFT))
   keydown('right', callback=partial(__direction__,player, RIGHT))
   keydown('up', callback=partial(__direction__,player, BACK))
   keydown('down', callback=partial(__direction__,player, FRONT))

   player.keys(right = 'd', left = 'a', up = 'w', down = 's')
   def __wall_buster__(player, wall):
      wall.fade(0.25)
   player.collides(get('wall'), __wall_buster__)

   def __completed__(self):
      if self.blue_spawned == self.blue_safe and len(get('red')) == 0:
         return True
   level.completed = MethodType(__completed__, level)


def punch(level, player):
   #print('future home of a punch')
   player.act(THROW, loop=1)
   target = at(player.next(player.direction))
   if isinstance(target, Actor):
       target.kill()
   elif isinstance(target, Sprite):
       target.fade(0.5)

def throw(level, player, repeat=False):
   """ throw some c-4 (explodes on '3' button press)"""
   player.act(THROW, loop=1)
   # set the range of the c4
   pos = player.facing(8)
   bpos = player.pos
   c4 = image('mine', tag='c4', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.5).spin(0.25)

   def __hit__(c4, target):
      if target != c4 and target != player:
         if isinstance(target, Actor):
            target.kill()
   def __explode__(c4):
      c4.destroy()
      cpos = c4.pos
      exp = shape(CIRCLE, RED, (cpos[0]-1.5,cpos[1]-1.5), size=0.3)
      exp.collides(sprites(), __hit__)
      exp.scale(10)
      callback(partial(exp.fade, 1), 0.5)
   def __detonate__():
      bombs = get('c4')
      for bomb in bombs:
         callback(partial(__explode__, bomb), 0.25)
   keydown('3', __detonate__)
   c4.move_to(pos)


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
   pos = player.facing(7)
   bpos = player.pos
   bullet = image('bullet', tag='bullet', pos=(bpos[0]+0.85, bpos[1]+0.35), size=0.3)
   bullet.speed(9.5).move_to((pos[0]+0.5,pos[1]+0.35),callback=bullet.destroy)

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
   # return name of actor and grazing speed
   return 'Piggy', 2

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
