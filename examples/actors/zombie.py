# A Customizable Style Maze Game
# Don't Edit This File
WIDTH = 31
HEIGHT = 19
TITLE = 'Making Bacon with Levels'


class BaconLevel(Level):
   plugins = import_plugin('zombie_plugins.py')

   def __init__(self, targets=1, level=1, total_hits=0, duration=0, time_remaining=30):
      self.targets = targets
      self.level = level
      self.hits = 0
      self.total_hits = total_hits
      self.time_remaining = time_remaining
      self.duration = duration

   def hit(self):
      self.hits += 1
      self.total_hits += 1
      score(self.total_hits)

   def get_duration(self):
      return score(pos=LOWER_RIGHT)

   def setup(self):
      """ setup the level """


      # PLAYER
      player = actor(self.plugins.get_player(), (1, HEIGHT-2), tag='player', abortable=True)
      player.speed(5).keys(precondition=player_physics)

      # TARGETS
      self.plugins.create_targets(self.targets)

      # SCORE BOARD
      score(self.total_hits, color=WHITE, method=VALUE, prefix='Kills: ')
      score(self.level, pos=UPPER_RIGHT, color=WHITE, method=VALUE, prefix='Level: ')
      stopwatch(color=WHITE, value=self.duration)

      # KEYBOARD EVENTS
      keydown('space', partial(self.plugins.shoot, self, player))
      keydown('1', partial(self.plugins.punch, self, player))
      keydown('2', partial(self.plugins.throw, self, player))
      keydown('r', reset)

      # MAZE and BACKGROUND
      self.plugins.setup(player, self.level)

   def completed(self):
       """ level is complete when all targets have been destroyed """
       if self.hits == self.targets:
           return True
       else:
           return False

   def next(self):
       """ load the next level """
       return BaconLevel(self.targets+1, level=self.level+1,
                         total_hits=self.total_hits, duration=score(pos=LOWER_RIGHT))

level(BaconLevel(1))
