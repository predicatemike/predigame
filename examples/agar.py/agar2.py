WIDTH = 30
HEIGHT = 20
TITLE = 'Agar2.py'

p1 = image('kenny').scale(1.5).speed(10).keys()
p2 = image('kurt').scale(1.5).speed(10).keys('d', 'a', 'w', 's').flip()

def win(p1, p2):
    if p1.size > p2.size:
        p1.size += p2.size
        p2.destroy()

    if p2.size > p1.size:
        p2.size += p1.size
        p1.destroy()

p1.collides(p2, win)

def eat(p, f):
    p.scale(1.05)
    sound('eat')
    f.destroy()

for i in range(25):
    f = image('pizza').float(0.5).speed(1)
    p1.collides(f, eat)
    p2.collides(f, eat)

keydown('r', reset)
