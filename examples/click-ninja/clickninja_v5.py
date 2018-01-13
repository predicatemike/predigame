WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s):
    if s.name == 'taco':
       score(50)
    else:
       score(5)
    s.destroy()

def failure(s):
    score(-20)
    if s.name == 'bomb' or score() < 0:
        text('You Survived %s seconds' % time(), MAROON)
        gameover()

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

    arc = rand_arc()

    s = image(target, arc[0], size)
    if target == 'bomb':
       s.speed(speed).clicked(failure)
       s.move_to(arc[1], arc[2], callback = s.destroy)
    elif target == 'taco':
       s.speed(5).clicked(destroy)
       s.move_to((-10, -2), (-5, HEIGHT/2), (WIDTH+1, HEIGHT/2), callback = s.destroy)
    else:
       s.speed(speed).clicked(destroy)    
       s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(spawn, 1)

score(color = PURPLE)
callback(spawn, rand(0.1, 3))
keydown('r', reset)  