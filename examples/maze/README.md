Drawing Mazes
===================
We can code a number of games with mazes. From Pacman to avoiding the zombie apocalypse, mazes are a fun and easy way to plant obstacles or walls.  The Predigame platform supports a number of maze options that we'll explore in this README. For those familiar with the Predigame Sprite, mazes are nothing more than a collection of sprites, normally all of the same type and size.

Let's explore how to code mazes!

Getting Started
----------
To get things started, we're going to create a basic Predigame canvas that we'll use to build the maze. The canvas will have a width of 30 grid cells and a height of 20 grid cells.

```python
WIDTH = 30
HEIGHT = 20
TITLE = 'MAZE'
```
Save your changes. Let's call the file `maze.py`.  Try running the game from the terminal using the `pigm` command (you'll want to run this command from the directory where you saved the file). 

    my_machine$ pigm maze.py

This program doesn't do much just yet. Just an empty window titled "MAZE" - that's missing the maze! Let's add that now.

# Random Mazes
The first type of maze we'll create is the computer generated randomized maze. The code below will iterate over every cell in the game and make a random decision to draw a maze. 

```python
# these two nested for loops iterate over
# every grid cell on the canvas
for y in range(HEIGHT):
    for x in range(WIDTH):
    	# don't create a block on the location of
    	# the player OR the location of the green cell
        if (x, y) == (0, 0) or (x, y) == (29, 16):
            continue
        # make a random decision to color the cell red
        # this number can be adjusted to make the cells
        # smaller or larger.
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y))
```
The line `rand(1, 3) > 2.5` represents the probability of drawing a maze. There is about a 16.6667% chance that a given cell will have a **RED** cell colored. Try adjusting the `2.5` to a larger (but less than 3) or smaller (but greater than 1) and see what happens.

You'll also notice that with the if condition:
```python
        if (x, y) == (0, 0) or (x, y) == (29, 16):
            continue
```
Will never consider placing a **RED** cell at position `(0, 0)` (top left corner) or `(29, 16)` (bottom right corner). This where we will put the player and a green destination block. 

Now that we can draw a random maze, lets add a player sprite at the top of the code, under the `TITLE` line.
```python
# create a sprite based on the "player" image
# position at the top left corner
# control the sprite with the arrow keys
# the speed of the sprite enables "graceful" 
# movement with the keyboard
p = image('player', (0, 0)).speed(5).keys()

# center the player on the 0,0 grid cell
p.move_to((0, 0))
```
Notice that the `p.move_to((0, 0))` seems a bit redundant given that we already placed the player sprite at position `(0, 0)`? Well, it is! By default the position provided to Predigame places the center of the sprite image at that position. The `move_to` places the sprite inside the grid cell.

Finally, to complete our simple game, let's add a **GREEN** destination block. We'll also add a callback to end the game when the player sprite collides with the destination block. Let's add this code to the bottom of the file.

```python
# a callback function for when the player reaches 
# the green destination
def win(b, p):
    text('YOU WIN', BLUE)
    gameover()
   
# draw a green destination cell on the bottom right
d = shape(RECT, GREEN, (WIDTH-1, HEIGHT-1), tag='destination')

# if the player reaches this cell, execute the 'win' callback
d.collides(p, win)

# register the 'r' key for resetting the game
keydown('r', reset)
```
For context, here is the complete code: 

```python
WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'

# create a sprite based on the "player" image
# position at the top left corner
# control the sprite with the arrow keys
# the speed of the sprite enables "graceful" 
# movement with the keyboard
p = image('player', (0, 0)).speed(5).keys()

# center the player on the 0,0 grid cell
p.move_to((0, 0))

# these two nested for loops iterate over
# every grid cell on the canvas
for y in range(HEIGHT):
    for x in range(WIDTH):
    	# don't create a block on the location of
    	# the player OR the location of the green cell
        if (x, y) == (0, 0) or (x, y) == (29, 16):
            continue
        # make a random decision to color the cell red
        # this number can be adjusted to make the cells
        # smaller or larger.
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y))

# a callback function for when the player reaches 
# the green destination
def win(b, p):
    text('YOU WIN', BLUE)
    gameover()
   
# draw a green destination cell on the bottom right
d = shape(RECT, GREEN, (WIDTH-1, HEIGHT-1), tag='destination')

# if the player reaches this cell, execute the 'win' callback
d.collides(p, win)

# register the 'r' key for resetting the game
keydown('r', reset)
```
Save the changes and try running the code:

    my_machine$ pigm maze.py

Notice that player sprite can walk through walls? That's a bit silly. We'll fix that in a few minutes. Can't reach the destination? Try hitting `r` to reset the game.

## Don't hit the walls!
Now let's modify the code to end the game if the player sprite bumps into a wall. It's a small insertion we can add to the end of the file.

```python
# a callback function for when the player runs into
# a red cell
def lose(b, p):
	if b.tag != 'destination':
		text('GAME OVER', BLACK)
		gameover()

# if the player 'collides' with any cell, execute the 'lose' callback
p.collides(sprites(), lose)
``` 
Save the changes and try running the code:

    my_machine$ pigm maze.py

## Wall Avoidance
In a real game, we don't want the player sprite to walk into walls. It's possible to check the destination of where the player is about to move prior to making the move. We'll call this a *precondition* - Predigame handles this as a callback function.

Add the following code to the type of your file, under the `TITLE` line:

```python
# a callback that keeps the player from running
# into walls. it's only acceptable to walk into
# an object marked as a "destination"
def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj:
        if obj.tag == 'destination':
            return True
        else:
            return False
    else:
        return True
```
This code calls the `at(pos)` function that returns any objects that are **at** a given location - the location the sprite is about to move to. If there is an object at the location **AND**  that object doesn't have the tag named `destination`, it must be a wall, so `evaluate` will return `False`, an indication it is not safe to complete the movement. In all other conditions - either nothing is there or something with the name `destination`, permit the move to complete.

Next we'll set the `evaluate` callback function and assign to execute on `keys()` function. Let's make a change to our player sprite:

```python
# create a sprite based on the "player" image
# position at the top left corner. control the 
# sprite with the arrow keys while checking a 
# precondition to make sure we don't walk into 
# walls. the speed of the sprite enables "graceful" 
# movement with the keyboard
p = image('player', (0, 0)).speed(5).keys(precondition=evaluate)
```
The code from the prior step can be removed since it won't be called anymore. For context, here's the complete file in case you git a little lost making changes in the right locations.

```python
WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE'

# a callback that keeps the player from running
# into walls. it's only acceptable to walk into
# an object marked as a "destination"
def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj:
        if obj.tag == 'destination':
            return True
        else:
            return False
    else:
        return True


# create a sprite based on the "player" image
# position at the top left corner. control the 
# sprite with the arrow keys while checking a 
# precondition to make sure we don't walk into 
# walls. the speed of the sprite enables "graceful" 
# movement with the keyboard
p = image('player', (0, 0)).speed(5).keys(precondition=evaluate)

# center the player on the 0,0 grid cell
p.move_to((0, 0))


# these two nested for loops iterate over
# every grid cell on the canvas
for y in range(HEIGHT):
    for x in range(WIDTH):
    	# don't create a block on the location of
    	# the player OR the location of the green cell
        if (x, y) == (0, 0) or (x, y) == (29, 16):
            continue
        # make a random decision to color the cell red
        # this number can be adjusted to make the cells
        # smaller or larger.
        if rand(1, 3) > 2.5:
            shape(RECT, RED, (x, y))

# a callback function for when the player reaches 
# the green destination
def win(b, p):
    text('YOU WIN', BLUE)
    gameover()
   
# draw a green destination cell on the bottom right
d = shape(RECT, GREEN, (WIDTH-1, HEIGHT-1), tag='destination')

# if the player reaches this cell, execute the 'win' callback
d.collides(p, win)

# register the 'r' key for resetting the game
keydown('r', reset)
```

# Maze Editor

Random mazes can be a little challenging to work with since we don't have any control where the obstacles are created. We'll now walk through how to create mazes.

To help illustrate mazes, the Predigame platform includes a maze editor example that can be used to create, preview, and delete mazes. Try running the code and create some mazes.

    my_machine$ pigm maze-editor.py

The code includes some debugging information on start up that documents how to use the maze  editor.

```
Left Click to draw / Right Click to undo a selection
p - preview saved mazes (hit again for next)
d - delete the current saved maze
s - save the current maze in a new file
r - reset and clear screen
```
It's possible to create some pretty cool mazes. Give it a try and see what you can create! Here's an example maze:

![alt text](http://predicate.us/predigame/images/maze_editor.png "Predigame Grid Coordinates")

## Loading Saved Mazes

Once a few mazes have been created, it's possible to load them into a new game. Let's take a look at a simple example. This code assumes that two mazes "1" and "2" are available in the `mazes/` directory.

```python
WIDTH = 30
HEIGHT = 18
TITLE = 'MAZE From File'

# load a sample maze
maze('1', partial(shape, RECT, RED))

# load another sample maze
maze('2', partial(image, 'stone'))

# center the player on the 0,0 grid cell
p = image('player', (0, 0)).speed(5).keys()
p.move_to((0, 0))

# register the 'r' key for resetting the game
keydown('r', reset)
```

This example loads two separate mazes into the game - one containing **RED** shapes, the other **stone** images. The code uses a concept called a "partial".  This is like a callback function, but provides the coder additional controls for how that callback can be used.

#### Understanding Partials
Here's an example shape sprite that will create a **RED** rectangle at a random position. 
```python
shape(RECT, RED)
```
Now, here's the above example coded as a partial definition:
```python
partial(shape, RECT, RED)
```
Notice the similarities? Predigame and python will unpack the partial into the shape once it's ready to create the shape.
