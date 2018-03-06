# A Customizable Maze Game
# Don't Edit This File
WIDTH = 31
HEIGHT = 19
TITLE = 'Zombie Madness'
current_level = None
from types import MethodType

def invoke(plugins, function, default, **kwargs):
   if function in plugins.__dict__:
      return plugins.__dict__[function](**kwargs)
   else:
      return globals()[default](**kwargs)

def monitor(a, cb):
   if a.action.startswith(IDLE):
      cb()
   if not a.action.startswith(DIE):
      callback(partial(monitor, a, cb), 0.75)

def arrive_destination(dest_sprite, target):
   if target.tag == 'blue':
      target.destroy()
      current_level.blue_safe += 1

def default_blue_destination():
   return 'pigpen'

def red_attack(red, target):
   if target.tag == 'red':
      return
   if target.tag == 'blue' or target.tag == 'player':
      if target.tag == 'blue' and target.health > 0:
         current_level.blue_killed += 1
      red.stop()
      red.act(ATTACK, 1)
      callback(partial(red.act, IDLE_FRONT, FOREVER), 1)
      target.kill()

def red_murder(self):
    if self.health > 0:
       current_level.red_killed += 1
    Actor.kill(self)

def update_status(player):
    score("{:3d} | {:3d}".format(int(player.energy), int(player.health)), color=WHITE, pos=LOWER_LEFT, method=VALUE)

class ZombieLevel(Level):
   plugins = import_plugin('zombie_plugins.py')
   def __init__(self, targets=1, level=1, duration=0, time_remaining=30):
      self.targets = targets
      self.level = level
      self.time_remaining = time_remaining
      self.duration = duration
      self.blue_safe = 0
      self.blue_spawned = 0
      self.blue_killed = 0
      self.red_spawned = 0
      self.red_killed = 0
      self.destination = None
      self.player = None
      global current_level
      current_level = self

   def get_duration(self):
      return score(pos=LOWER_RIGHT)

   def create_blue(self):
      """ create a blue (friendly) actor """
      self.blue_spawned += 1
      atts = self.plugins.get_blue()
      blue = actor(atts[0], (1,1), tag='blue').speed(atts[1])
      self.destination.collides(blue, arrive_destination)
      if len(atts) == 3: blue.defend = atts[2]
      # callbacks
      for o in get('red'):
         o.collides(blue, red_attack)

      # movements
      cb = partial(track_astar, blue, ['destination'], pabort=0.1)
      callback(cb, 0.1)
      callback(partial(monitor, blue, cb), 0.75)

   def create_red(self):
      """ create a red (hostile) actor """
      self.red_spawned += 1
      actor_name, speed = self.plugins.get_red()
      red = actor(actor_name, (WIDTH-2,1), tag='red').speed(speed)
      red.old_kill = MethodType(red.kill, red)
      red.kill = MethodType(red_murder, red)
      # callbacks
      for o in get('blue'):
         red.collides(o, red_attack)
      for o in get('player'):
         red.collides(o, red_attack)

      # movements
      cb = partial(track_astar, red, ['blue', 'player'], pabort=0.1)
      callback(cb, 0.1)
      callback(partial(monitor, red, cb), 0.75)

   def setup(self):
      """ setup the level """

      # PLAYER
      self.player = actor(self.plugins.get_player(), (1, HEIGHT-2), tag='player', abortable=True)
      self.player.speed(5).keys(precondition=player_physics)

      # DESTINATION
      self.destination = image(invoke(self.plugins, "blue_destination", "default_blue_destination"), pos=(WIDTH-2, HEIGHT-2), size=1, tag='destination')

      # KEYBOARD EVENTS
      keydown('r', reset)

      # USER DEFINED STUFF
      self.plugins.setup(self.player, self)

      # LOAD IN SAVED STATE
      load_state(self.player, 'player.pg')

      # FRIENDLIES
      for i in range(self.targets):
         self.create_blue()

      # HOSTILES
      for i in range(self.targets):
         self.create_red()

      # SCORE BOARD
      score(self.level, pos=UPPER_RIGHT, color=WHITE, method=VALUE, prefix='Level: ')

      callback(partial(update_status, self.player), wait=1, repeat=FOREVER)

   def completed(self):
      #print("RS:{},RK:{},BS:{},BK:{},BF:{}".format(self.red_spawned, self.red_killed, self.blue_spawned, self.blue_killed, self.blue_safe))
      if len(get('destination')) == 0:
         text("DESTINATION DESTROYED! GAME OVER")
         gameover()
      elif (self.blue_safe == 0 and len(get('blue')) == 0) or len(get('player')) == 0:
         text('GAME OVER')
         gameover()
      elif len(get('blue')) == 0 or len(get('red')) == 0:
         save_state(self.player, 'player.pg')
         return True
      else:
         return False

   def next(self):
       """ load the next level """
       if randint(1, 10) == 4:
          return WalkAcrossLevel(self.targets+1, level=self.level+1,
                                 duration=score(pos=LOWER_RIGHT))
       else:
          return ZombieLevel(self.targets+1, level=self.level+1,
                             duration=score(pos=LOWER_RIGHT))

class WalkAcrossLevel(Level):
   plugins = import_plugin('zombie_plugins.py')

   def __init__(self, targets=1, level=1, duration=0, time_remaining=30):
      self.level = level
      self.targets = targets
      self.duration = duration
      global current_level
      current_level = self


   def setup(self):
      """ setup the level """

      # PLAYER
      player = actor(self.plugins.get_player(), (1, HEIGHT-2), tag='player', abortable=True)
      player.speed(5).keys(precondition=player_physics)

      # SCORE BOARD
      score(self.level, pos=UPPER_RIGHT, color=BLACK, method=VALUE, prefix='Level: ')

      txt = text("TIME TO DIE!!")
      callback(txt.destroy, 4)

      # HOSTILE
      actor_name, speed = self.plugins.get_red()
      red = actor(actor_name, (WIDTH+15,5), tag='red', size=15).speed(8)
      red.collides(sprites(), red_attack)
      points = [(p, 5) for p in range(WIDTH+15, -15, -2)]
      red.move_to(*points, callback=red.destroy)

      keydown('r', reset)

   def completed(self):

      if len(get('player')) == 0:
         text('GAME OVER')
         gameover()
      elif len(get('red')) == 0:
         print('no red')
         return True

   def next(self):
       """ load the next level """
       return ZombieLevel(targets=self.targets+1, level=self.level+1,
                          duration=score(pos=LOWER_RIGHT))

level(ZombieLevel(1))
