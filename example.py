HEIGHT = 8 # optional window height constant
WIDTH = 10 # optional window width constant
TITLE = 'PREDIGAME' # optional title constant
SIZE = 100 # optional grid square size in pixels

grid() # draw the coordinate grid

shape().float().speed(2) # a simple and likely shape use case
img().keys() # a simple and likely image use case

shape(RECT, CYAN, (6, 6), (2, 2), outline = 10).keys('d', 'a', 'w', 's', spaces = 2).speed(10) # create a shape using all possible parameters
