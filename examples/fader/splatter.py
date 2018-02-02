#splats should be in the center
WIDTH = 30
HEIGHT = 20
TITLE = 'Image Splatter Test'

grid()

def on_click(s):
	print(s.event_pos)
	i= image('redsplat', center=s.event_pos, size=1).fade(3)
	print(i.pos)
p1 = image('kenny', center=(15,5), size=10)
p1.clicked(on_click)
