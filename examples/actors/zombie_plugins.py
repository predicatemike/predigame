# A Place for Gamer Customizations

time_left = 30

def setup(player, level):
   """ setup is called for every level. this is a place to add new things. """

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

   def __put__(player, direction):
      """ put a block at the player's next location  """
      pos = player.next(direction)
      image('stone', pos, tag = 'wall')

   keydown('w', callback=partial(__put__, player, BACK))
   keydown('a', callback=partial(__put__, player, LEFT))
   keydown('s', callback=partial(__put__, player, FRONT))
   keydown('d', callback=partial(__put__, player, RIGHT))

def punch(level, player):
   #print('future home of a punch')
   player.act(THROW, loop=1)
   target = at(player.next(player.direction))
   if isinstance(target, Actor):
       target.kill()
   elif isinstance(target, Sprite):
       target.fade(0.5)

def throw(level, player, repeat=False):
   """ grenade thrower """
   player.act(THROW, loop=1)
   # set the range of the grenade
   pos = player.facing(5)
   bpos = player.pos
   grenade = image('grenade', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.3).spin(0.25)

   def __hit__(grenade, target):
      if target != grenade:
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   def __explode__(grenade):
      grenade.destroy()
      exp = shape(CIRCLE, RED, grenade.pos, size=0.3)
      exp.collides(sprites(), __hit__)
      exp.scale(10)
      callback(partial(exp.fade, 1), 0.5)
   grenade.move_to(pos, callback=callback(partial(__explode__, grenade), wait=1))


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
