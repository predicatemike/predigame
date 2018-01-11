WIDTH = 30
HEIGHT = 20
TITLE = 'Sprites Demo'

# create sprites and position them
# shapes and images

# show effects all in a single window

# document the process

def on_click(s):
	image('redsplat', s.event_pos, 1).fade(15)

p1 = image('kenny', (15,10), 10)
p1.clicked(on_click)
