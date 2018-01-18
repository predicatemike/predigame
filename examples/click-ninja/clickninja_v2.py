WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s):
    score(1)
    s.destroy()

def failure(s):
    text('You Survived %s seconds' % time(), MAROON)
    gameover()

def spawn():

    speed = randint(2, 10)
    size = randint(1,4)

    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    arc = rand_arc()

    s = image(target, arc[0], size)
    s.speed(speed).clicked(destroy) 
    s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, 1)
keydown('r', reset)  