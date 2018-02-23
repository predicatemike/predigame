# A Customizable Maze Game
# Don't Edit This File
WIDTH = 31
HEIGHT = 19
TITLE = 'Zombie Madness'
current_level = None

def invoke(function, default, **kwargs):
   if function in globals():
      return globals()[function](**kwargs)
   else:
      return globals()[default](**kwargs)

def is_moving(a):
   return a.action != IDLE

def monitor(a, callback):
   if not is_moving(a):
      callback()

def arrive_destination(dest_sprite, target):
   if target.tag == 'blue':
      target.destroy()
      current_level.blue_arrived += 1

def create_blue_destination():
   return 'pigpen'


def create_blue(plugins):
   """ create a blue (friendly) actor """
   actor_name, speed = plugins.get_blue()
   blue = actor(actor_name, (1,1), tag='blue').speed(speed)
   cb = partial(track_astar, blue, ['destination'], pabort=0.25)
   callback(cb, 0.25)
   callback(partial(monitor, blue, cb), 0.5, repeat=FOREVER)

def create_red(plugins):
   """ create a red (hostile) actor """
   actor_name, speed = plugins.get_red()
   red = actor(actor_name, (WIDTH-2,1), tag='red').speed(speed)
   cb = partial(track_astar, red, ['blue', 'player'], pabort=0.25)
   callback(cb, 0.25)
   callback(partial(monitor, red, cb), 0.5, repeat=FOREVER)


def red_attack(red, target):
   if target.tag == 'red':
      return
   if target.tag == 'blue' or target.tag == 'player':
      red.stop()
      red.act(ATTACK, 1)
      target.kill()

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

      if len(get('destination')) == 0:
         text("DESTINATION DESTROYED! GAME OVER")
         gameover()

      if self.blue_arrived == self.level or len(get('red')) == 0:
        return True

      if len(get('blue')) == 0 or len(get('player')) == 0:
         text('GAME OVER')
         gameover()

   def next(self):
       """ load the next level """
       return ZombieLevel(self.targets+1, level=self.level+1,
                          duration=score(pos=LOWER_RIGHT))

level(ZombieLevel(1))
