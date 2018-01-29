WIDTH = 30
HEIGHT = 20
TITLE = 'Scoring Demo'

# default scoring box (upper left corner)
score()

def timer():
	text('GAME OVER')
	gameover()

# some other scoring options
score(pos=UPPER_RIGHT, method=VALUE)
score(pos=LOWER_LEFT, method=TIMER, step=1, goal=10, prefix='Duration:')
score(30, pos=LOWER_RIGHT, method=TIMER, step=-1, callback=timer, prefix='Time Left:')
def pop(s):
	s.destroy()
	score(1)
	score(100, pos=UPPER_RIGHT)
	if score() % 3 == 0:
		reset_score(pos=UPPER_RIGHT, method=VALUE)

def show():
	shape(CIRCLE, RED).clicked(pop)
	callback(show, rand(0,2))
callback(show, 0.5)


keydown('r', reset)
