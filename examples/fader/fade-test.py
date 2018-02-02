WIDTH = 30
HEIGHT = 20
TITLE = 'Image Fadeout Test'

def on_click(s):
	s.fade(5)

p1 = image('kenny', (10,5), size=10).bouncy()
p1.clicked(on_click)

p2 = shape(CIRCLE, size=2).bouncy()
p2.clicked(on_click)
