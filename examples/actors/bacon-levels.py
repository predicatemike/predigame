WIDTH = 31
HEIGHT = 19
TITLE = 'Making Bacon with Levels'

def shoot(level, player):
   player.act(SHOOT, loop=1)
   target = player.next_object()

   # if it's a target and that target is alive
   if target and target.tag == 'target' and target.health > 0:
      target.health = 0
      target.destruct(5)
      level.hit()

def create_targets(num):
   for x in range(num):
      pos = rand_pos()
      while at(pos) is not None:
         pos = rand_pos()

      piggy = actor('Piggy', pos, tag='target')
      piggy.wander(partial(graze, piggy), time=0.75)

class BaconLevel(Level):
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
      # MAZE and BACKGROUND
      background('grass')
      maze(callback=partial(image, 'stone'))

      # PLAYER
      player = actor('Soldier-2', (1, HEIGHT-2), tag='player', abortable=True)
      player.speed(5).keys(precondition=player_physics)

      # TARGETS
      create_targets(self.targets)

      # SCORE BOARD
      score(self.total_hits, color=WHITE, method=VALUE, prefix='Kills: ')
      score(self.level, pos=UPPER_RIGHT, color=WHITE, method=VALUE, prefix='Level: ')
      timer(color=WHITE, value=self.time_remaining)
      stopwatch(color=WHITE, value=self.duration)

      # KEYBOARD EVENTS
      keydown('space', partial(shoot, self, player))
      keydown('r', reset)

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
