WIDTH = 31
HEIGHT = 19
TITLE = 'Making Bacon with Levels'

def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj and obj.tag == 'wall':
        return False
    elif not visible(pos):
        return False
    else:
        return True

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

def timer(level):
    text("You survived " + str(level.get_duration()) + " seconds.")
    callback(gameover, 2)

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

    def get_duration():
        return score(pos=LOWER_RIGHT)

    def setup(self):
        """ setup the level """
        # MAZE and BACKGROUND
        background('grass')
        maze(callback=partial(image, 'stone'))

        # PLAYER
        player = actor('Soldier-2', (1, HEIGHT-2), tag='player', abortable=True)
        player.speed(5).keys(precondition=evaluate)

        # TARGETS
        create_targets(self.targets)

        # SCORE BOARD
        score(self.total_hits, color=WHITE, method=VALUE, prefix='Kills: ')
        score(pos=LOWER_LEFT, color=WHITE, value=self.time_remaining, method=TIMER,
              step=-1, goal=0, callback=partial(timer, self), prefix='Time Remaining: ')
        score(pos=LOWER_RIGHT, color=WHITE, value=self.duration, method=TIMER,
              step=1, goal=1000, prefix='Duration: ')
        score(self.level, pos=UPPER_RIGHT, color=WHITE, method=VALUE, prefix='Level: ')

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
