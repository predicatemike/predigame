HEIGHT = 8 # optional window height constant
WIDTH = 10 # optional window width constant
TITLE = 'PREDIGAME' # optional title constant
SIZE = 100 # optional grid square size in pixels

grid() # draw the coordinate grid

shape().float().speed(1) # a simple and likely shape use case
img().move_keys() # a simple and likely image use case

shape(RECT, CYAN, (6, 6), (2, 2), outline = 10).move_keys('d', 'a', 'w', 's').speed(10) # create a shape using all possible parameters
