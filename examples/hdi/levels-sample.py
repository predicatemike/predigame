# Create a basic game that demonstrates how to create levels
# In each level, the player has to pop all the circles in 10 seconds
# A new circle will be added for each level

WIDTH = 30
HEIGHT = 20
TITLE = 'Simple Levels Example'

current_level = None

def timer():
    text("You survived " + str(current_level.get_duration()) + " seconds.")
    callback(gameover, 2)

def pop(s):
    s.destroy()
    current_level.hit()

class PopLevel(Level):
    def __init__(self, level=1, duration=0):
        self.level = level
        self.hits = 0
        self.time_remaining = 10
        self.duration = duration

    def hit(self):
        self.hits += 1
        score(self.hits)

    def get_duration(self):
        return score(pos=LOWER_RIGHT)

    def setup(self):
        """ setup the level """

        # Hold a reference to this level
        global current_level
        current_level = self

        # TARGETS
        for x in range(self.level):
            shape(CIRCLE).clicked(pop)

        # SCORE BOARD
        score(0, color=BLACK, method=VALUE, prefix='Hits: ')
        score(pos=LOWER_LEFT, color=BLACK, value=self.time_remaining, method=TIMER,
              step=-1, goal=0, callback=timer, prefix='Time Remaining: ')
        score(pos=LOWER_RIGHT, color=BLACK, value=self.duration, method=TIMER,
              step=1, goal=1000, prefix='Duration: ')
        score(self.level, pos=UPPER_RIGHT, color=BLACK, method=VALUE, prefix='Level: ')

        # KEYBOARD EVENTS
        keydown('r', reset)

    def completed(self):
        """ level is complete when all targets have been destroyed """
        if self.hits == self.level:
            return True
        else:
            return False

    def next(self):
        """ load the next level """
        return PopLevel(level=self.level+1, duration=score(pos=LOWER_RIGHT))

level(PopLevel(1))
