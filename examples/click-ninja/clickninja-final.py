WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'
BACKGROUND = 'board'

def destroy(s):
    sound('swoosh')
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
        text('You Survived %s seconds' % time(), MAROON)
        callback(gameover, 0.01)

def spawn():
    speed = randint(2, 10)
    size = randint(1,4)

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

    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, 1)
keydown('r', reset)
