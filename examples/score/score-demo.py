# a pretty silly game that showcases all the different ways to keep score

WIDTH = 30
HEIGHT = 20
TITLE = 'Scoring Demo'

# default scoring box (upper left corner)
score(color=WHITE)

# a callback used for a timer
def timer():
	text('GAME OVER')
	gameover()

# place this scoreboard in the upper right corner and just show the value
# this means the scoreboard will not accumulate the score
score(pos=UPPER_RIGHT, method=VALUE)

# position this scoreboard in the bottom left corner
# run as a timer from 0 to 10 (the goal), in increments of 1
# add a prefix "Duration:"
# since there is no callback registered, the counter will simply when the goal is obtained
score(pos=LOWER_LEFT, method=TIMER, step=1, goal=10, prefix='Duration:')

# position this scoreboard in the bottom right corner
# run as a timer from 30 to 0 (step is -1 so the counter "steps down")
# when the goal of 0 is reached, execute the timer callback function
score(30, pos=LOWER_RIGHT, method=TIMER, step=-1, goal=0, callback=timer, prefix='Time Left:')

# a simple sprite callback for popping circles and executing the score Options
# every three pops will reset the scoreboard in the upper right corner
def pop(s):
	s.destroy()
	score(1)
	score(100, pos=UPPER_RIGHT)
	if score() % 3 == 0:
		reset_score(pos=UPPER_RIGHT, method=VALUE)

# silly circle drawer
def show():
	shape(CIRCLE, RED).clicked(pop)
	callback(show, rand(0,2))
callback(show, 0.5)

# register a 'r' keydown method to reset
keydown('r', reset)
