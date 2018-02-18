# A Place for Gamer Customizations

def setup(player, level_number):
   """ setup is called for every level. this is a place to add new things. """

   # create a stone Maze
   maze(callback=partial(image, 'stone'))

   background('grass')

def punch(level, player):
   print('future home of a punch')

def throw(level, player, repeat=False):
   print('future home of a throw')

def shoot(level, player):
   player.act(SHOOT, loop=1)
   target = player.next_object()

   if target and isinstance(target, Actor):
      target.kill()

def get_blue():
   """ create a blue (friendly) actor """
   # return name of actor and grazing speed
   return 'Piggy', 0.75

def get_red():
   """ create a red (hostile) actor """
   # return name of actor, movement speed
   return 'Zombie-1', 1

def get_player():
   # name of player sprite (must exist in actors/ directory)
   return 'Soldier-2'
