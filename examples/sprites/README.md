Working with Sprites
===================
The PrediGame sprite is a generic two-dimensional object that is integrated with other sprites in a larger scene. A sprite can consist of a bitmap (still) image or a basic geometrical shape (circle, rectangle, ellipse). Sprites in PrediGame have some fun properties - they can be clicked, collide with other sprites, even fade, spin or pulse. 

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

This program doesn't do much just yet. Just an empty window titled "Sprites Demo". So boring. Let's add some more code.

Creating Shapes
-------------
There are two types of sprites supported in the PrediGame platform - shapes and images. Let's look at shapes. The formal *function definition* (or signature) for creating a shape is as follows:

```python
shape(shape = None, color = None, pos = None, size = (1, 1))
```
Reading this code, there are four **attributes**:

1. `shape` - the type of shape to create. Can be one of RECT, SQUARE, CIRCLE, or ELLIPSE
2. `color` - the shape's color. Can be a constant like BLACK, BLUE, or RED, as well as a (red, green, blue) tuple such as (128, 128, 128)
3. `pos`   - the grid cell of the shape
4. `size`  - the size of the shape in terms of grid cells using the form (width, height). For CIRCLE shapes, only the first number is considered.

Notice that each of these attributes have default values. This means that they are option, and if not specified, PrediGame will create a random shape type of random color, size, and position.

Here are a few example shapes we can add to our canvas:

```python
# red circle at position 2, 2
shape(CIRCLE, RED, (2, 2))

# create a big blue circle next to the red one
shape(CIRCLE, BLUE, (5, 1), 3)

# create a 2x2 ORANGE square at position (8,2)
shape(RECT, ORANGE, (10, 2), (2,2))

# create a 6x1 rectangle
shape(RECT, AQUA, (15, 2), (6, 1))

# create a custom colored (r, g, b) ELLIPSE
shape(ELLIPSE, (134, 134, 134), (23, 2), (5, 2))
```
Creating Images
-------------
Like shapes, the PrediGame platform also supports creating images. The formal *function definition* (or signature) for creating an image is as follows:

```python
image(name = None, pos = None, size = 1)
```
Notice that it is similar, yet slightly different than the code for creating a shape. An image in Predigame is defined by:

1. `name` - the name (without extension) of the image file. The image file should be stored in the **images/** directory. For example, if we had an image "coke.png" in our **images/** directory, the name of the image would be "coke".
2. `pos` -  the grid cell of the shape. Officially, this will be the top-left cell of the image.
3. `size` - the size of the shape in terms of grid cells. By default, the image will be fit into a single grid cell.

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
Have the sprite execute a pulsing - rapidly expand and shrink. The `size` attribute will control the maximum size of the sprite (as a multiplier) during expansion. The `time` attribute sets the amount of time (in seconds) the sprite will take to complete an expansion or contraction.

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
    image('kaboom', (15, 10), size=25)

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

**Steps to accomplish**:
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

### Hints
Creating a zombie:

```python
# create a zombie sprite. flip the sprite so the zombie faces to the right
zombie = image('zombie-2', (5, 15), size = 5).speed(10).keys().flip()
```

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