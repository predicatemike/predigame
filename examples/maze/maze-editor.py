import glob
import json
import pathlib
 
WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE EDITOR (click to draw)'

grid()

maze_file = 0
label = None

# mark a shape red
def mark(s):
    s.destroy()
    print(s.tag)
    if s.tag is '':
        # right mouse button is undo
        shape(RECT, RED, s.pos, tag='cell').clicked(mark, button=3)
    else:
        shape(RECT, WHITE, s.pos).clicked(mark)

def clear():
    global label
    label = None
    for i in list(sprites()):
        i.destroy()

    # paint every cell white
    for y in range(HEIGHT):
       for x in range(WIDTH):
          s = shape(RECT, WHITE, (x,y)).clicked(mark)
clear()


def get_mazes():
    return glob.glob('./mazes/*.json')

def get_next_file():
    return 'mazes/' + str(len(get_mazes()) + 1) + '.json'

def next_preview():
    global maze_file
    global label
    clear()
    mazes = get_mazes()

    if len(mazes) == 0:
        return

    if maze_file is None:
        maze_file = 0

    if maze_file >= len(mazes):
        maze_file = 0

    cells = json.load(open(mazes[maze_file], 'r'))

    if label is not None:
        label.destroy()
    label = text('Maze ' + mazes[maze_file], BLACK)

    for cell in cells:
        print(cell)
        shape(RECT, RED, (cell[0], cell[1]), tag='cell').clicked(mark, button=3)
    maze_file += 1


def start_preview():
    next_preview()


def save():
    pathlib.Path('mazes').mkdir(parents=True, exist_ok=True) 
    objs = []
    for s in sprites():
        if s.tag == 'cell':
            objs.append(s.pos)
    json.dump(objs, open(get_next_file(), 'w'))
    reset()

keydown('p', start_preview)
keydown('n', next_preview)
keydown('s', save)
keydown('r', reset)