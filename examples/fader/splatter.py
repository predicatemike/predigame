#splats should be in the center
WIDTH = 30
HEIGHT = 20
TITLE = 'Image Splatter Test'

grid()

def on_click(s):
	image('redsplat', s.event_pos, 1).fade(15)

p1 = image('kenny', (15,10), 10)
p1.clicked(on_click)
