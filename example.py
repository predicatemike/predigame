from predigame import *

grid() # draw the coordinate grid

shape().float().speed(20) # a simple and likely shape use case
img('kenny').move_keys() # a simple and likely image use case

shape(RECT, CYAN, (6, 6), (2, 2), outline = 10).move_keys('d', 'a', 'w', 's').speed(10) # create a shape using all possible parameters
