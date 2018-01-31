import glob, json, os
import pathlib, contextlib

WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE EDITOR (click to draw)'

print('The Maze Editor')
print('Left Click to draw / Right Click to undo a selection')
print('p - preview saved mazes (hit again for next)')
print('d - delete the current saved maze')
print('s - save the current maze in a new file')
print('r - reset and clear screen')

grid()

maze_file = 0
label = None

# mark a shape red (left click)
# reset a selected shape (right click)
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
    max_num = 1
    for a in get_mazes():
        num = int(a.split('/')[-1].split('.')[0])
        if num > max_num:
            max_num = num

    return 'mazes/' + str(max_num + 1) + '.json'

def preview():
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

    for cell in cells:
        shape(RECT, RED, (cell[0], cell[1]), tag='cell').clicked(mark, button=3)
    
    if label is not None:
        label.destroy()
    label = text('Maze ' + mazes[maze_file], BLACK)

    maze_file += 1

def delete():
    global maze_file
    # only run in preview mode
    if label is not None:
        mazes = get_mazes()
        print(maze_file)
        if maze_file <= len(mazes):
            os.remove(mazes[maze_file-1])
            reset()

def save():
    try:
       pathlib.Path('mazes').mkdir(parents=True)
    except:
       print('mazes directory already exists')
    objs = []
    for s in sprites():
        if s.tag == 'cell':
            objs.append(s.pos)
    json.dump(objs, open(get_next_file(), 'w'))
    reset()

keydown('p', preview)
keydown('d', delete)
keydown('s', save)
keydown('r', reset)
