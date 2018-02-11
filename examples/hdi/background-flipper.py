WIDTH = 20
HEIGHT = 10
TITLE = 'Background Flipper'

backgrounds = ['grass', 'ville', None, (255, 0, 0), (0, 0, 255), (0, 0, 0)]
BACKGROUND = backgrounds[0]

def flip():
    background(choice(backgrounds))
    callback(flip, 0.25)
callback(flip, 3)
