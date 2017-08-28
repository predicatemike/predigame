WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'

p = shape(CIRCLE, BLUE, (1, 1)).keys()

def win(b, p):
    text('YOU WIN', BLUE)
    pause()

def end(b, p):
    p.destroy()
    text('GAME OVER', BLACK)

for y in range(HEIGHT):
    for x in range(WIDTH):
        if (x, y) == (1, 1) or (x, y) == (28, 16):
            continue
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y)).collides(p, end)

shape(RECT, GREEN, (28, 16)).collides(p, win)

keydown('r', reset)
