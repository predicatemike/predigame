Working with Sprites
===================
The Predigame sprite is a generic two-dimensional object that is integrated with other sprites in a larger scene. A sprite can consist of a bitmap (still) image or a basic geometrical shape (circle, rectangle, ellipse). Sprites in Predigame have some fun properties - they can be clicked, collide with other sprites, even fade, spin or pulse.

Let's have fun working with Sprites!

Getting Started
----------
To get things started, we're going to create a basic PrediGame canvas that we'll use to place sprites. The canvas will have a width of 30 grid cells and a height of 20 grid cells.

```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Sprites Demo'
```
Save your changes. Let's call the file `sprite-demo.py`.  Try running the game from the terminal using the `pigm` command (you'll want to run this command from the directory where you saved the file).

    my_machine$ pigm sprite-demo.py

This program doesn't do much just yet. Just an empty window titled "Sprites Demo". So boring. We're going to add some more code, but first let's make sure we understand grid coordinates and how to place sprites within those coordinates.

Understanding Grid Coordinates
-------------
Probably the easiest way to understand grid coordinates is to enable the `grid()` overlay in the game code.

```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Sprites Demo'

# enable the grid overlay
grid()
```
Save your code and try running the this version using the same command:

    my_machine$ pigm sprite-demo.py

The result should look like the figure below. Counting the grid coordinates will show **30** from *left to right* and **20** from *top to bottom*. This doesn't address how to address sprites using grid coordinates, we'll cover that next.

![alt text](http://predicate.us/predigame/images/sprites_grid.png "Predigame Grid Coordinates")

The following code will show how to place rectangle sprites in each of the four corners of the window.

```python
# top/left
shape(RECT, RED, (0, 0))

# bottom/left
shape(RECT, BLUE, (0, HEIGHT-1))

# top/right
shape(RECT, PINK, (WIDTH-1, 0))

# bottom/right
shape(RECT, PURPLE, (WIDTH-1, HEIGHT-1))
```
Saving and running the code will show:
- a RED rectangle at position `(0, 0)` corresponding to the top-left corner
- a BLUE rectangle at position `(0, HEIGHT-1)` corresponding to the bottom-left corner
- a PINK rectangle at position `(WIDTH-1,  0)` corresponding to the top-right corner
- a PURPLE rectangle at position `(WIDTH-1, HEIGHT-1)` corresponding to the bottom-right corner

#### *Why are the corners specified as `WIDTH-1` and `HEIGHT-1`*?
Computers always start counting at zero. So if `WIDTH = 30` and the first grid is `0` the thirtieth cell would be `WIDTH-1` or `29`.

Running this code should look like the figure below.
![alt text](http://predicate.us/predigame/images/sprites_grid2.png "Predigame Grid Coordinates")

We added a few labels to make the grid coordinates a little more easier to visualize. It's possible to replace the code from the previous exercise with the one here:

```python
# place on center of screen
text("Understanding Grid Coordinates", color=BLACK, size = 2.0)
text("this is a 30 x 20 window", color=BLACK, pos=(WIDTH/2-7, HEIGHT/2+1), size = 1.75)

# top/left
shape(RECT, RED, (0, 0))
text("(0, 0)", RED, pos = (0,1), size = 1.25)

# bottom/left
shape(RECT, BLUE, (0, HEIGHT-1))
text("(0, " + str(HEIGHT-1) + ")", BLUE, pos = (0, HEIGHT-2), size=1.25)

# top/right
shape(RECT, PINK, (WIDTH-1, 0))
text("(" + str(WIDTH-1) + ", 0)", PINK, pos = (WIDTH-2.5,1), size = 1.25)

# bottom/right
shape(RECT, PURPLE, (WIDTH-1, HEIGHT-1))
text("(" + str(WIDTH-1) + ", " + str(HEIGHT-1) + ")", PURPLE, pos = (WIDTH-3,HEIGHT-2), size = 1.25)
```

The resulting game window will show the following rendering:
![alt text](http://predicate.us/predigame/images/sprites_grid3.png "Predigame Grid Coordinates")

Creating Shapes
-------------
There are two types of sprites supported in the Predigame platform - shapes and images. Let's look at shapes. The formal *function definition* (or signature) for creating a shape is as follows:

```python
shape(shape = None, color = None, pos = None, size = (1, 1))
```
Reading this code, there are four **attributes**:

1. `shape` - the type of shape to create. Can be one of RECT, SQUARE, CIRCLE, or ELLIPSE
2. `color` - the shape's color. Can be a constant like BLACK, BLUE, or RED, as well as a (red, green, blue) tuple such as (128, 128, 128)
3. `pos`   - the grid cell of the shape
4. `size`  - the size of the shape in terms of grid cells using the form (width, height). For CIRCLE shapes, only the first number is considered.

Notice that each of these attributes have default values. This means that they are option, and if not specified, Predigame will create a random shape type of random color, size, and position.

```python
# draw a random shape type of random color, size, and position
shape()
```

Here are a few example shapes we can add to our canvas:
```python
# red circle at position (2, 2)
shape(CIRCLE, RED, (2, 2))

# create a big blue circle next to the red one
shape(CIRCLE, BLUE, (5, 1), 3)

# create a 2x2 ORANGE square at position (10, 2)
shape(RECT, ORANGE, (10, 2), (2,2))

# create a 6x1 rectangle
shape(RECT, AQUA, (15, 2), (6, 1))

# create a custom colored (r, g, b) ELLIPSE
shape(ELLIPSE, (134, 134, 134), (23, 2), (5, 2))
```
If we add each of the above shapes to our code, the resulting file will look like this:
```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Sprites Demo'

# red circle at position (2, 2)
shape(CIRCLE, RED, (2, 2))

# create a big blue circle next to the red one
shape(CIRCLE, BLUE, (5, 1), 3)

# create a 2x2 ORANGE square at position (10, 2)
shape(RECT, ORANGE, (10, 2), (2,2))

# create a 6x1 rectangle
shape(RECT, AQUA, (15, 2), (6, 1))

# create a custom colored (r, g, b) ELLIPSE
shape(ELLIPSE, (134, 134, 134), (23, 2), (5, 2))
```
Save and run this code. The result should look similar to the image below:
![alt text](http://predicate.us/predigame/images/sprites_grid4.png "Predigame Grid Coordinates")

Creating Images
-------------
Like shapes, the Predigame platform also supports creating images. The formal *function definition* (or signature) for creating an image is as follows:

```python
image(name = None, pos = None, center = None, size = 1)
```
Notice that it is similar, yet slightly different than the code for creating a shape. An image in Predigame is defined by:

1. `name` - the name (without extension) of the image file. The image file should be stored in the **images/** directory. For example, if we had an image "coke.png" in our **images/** directory, the name of the image would be "coke".
2. `pos` -  the grid cell of the shape. Officially, this will be the top-left cell of the image.
3. `center` - used as an alternative to `pos` to use this position as the center point.
4. `size` - the size of the shape in terms of grid cells. By default, the image will be fit into a single grid cell.

Notice again that each of these attributes have default values. This means that they are option, and if not specified, PrediGame will select a random image from the **images/** directory of size `1` (so it will fit into a single cell) and will be placed at a random position.

Now here are a few example shapes we can also add to our canvas:

```python
# create a "sprite" sprite and place at grid location (2, 8)
image('sprite', (2, 8))

# create a "coke" sprite of double size and place at grid (7, 8)
image('coke', (7, 8), size = 2)

# create a zombie
image('zombie-1', (13,9), size = 5)

# create another zombie
image('zombie-2', (19,9), size = 5)
```
Add the above lines to our code file and save the changes. The result should look similar to the image below:
![alt text](http://predicate.us/predigame/images/sprites_grid5.png "Predigame Grid Coordinates")

Sprite Effects
-------------
Drawing sprites can be a lot of fun, however, we can add some effects to bring them to life. For example, we can make sprites spin, float, and even pulse. Let's look at the some new sprites with effects attached.

### Spinning
```python
image('sprite', (2,14)).spin(time=1)
```
This sprite will spin and complete a revolution every second. It's possible to change `time` to a smaller or larger number to increase or decrease the spin rate.

### Pulsing
```python
image('sprite', (7,14)).pulse(time=0.5, size=3)
```
Have the sprite execute a pulsing effect - rapidly expand and shrink. The `size` attribute will control the maximum size of the sprite (as a multiplier) during expansion. The `time` attribute sets the amount of time (in seconds) the sprite will take to complete an expansion or contraction.

### Floating

```python
image('coke', (13, 15), size = 2).speed(1).float(distance=1)
```
Have the sprite float in place. The `.speed(1)` call sets the speed of the movement and the `distance` attribute sets the amount of room (in term of grid cells) the sprite will use to complete a floating operation.

Sprite Event Callbacks
-------------
When we code a game we sometimes need to create actions that will eventually occur. Think of a mouse trap. It doesn't do much until, you know, the mouse comes by and eats the cheese. In code we define callback functions -- they don't do anything until a certain event, like a mouse click, occurs in the game.

The Python program language requires that we specify our functions before registering them in the code. Let's look at a simple callback example.

```python
def destroy(s):
    s.destroy()
```
This function will simply destroy a circle anytime one is clicked. Functions don't work until they are called, or in the case of callbacks, until they are registered.

```python
s = shape(CIRCLE, RED, rand_pos()).clicked(destroy)
```
That's right.. We can basically add a `.clicked(destroy)` to the end of our shape definition and register a callback function that won't get called until the player clicks on the circle.

Let's take a look at few more examples of event callbacks.

### Click Events
We already briefly covered a click example, but let's look at one that is a little more complicated.

```python
def doit(s):
    s.destroy()
    image('kaboom', center=(15, 10), size=25)

image('clickme', (19, 15), size = 2).pulse(time=0.05, size= 1.25).clicked(doit)
```
This example creates a fast pulsing `clickme` sprite that is destroyed when clicked and replaced with an oversized  `kaboom` image.

```python
s = image('coke', (13, 15), size = 2)
s.speed(1).bouncy().spin().pulse().clicked(s.destroy)
```
This example is similar to our first mouse click example on the shape but it recycles the sprites `destroy()` method as a callback - `.clicked(s.destroy)`. It also chains a whole bunch of effects that make this sprite bounce around the canvas, pulse, and even spin.

### Keyboard Events
We can also control a sprite with the keyboard.

```python
image('zombie-1', (28, 18), size = 2).keys()
image('zombie-2', (25, 18), size = 2).keys(right='d', left='a', up='w', down='s')
```
In this case `zombie-1` is registered with the `.keys()`function which will control the sprite with keyboard arrow buttons. In the case where we'd like to use other keyboard buttons, such as a multi-player game, we can assign new keys - `.keys(right='d', left='a', up='w', down='s')`.

### Collisions
It's common in some games, like FPS, to want to check for sprites that collide with each other.  Let's take our previous keyboard example and check for collisions.

```python
def eatit(z, s):
    s.destroy()
    z.scale(1.2)

image('zombie-1', (28, 18), size = 2).keys().collides(sprites(), eatit)
image('zombie-2', (25, 18), size = 2).keys(right='d', left='a', up='w', down='s').collides(sprites(), eatit)
```
Here we **chain** the `.collides()` callback which takes in a list of sprites and registers a callback function. As coded, we register both zombies to check for collisions with all sprites, the `sprites()` call will return all sprites on the canvas, and invite the `eatit` callback function.

Challenge Program - Thirsty Zombie
-------------

Our zombie likes sprite and hates code. Your job is to throw "sprite" sprites at the zombie and have the zombie consume (destroy) them. If the zombie consumes a "coke" sprite, it will explode and end the game. You'll want to keep score by rewarding one point for every "sprite" consumed.

**Game Algorithm**:
- create a game canvas with a width of 30 and height of 20 grid cells
- use `callback(function, time)` throw the cans
- pick a random probability for throwing a "coke"
- reward the zombie `1` point for every sprite consumed
- destroy the zombie, if
    - the zombie consumes a coke
    - the score falls below zero
- use random speeds and callback times to throw more or less cans
- use effects to make the game fun
- reset the game if the `r` key is pressed

### Game Code
Here's the first few lines:
```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Thirsty Zombie'

# load in the stormy background
BACKGROUND = 'stormy'
```
This will build a window of 30x20 grid cells and add a "stormy" background image. *Make sure this image is saved in the `backgrounds/` directory*.

**Zombie Creation**

```python
# create a zombie sprite. flip the sprite so the zombie faces to the right
zombie = image('zombie-2', (5, 15), size = 3).speed(10).flip()

# tell the zombie to follow the mouse movement
zombie.follow()
```
We use the `.flip()` function to have the zombie face towards right right side of the screen.

Here's how to throw a sprite object:
```python
def throw():
    # pick a random position and select the y coordinate
    y_pos = rand_pos()[1]

    # create a soda and move it from right to left
    target = 'sprite'
    if randint(1, 5) == 4:
        target = 'coke'     
    s = image(target, (WIDTH+5, y_pos)).speed(2).collides(zombie, consume)
    s.move_to((-1, y_pos), callback = lambda: miss(s))

    # a callback to call the throw() function again
    callback(throw, rand(0.5, 2))
```
**Callback Functions**

Before we draw the code for a beverage, we need to define the logic that describes consumption. Remember, this is because python requires us to define our callback functions before we use them.

```python
# zombie consumes a drink and explodes if it's a coke
def consume(target, zombie):
    # destroy the can
    target.destroy()

    if target.name == 'coke':
        # zombies don't like coke. end the game
        zombie.destroy()
        image('kaboom', center=(15, 10), size=25)
        gameover()
    else:
        # we added a sprite. increase score
        score(1)
```
If we don't consume a beverage, the zombie will need to suffer a little bit. Our second callback describes the "misses":

```python
# zombie misses the opportunity to take a drink and is thirsty.
def miss(target):

    # destroy the can
    target.destroy()

    # subtract a point if this was a sprite
    if target.name == 'sprite':
        score(-1)

    # we lost
    if score() < 0:
        text("TOTAL DEHYDRATION")
        zombie.rotate(90).pulse(time=2, size=2)
        gameover()
```
**Throwing Soda**

Throwing cans of soda is also a callback function, but controlled via time. A key to throwing is to mix up the positions a bit. The line of code `y_pos = rand_pos()[1]` is a shorthanded way of randomly picking a y (top/bottom) position. Read through the rest of the code below, we added some documentation to clarify each of the lines.

```python
# this is a callback that throws a sprite or coke across the screen
def throw_soda():

    # pick a random position and select the y coordinate
    y_pos = rand_pos()[1]

    # create a soda and move it from right to left
    target = 'sprite'

    # roughly 50% of the cans are cokes
    if randint(1, 2) == 2:
        target = 'coke'     

    # position the sprite off the right side of the screen
    # make it move fast (speed 10)
    # if the zombie hits the can, execute the "consume" callback
    s = image(target, (WIDTH+5, y_pos)).speed(10).collides(zombie, consume)

    # move the sprite to the left. execute callback "miss" if movement finishes
    s.move_to((-1, y_pos), callback = lambda: miss(s))

    # a callback to call the throw() function again
    callback(throw_soda, rand(0, 1.5))

# schedule the throw callback to run
callback(throw_soda, 1)
```
**Final Bits**

The final parts of the game enable score keeping and resetting the game if the 'r' key is pressed.

```python
# add this so we can keep score of the game
score(color=WHITE)

# press the r key to reset
keydown('r', reset)
```

**Complete Code**

Below is the complete code for "thirsty zombie".  We added an easter egg if the 'b' button is pressed - launch of soccer balls; it's an added obstacle that the zombie will need to avoid.

```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Thirsty Zombie'

# load in the stormy background
BACKGROUND = 'stormy'

# create a zombie sprite. flip the sprite so the zombie faces to the right
zombie = image('zombie-2', (5, 15), size = 3).speed(10).flip()

# tell the zombie to follow the mouse movement
zombie.follow()

# keep track if the zombie is spinning
spinning = False

# zombie consumes a drink and explodes if it's a coke
def consume(target, zombie):

    # a spinning zombie cannot consume things
    if spinning:
        return

    # destroy the can
    target.destroy()

    if target.name == 'coke':
        # zombies don't like coke. end the game
        zombie.destroy()
        image('kaboom', center=(15, 10), size=25)
        gameover()
    else:
        # we added a sprite. increase score
        score(1)

# zombie misses the opportunity to take a drink and is thirsty.
def miss(target):

    # destroy the can
    target.destroy()

    # subtract a point if this was a sprite
    if target.name == 'sprite':
        score(-1)

    # we lost
    if score() < 0:
        text("TOTAL DEHYDRATION")
        zombie.rotate(90).pulse(time=2, size=2)
        gameover()

# this is a callback that throws a sprite or coke across the screen
def throw_soda():

    # pick a random position and select the y coordinate
    y_pos = rand_pos()[1]

    # create a soda and move it from right to left
    target = 'sprite'

    # roughly 50% of the cans are cokes
    if randint(1, 2) == 2:
        target = 'coke'     

    # position the sprite off the right side of the screen
    # make it move fast (speed 10)
    # if the zombie hits the can, execute the "consume" callback
    s = image(target, (WIDTH+5, y_pos)).speed(10).collides(zombie, consume)

    # move the sprite to the left. execute callback "miss" if movement finishes
    s.move_to((-1, y_pos), callback = lambda: miss(s))

    # a callback to call the throw() function again
    callback(throw_soda, rand(0, 1.5))

# schedule the throw callback to run
callback(throw_soda, 1)

# this is a callback when the zombie is done spinning
def done_spinning():

    # the "global" variable is set to False (since we are done spinning)
    global spinning
    spinning = False

# this is a callback when the zombie is hit by a ball
def spinner(b, z):

    # the "global" variable is set to True (since we are spinning)
    global spinning
    spinning = True

    # destroy the ball
    b.destroy()

    # spin the zombie.. time probably can't go much smaller than 0.5
    # execute callback done_spinning after completing two rotations
    z.spin(time=0.5, rotations=2, callback=done_spinning)

# this is a callback function to launch the ball
def launch():

    # create a ball and position off the right side of the screen
    random_y_position = rand_pos()[1]

    # position balls off the screen, make them spin and move a little fast
    ball = image('ball', (WIDTH+5, random_y_position), size=2).spin(0.2).speed(5)

    # move right to left, destroy if movement completes
    ball.move_to((-5, random_y_position), callback=ball.destroy)

    # make the zombie spin if hit by a ball
    ball.collides(zombie, spinner)

    # prepare to launch another
    callback(launch, rand(0.2, 1))

# hitting 'b' starts launching balls!
keydown('b', launch)

# add this so we can keep score of the game
score(color=WHITE)

# press the r key to reset
keydown('r', reset)
```

Save this code as `thirsty-zombie.py` and let's give it a run!

    my_machine$ pigm thirsty-zombie.py

If it loads correctly, the following game canvas should display. Have fun!!

![alt text](http://predicate.us/predigame/images/sprites_grid6.png "Predigame Grid Coordinates")
