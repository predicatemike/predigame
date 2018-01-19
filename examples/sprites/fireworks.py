WIDTH = 30
HEIGHT = 20
TITLE = 'Fireworks!'
BACKGROUND = (0,0,0)

def explode(s):
	s.destroy()
	num = randint(1, 5)
	img = image('fireworks-'+str(num), s.pos, size=0.5)
	img.pulse(time=4, size=10).destruct(rand(0.1,4))

def launch():
	sound('fireworks')
	p = rand_pos(x_padding=5, y_padding=10)
	s = shape(CIRCLE, YELLOW, (p[0], WIDTH-5), size=0.1)
	s.speed(15).move_to(p, callback=lambda: explode(s))
	callback(launch, rand(0, 3))

callback(launch, 1)	


