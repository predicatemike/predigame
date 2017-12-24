
def pop(s):
    s.scale(1.1)
    if s.width > 3:
        s.destroy()
        shapes.remove(s)

        if len(shapes) == 0:
            text('You won in %s seconds' % time())
            pause()

shapes = []

for i in range(5):
     s = shape(CIRCLE).bouncy()
     s.clicked(pop, 1)
     shapes.append(s)

keydown('r', reset)
