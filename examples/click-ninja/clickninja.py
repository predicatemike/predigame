WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def explode(s):
    text('You Survived %s seconds' % time(), MAROON)
    pause()

def hurt(s):
    s.destroy()
    score(-20)
    if score() < 0:
        text('You Survived %s' % time(), MAROON)
        pause()

def point(s):
    s.destroy()
    score(5)

def spawn():
    target = choice(['bomb', 'bananas', 'cherries', 'olives'])
    if target == 'bomb':
        s = image(target, (rand(0, WIDTH - 2), HEIGHT + 1), 2)
        s.speed(11).clicked(explode)
        s.move_to((s.x + 1, 1), (s.x + 1, HEIGHT + 1), callback = s.destroy)
    elif target in ['bananas', 'cherries', 'olives']:
        s = image(target, (rand(0, WIDTH - 2), HEIGHT + 1), 2)
        s.speed(11).clicked(point)
        s.move_to((s.x + 1, 1), (s.x + 1, HEIGHT + 1), callback = lambda: hurt(s))
    callback(spawn, rand(0.5, 1))

score(color = PURPLE)

callback(spawn, rand(0.5, 1))
keydown('r', reset)
