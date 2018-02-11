# This is a simple game with two levels
WIDTH = 30
HEIGHT = 20
TITLE = 'Simple Two Level Example'

current_level = None

def timer():
    text("You survived " + str(current_level.get_duration()) + " seconds.")
    callback(gameover, 2)

def pop(s):
    s.destroy()
    current_level.hit()

class PopLevel2(Level):
    def __init__(self, duration):
        self.hits = 0
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

        # create two targets
        shape(CIRCLE).clicked(pop)
        shape(CIRCLE).clicked(pop)

        # SCORE BOARD
        score(0, color=BLACK, method=VALUE, prefix='Hits: ')
        score(pos=LOWER_RIGHT, color=BLACK, value=self.duration, method=TIMER,
              step=1, goal=1000, prefix='Duration: ')

        # KEYBOARD EVENTS
        keydown('r', reset)

    def completed(self):
        """ level is complete when all targets have been destroyed """
        if self.hits == 2:
            return True
        else:
            return False

    def next(self):
        """ end the game.. there is no next level """
        text("YOU SOLVED ALL LEVELS!")
        callback(gameover, 0.1)
        return None

class PopLevel1(Level):
    def __init__(self, duration):
        self.hits = 0
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

        # create one target
        shape(CIRCLE).clicked(pop)

        # SCORE BOARD
        score(0, color=BLACK, method=VALUE, prefix='Hits: ')
        score(pos=LOWER_RIGHT, color=BLACK, value=self.duration, method=TIMER,
              step=1, goal=1000, prefix='Duration: ')

        # KEYBOARD EVENTS
        keydown('r', reset)

    def completed(self):
        """ level is complete when all targets have been destroyed """
        if self.hits == 1:
            return True
        else:
            return False

    def next(self):
        """ load the next level """
        return PopLevel2(duration=score(pos=LOWER_RIGHT))

level(PopLevel1(1))
