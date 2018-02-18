WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja (Leveled Edition)'
current_level = None
def destroy(s):
    sound('swoosh')
    current_level.hit()
    if s.name == 'taco':
       score(50)
    else:
       score(5)

    # draw a splatting image at the center position of the image
    image('redsplat', center=s.event_pos, size=2).fade(1.0)

    s.fade(0.25)

def failure(s):
    score(-20)
    if s.name == 'bomb':
        s.destroy()
        image('explode', center=s.center, size=10).pulse(0.05)

    if s.name == 'bomb' or score() < 0:
        sound('scream')
        text('You Survived %s seconds' % current_level.get_duration(), MAROON)
        callback(gameover, 0.01)

def spawn(min_size=4, max_size=4, min_speed=1, max_speed=1, min_rate=1, max_rate=1):
    size = rand(min_size, max_size)
    speed = rand(min_speed,max_speed)

    target = choice(['bananas', 'cherries',
                     'olives', 'ham', 'hotdog',
                     'fries','icee', 'pizza'])

    if randint(1, 4) == 2:
        target = 'bomb'
    if randint(1, 10) == 5:
        target = 'taco'

    sound('launch')

    arc = rand_arc()

    s = image(target, arc[0], size=size)
    if target == 'bomb':
       s.speed(speed).spin(1).clicked(failure)
       s.move_to(arc[1], arc[2], callback = s.destroy)
    elif target == 'taco':
       s.speed(5).spin().clicked(destroy)
       s.move_to((-10, -2), (-5, HEIGHT/2), (WIDTH+1, HEIGHT/2), callback = s.destroy)
    else:
       s.speed(speed).clicked(destroy)
       s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(partial(spawn, min_speed=min_speed, max_speed=max_speed,
                     min_rate=min_rate, max_rate=max_rate,
                     min_size=min_size, max_size=max_size), rand(min_rate, max_rate))

class NinjaLevel(Level):
    def __init__(self, level=1, total_hits=0, duration=0, min_size=4, max_size=4, min_speed=1, max_speed=1, min_rate=3, max_rate=3):
        self.level = level
        self.min_size = min_size
        if self.min_size < 0.1:
            self.min_size = 0.1

        self.max_size = max_size
        self.min_speed = min_speed
        if self.min_speed < 0.1:
            self.min_speed = 0.1

        self.max_speed = max_speed

        self.min_rate = min_rate
        if self.min_rate < 0:
            self.min_rate = 0

        self.max_rate = max_rate
        self.hits = 0
        self.total_hits = total_hits
        self.duration = duration

    def hit(self):
        self.hits += 1
        self.total_hits += 1
        score(self.total_hits, pos=LOWER_LEFT)

    def get_duration(self):
        return score(pos=LOWER_RIGHT)

    def setup(self):
        """ setup the level """
        global current_level
        current_level = self

        # BACKGROUND (randomly selected)
        background()

        # SCORE BOARD
        score(0, prefix='Score: ')
        score(self.total_hits, pos=LOWER_LEFT, color=BLACK, method=VALUE, prefix='Hits: ')
        score(pos=LOWER_RIGHT, color=BLACK, value=self.duration, method=TIMER,
              step=1, goal=1000, prefix='Duration: ')
        score(self.level, pos=UPPER_RIGHT, color=BLACK, method=VALUE, prefix='Level: ')

        # START LEVEL
        callback(partial(spawn, min_speed=self.min_speed, max_speed=self.max_speed,
                         min_rate=self.min_rate, max_rate=self.max_rate,
                         min_size=self.min_size, max_size=self.max_size), 1)

        # KEYBOARD EVENTS
        keydown('r', reset)

    def completed(self):
        """ 10 hits are required to complete a level """
        if self.hits == 10:
            return True
        else:
            return False

    def next(self):
        """ load the next level """
        return NinjaLevel(level=self.level+1, total_hits=self.total_hits,
                          duration=score(pos=LOWER_RIGHT),
                          min_speed=self.min_speed-0.1, max_speed=self.max_speed+0.5,
                          min_rate=self.min_rate-0.5, max_rate=self.max_rate-0.1,
                          min_size=self.min_size-0.5, max_size=self.max_size)

level(NinjaLevel(1))
