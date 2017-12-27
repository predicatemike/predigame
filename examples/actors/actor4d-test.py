#splats should be in the center
WIDTH = 30
HEIGHT = 20
TITLE = 'Animated Actors'

p1 = actor('Zombie-2', (15,10), 5, 4)


keydown('q', lambda: p1.act(ATTACK_BACK, FOREVER))
keydown('w', lambda: p1.act(ATTACK_FRONT, FOREVER))
keydown('e', lambda: p1.act(ATTACK_LEFT, FOREVER))
keydown('r', lambda: p1.act(ATTACK_RIGHT, FOREVER))

keydown('a', lambda: p1.act(DIE_BACK, FOREVER))
keydown('s', lambda: p1.act(DIE_FRONT, FOREVER))
keydown('d', lambda: p1.act(DIE_LEFT, FOREVER))
keydown('f', lambda: p1.act(DIE_RIGHT, FOREVER))

keydown('z', lambda: p1.act(IDLE_BACK, FOREVER))
keydown('x', lambda: p1.act(IDLE_FRONT, FOREVER))
keydown('c', lambda: p1.act(IDLE_LEFT, FOREVER))
keydown('v', lambda: p1.act(IDLE_RIGHT, FOREVER))

keydown('1', lambda: p1.act(WALK_BACK, FOREVER))
keydown('2', lambda: p1.act(WALK_FRONT, FOREVER))
keydown('3', lambda: p1.act(WALK_LEFT, FOREVER))
keydown('4', lambda: p1.act(WALK_RIGHT, FOREVER))
