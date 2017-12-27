#splats should be in the center
WIDTH = 30
HEIGHT = 20
TITLE = 'Animated Actors'

p1 = actor('1', (15,10), 5)

keydown('i', lambda: p1.act(IDLE, FOREVER))
keydown('w', lambda: p1.act(WALK, 3))  
keydown('r', lambda: p1.act(RUN, 3))
keydown('a', lambda: p1.act(ATTACK, 1))
keydown('s', lambda: p1.act(ATTACK1, 1))
keydown('d', lambda: p1.act(ATTACK2, 1))
keydown('f', lambda: p1.act(ATTACK3, 1))
keydown('h', lambda: p1.act(HURT, 1))
keydown('j', lambda: p1.act(JUMP, 1))

