WIDTH = 30
HEIGHT = 20
TITLE = 'Image Fadeout Test'
from time import sleep

percentage = 0

def on_click(s):
	global percentage
	percentage = percentage + 5
	s.pixelate(percentage)
	print(percentage)

p1 = image('kenny', (10,5), 10).clicked(on_click)
