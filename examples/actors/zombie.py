# A Customizable Maze Game
# Don't Edit This File
WIDTH = 31
HEIGHT = 19
TITLE = 'Zombie Madness'
current_level = None

def arrive_destination(dest_sprite, target):
   if target.tag == 'blue':
      target.destroy()
      current_level.blue_arrived += 1

def create_blue_destination():
   return 'pigpen'

def cb_find_destination(p):
   callback(partial(track_astar, p, ['destination'], callback=partial(cb_find_destination,p), pabort=0.15), 1)

def create_blue(plugins):
   """ create a blue (friendly) actor """
   actor_name, speed = plugins.get_blue()
   blue = actor(actor_name, (1,1), tag='blue').speed(speed)
   cb_find_destination(blue)

def cb_find_blue(r):
   callback(partial(track_astar, r, ['blue', 'player'], callback=partial(cb_find_blue,r), pabort=0.15), 1)

def create_red(plugins):
   """ create a red (hostile) actor """
   actor_name, speed = plugins.get_red()
   r = actor(actor_name, (WIDTH-1,1), tag='red').speed(speed)
   cb_find_blue(r)

def red_attack(red, target):
   if target.tag == 'red':
      return
   if target.tag == 'blue' or target.tag == 'player':
      red.stop()
      red.act(ATTACK, 1)
      target.kill()
      cb_find_blue(red)

class ZombieLevel(Level):
   plugins = import_plugin('zombie_plugins.py')

   def __init__(self, targets=1, level=1, duration=0, time_remaining=30):
      self.targets = targets
      self.level = level
      self.time_remaining = time_remaining
      self.duration = duration
      self.blue_arrived = 0
      global current_level
      current_level = self

   def get_duration(self):
      return score(pos=LOWER_RIGHT)

   def setup(self):
      """ setup the level """

      # PLAYER
      player = actor(self.plugins.get_player(), (1, HEIGHT-2), tag='player', abortable=True)
      player.speed(5).keys(precondition=player_physics)

      # KEYBOARD EVENTS
      keydown('space', partial(self.plugins.shoot, self, player))
      keydown('1', partial(self.plugins.punch, self, player))
      keydown('2', partial(self.plugins.throw, self, player))
      keydown('r', reset)

      # USER DEFINED STUFF
      self.plugins.setup(player, self.level)

      # FRIENDLIES
      for i in range(self.targets):
         create_blue(self.plugins)

      # HOSTILES
      for i in range(self.targets):
         create_red(self.plugins)

      # make red attack blue and player
      for r in get('red'):
         r.collides(sprites(), red_attack)

      # create a destination
      img = image(create_blue_destination(), pos=(WIDTH-2, HEIGHT-2), size=1, tag='destination')
      img.collides(sprites(), arrive_destination)

      # SCORE BOARD
      score(self.level, pos=UPPER_RIGHT, color=WHITE, method=VALUE, prefix='Level: ')
      #stopwatch(color=WHITE, value=self.duration)

   def completed(self):
      """ level is complete when all reds have been destroyed and at least one blue is surviving """

      if self.blue_arrived == self.level and len(get('red')) == 0:
        return True

      if len(get('blue')) == 0 or len(get('player')) == 0:
         text('GAME OVER')
         gameover()



   def next(self):
       """ load the next level """
       return ZombieLevel(self.targets+1, level=self.level+1,
                          duration=score(pos=LOWER_RIGHT))

level(ZombieLevel(1))
