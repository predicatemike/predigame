WIDTH = 20
HEIGHT = 20
TITLE = 'Background Flipper'

backgrounds = ['grass', 'ville', None, (255, 0, 0), (0, 0, 255), (0, 0, 0)]
BACKGROUND = backgrounds[0]

img = image('fries', pos=(1,1), size=10000)

def inflate():
    img.scale(1.1)
    print(img.size)
    callback(inflate, 0.25)
callback(inflate, 1)
