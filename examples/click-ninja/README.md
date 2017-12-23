The Click Ninja
===================
It's like the app [fruit ninja](https://fruitninja.com/), but different and better. We write the code and control how the game operates. Check out this awesome preview!

[![IMAGE ALT TEXT](http://img.youtube.com/vi/_O8kF_3XAMg/0.jpg)](https://youtu.be/_O8kF_3XAMg "Click Ninja")

----------
Prerequisites
-------------
In order to hack this game, you'll need [python 3](https://www.python.org/downloads/) installed and well as Predicate's Gaming Platform - predigame - which is installed as a [pip package](https://github.com/predicateacademy/predigame).

----------
Basic Game
-------------
The fundamentals for click ninja are pretty basic. Open a text editor and copy in the follow code. This will create a window of 20x14 blocks and a title of 'Click Ninja'
```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'
```
Save your changes. Let's call the file `clickninja.py`.  Try running the game from the terminal using the `pigm` command. 

    my_machine$ pigm clickninja.py

You notice that the game doesn't do much just yet. Just an empty window titled "Click Ninja". So boring. Let's add some more code. We added a bunch of comments to describe the purpose of each line.

```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

# the "main" part of our game
def spawn():

    target = choice([BLACK, ORANGE, AQUA, NAVY])

    # there is a 25% chance to draw a bomb
    if randint(1, 4) == 2:
        target = RED

    # a virual "arc" -- three positions where
    # the object will move
    # 1. bottom/off screen
    # 2. top of the arc
    # 3. bottom/off screen
    arc = rand_arc()

    # draw our sprite
    s = shape(CIRCLE, target, arc[0])

    # if our target is RED
    if target == RED:
        # register the 'explode' callback function
        s.speed(5).clicked(explode)

        # move to second and third points of arc
        # destroy if not hit
        s.move_to(arc[1], arc[2], callback = s.destroy)

    else:
        # register the 'point' callback function
        s.speed(5).clicked(point)

        # move to second and third points of arc
        # destroy if not hit
        s.move_to(arc[1], arc[2], callback = lambda: hurt(s))

    #tell this code to run again -- sometime between 100ms to 3secs
    callback(spawn, rand(0.1, 3))

# keep score (top left)
score(color = PURPLE)

# start the game
callback(spawn, rand(0.1, 3))

# register some keys
# r - rest game
keydown('r', reset)  
```


Let's try our game now. We'll start to see a little more action. It looks a little like juggling, but we can't click on any of the circles. Notice that the last line of code will cause our game to reset if the 'r' key is pressed - this will be important a few steps later.

### Callback Functions
When we code a game we need to create virtual "mouse traps" that describe *key behavior* when certain events occur. A mouse trap doesn't do much until, you know, the mouse comes by and eats the cheese. The same applies to callback functions -- they don't do anything until a certain event, a mouse click in our case.

The Python program language requires that we define specify our **functions** before refer to them in the code. Let's look at a simple callback example.

```python
def destroy(s):
    s.destroy()
```
This function will simply destroy the circle anytime one is clicked. Functions don't work until they are called, or in the case of callbacks, until they are registered. 

```python
s = shape(CIRCLE, target, arc[0]).clicked(destroy)
```

That's right.. We can basically add a `.clicked(destroy)` to the end of our shape and *register* a callback function that won't get called until the player clicks on the circle.

Here's the full code now (we took out all the comments to make it a little easier to read). Let's give it a quick test.

```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s): 
    s.destroy()

def spawn():
    target = choice([BLACK, ORANGE, AQUA, NAVY])

    if randint(1, 4) == 2:
        target = RED

    arc = rand_arc()

    s = shape(CIRCLE, target, arc[0]).clicked(destroy) 
    s.move_to(arc[1], arc[2], callback = s.destroy)
    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, rand(0.1, 3))
keydown('r', reset)    
```
### Keeping Score
We can modify our destroy callback function to **score** the number of things we destroy. It's just requires adding a line of code. 
```python
def destroy(s):
    score(1)
    s.destroy()
```
----------
# Version 1: Keep Alive

At this point we almost have a fully functional game. We just need to add a keep alive function. That is, we want to make sure we stop the game if we don't click on a circle. Look for this line of code in our game:

```python
    s.move_to(arc[1], arc[2], callback = s.destroy)
```
The way this code is written, the `callback` function will be called if nothing else happens to the shape. Let's create a new callback function `failure(s)` that will pause the game. Notice we'll use something called a lamba. We'll be sure to discuss what that means later.
```python
    s.move_to(arc[1], arc[2], callback = lamba: failure(s))
```
Let's make sure we create the failure function. We'll put that right under our `destroy` callback function.
```python
def destroy(s):
    score(1)
    s.destroy()
    
def failure(s):
    text('You Survived %s seconds' % time(), MAROON)
    pause()
```
That's it! Here's the complete code if you need it. Go ahead and enjoy Version 1. How many circles can you click?
```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s):
    score(1)
    s.destroy()

def failure(s):
    text('You Survived %s seconds' % time(), MAROON)
    pause()

def spawn():
    target = choice([BLACK, ORANGE, AQUA, NAVY])

    if randint(1, 4) == 2:
        target = RED

    arc = rand_arc()

    s = shape(CIRCLE, target, arc[0]).clicked(destroy) 
    s.move_to(arc[1], arc[2], callback = lambda: failure(s))
    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, rand(0.1, 3))
keydown('r', reset)   
```
# Version 2: Throwing Food
Let's swap out circles for pictures of food. The predigame platform makes it easy to load pictures in your game. Just copy them to an `images` directory.

    my_machine$ mkdir images
    
The click ninja includes a few food images to get started. Let's see what we have.

    my_machine$ ls images
    bananas.png  cherries.png ham.png      icee.png     pizza.png    taco.png
    bomb.png     fries.png    hotdog.png   olives.png   redsplat.png    
    
Let's say we want to load the hotdog image. We can do that with a single line of code.

```python
image('hotdog', (x, y), size)
```
We'll see that to load the image we need the first part of the file, the initial x and y coordinates, and the size (default is `1.0`). Notice that we don't need to include the `images` directory or the `.png` file extension. Predigame takes care of that for us. 

So, now let's replace the circles with images. To do that we're going to rewrite our `spawn()` function.
```python
def spawn():

    speed = randint(2, 10)
    size = randint(1,4)

    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    arc = rand_arc()

    s = image(target, arc[0], size)
    s.speed(speed).clicked(destroy) 
    s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(spawn, rand(0.1, 3))
```
In addition to drawing images, notice that we also have variables for `speed` and `size`. As our code runs anytime we'll draw a *random* target with a *random* speed and *random* size.  Notice the `randint` functions, such as `randint(2, 10)`. This will randomly pick a number between 2 and 10.

Let's try running our code. Here's the complete version.
```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s):
    score(1)
    s.destroy()

def failure(s):
    text('You Survived %s seconds' % time(), MAROON)
    pause()

def spawn():

    speed = randint(2, 10)
    size = randint(1,4)

    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    arc = rand_arc()

    s = image(target, arc[0], size)
    s.speed(speed).clicked(destroy) 
    s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, rand(0.1, 3))
keydown('r', reset)   
```

# Version 3: Bombs Away
Instead of just drawing food, let's throw some bombs too. Unlike food, our players can't click on a bomb or else.. well, game over! For starters, let's assume there is a 25% (1 out of 4) chance a bomb will be thrown. In code we'll want to add two lines in our `spawn()` function.

```python
    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    if randint(1, 4) == 2:
        target = 'bomb'
```
These last two lines will replace the `target` variable with a bomb with a 25% probability. Now, we said the player can't click on a bomb (game over otherwise) and, unlike food, if they don't click, we don't want to stop the game. This means we'll need to change the following lines:
```python
    s = image(target, arc[0], size)
    s.speed(speed).clicked(destroy)
    s.move_to(arc[1], arc[2], callback = lambda: failure(s)) 
```
And check to see if target is a bomb.
```python
    s = image(target, arc[0], size)
    if target == 'bomb':
       s.speed(speed).clicked(failure)
       s.move_to(arc[1], arc[2], callback = s.destroy) 
    else:
       s.speed(speed).clicked(destroy)    
       s.move_to(arc[1], arc[2], callback = lambda: failure(s))
   
```
Let's try running our code. Here's the complete version.
```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s):
    score(1)
    s.destroy()

def failure(s):
    text('You Survived %s seconds' % time(), MAROON)
    pause()

def spawn():

    speed = randint(2, 10)
    size = randint(1,4)

    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    if randint(1, 4) == 2:
        target = 'bomb'

    arc = rand_arc()

    s = image(target, arc[0], size)
    if target == 'bomb':
       s.speed(speed).clicked(failure)
       s.move_to(arc[1], arc[2], callback = s.destroy) 
    else:
       s.speed(speed).clicked(destroy)    
       s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, rand(0.1, 3))
keydown('r', reset)   
```
# Version 4: Better Score

Our game ends quickly when we make a single mistake and that can make for a frustrating experience for the player. Let's improve our scoring with a few basic rules:

- Reward the player **five points** for clicking food
- Penalize the player  **twenty points** for missing a food item
- Halt the game when the number of points falls below zero
- Halt the game if the player clicks on a bomb

Here's our improved `destroy` and `failure` functions.
```python
def destroy(s):
    score(5)
    s.destroy()

def failure(s):
    score(-20)
    if s.name == 'bomb' or score() < 0:
        text('You Survived %s seconds' % time(), MAROON)
        pause()
```
Let's try running our code. Here's the complete version.
```python
WIDTH = 20
HEIGHT = 14
TITLE = 'Click Ninja'

def destroy(s):
    score(5)
    s.destroy()

def failure(s):
    score(-20)
    if s.name == 'bomb' or score() < 0:
        text('You Survived %s seconds' % time(), MAROON)
        pause()

def spawn():

    speed = randint(2, 10)
    size = randint(1,4)

    target = choice(['bananas', 'cherries', 
                     'olives', 'ham', 'hotdog', 
                     'fries','icee', 'pizza'])

    if randint(1, 4) == 2:
        target = 'bomb'

    arc = rand_arc()

    s = image(target, arc[0], size)
    if target == 'bomb':
       s.speed(speed).clicked(failure)
       s.move_to(arc[1], arc[2], callback = s.destroy) 
    else:
       s.speed(speed).clicked(destroy)    
       s.move_to(arc[1], arc[2], callback = lambda: failure(s))

    callback(spawn, rand(0.1, 3))

score(color = PURPLE)
callback(spawn, rand(0.1, 3))
keydown('r', reset)   
```
