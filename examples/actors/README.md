Actor Framework
===================
Predigame Actors are Sprites that perform certain **actions** - mostly in the form of animations that maze the game more realistic. Actors can perform any number of actions (walk, run, jump, attack) which are usually left up to the artist's creation of the sprite.

Prior to reading more about Predicate Actors, be sure to check out our [Sprites](https://github.com/predicateacademy/predigame/blob/master/examples/sprites/README.md) and [Mazes](https://github.com/predicateacademy/predigame/blob/master/examples/maze/README.md) tutorials!

Here are a few example Actors.

![alt text](http://predicate.us/predigame/images/zombie_animated.gif "Predigame Grid Coordinates")
![alt text](http://predicate.us/predigame/images/soldier_animated.gif "Predigame Grid Coordinates")
![alt text](http://predicate.us/predigame/images/other_animated.gif "Predigame Grid Coordinates")

NOTICE: Licensed Files
----------
All of the artwork used here has been purchased from [envanto market](https://graphicriver.net/category/game-assets/sprites) and is not included in the Predigame standard distribution. Feel free to purchase your own license and we can show you the steps to include the actor artwork into your Predigame.

How Actors Work
----------
The artwork we use for actors are *four directional sprites* in that each of the actions are repeated in each direction of movement (up, down, left, right). Actor animations may seem a big complicated under the hood, but it is nothing more than just a sequence of still images that are refreshed at a fast enough rate to give the **illusion of animation**.

In Predigame we store actors in the `actors` directory has highlighted in the picture below.
![alt text](http://predicate.us/predigame/images/actors.png "Predigame Actors ")

Each of the highlighted png files capture a single frame.
![alt text](http://predicate.us/predigame/images/actors2.png "Predigame Actors ")

And when those frames are rotated fast enough the actor (in this case the zombie) appears to be attacking! Pretty cool, right?

Now let's try to add actors in our code.

To get things started, we're going to create a basic Predigame canvas that we'll use to place sprites. The canvas will have a width of 30 grid cells and a height of 20 grid cells.

```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Actor Demo'
```
Save your changes. Let's call the file `actor-demo.py`.  Try running the game from the terminal using the `pigm` command (you'll want to run this command from the directory where you saved the file).

    my_machine$ pigm actor-demo.py

This program doesn't do much just yet. Just an empty window titled "Actor Demo". Now lets add an Actor to our game canvas.

Creating Actors
-------------
Every actor is stored in the `actors` directory. It's the same concept as `images` but rather than having a *single file* for each actor, the file structure is a little more complicated. Every actor is a directory of actions and each action directory is contains an a sequence of still images.

Let's take a quick glance at this figure again.
![alt text](http://predicate.us/predigame/images/actors.png "Predigame Actors ")
The above figure represents the total available actors that we have available (your listing will be different). There actors are named `Chika`, `Piggy`, `Soldier-1` and so on. Each actor has some number of actions that can be performed.  `Zombie-1`, for instance, has `attack`, `die`, `idle`, and `walk`. Notice that each action has a direction? Those indicate the orientation of the actor when that action occurs. The action selected, `attack_front`, has six still frames.  

Let's add an actor to our game.
```python
WIDTH = 30
HEIGHT = 20
TITLE = 'Actor Demo'

# create a Zombie actor
player = actor('Zombie-1', center=(14, 9), size=4)
```
Save your changes and run the game. Notice that we see an actor but our actor doesn't do much. Let's see what happens when have our actor follow the keyboard.
```python
# create a Zombie actor
player = actor('Zombie-1', center=(14, 9), size=4)

# follow the arrow keys
player.keys()
```
Save and try running the game now. Our zombie has come to life.

Actor Actions
-------------
Let's take a deeper dive into some of the actions that an actor can do. We're going to modify the previous code a bit so that we don't tie the actor to the keyboard for movement.

```python
# create a Zombie actor
player = actor('Zombie-1', center=(14, 9), size=4)

player.direction = FRONT
player.act(WALK, loop=FOREVER)
```
There are a few things that can be changed around for illustration.  Let's start with direction. Possible directions include:
```python
player.direction = FRONT
player.direction = BACK
player.direction = LEFT
player.direction = RIGHT
```
Now you wouldn't want to have all of these directions listed like we did above. That was for illustration.

Let's take a look at actions. The `Zombie-1` actor also supports `ATTACK`, `DIE`, and `IDLE` actions. Paired with a call to the `act` function is the amount of times to loop through the animation images. The default behavior is to loop through the images forever.

We assembled a quick demonstration of our different actors and their possible actions. These are provided in the [examples directory](https://github.com/predicateacademy/predigame/tree/master/examples/actors). If you have this code stored locally, try running each example.

    my_machine$ pigm actor-maze.py
    my_machine$ pigm actor-soldier.py
    my_machine$ pigm actor-other.py

If you look at the code for each of these demonstrations, you'll see a bunch of key event registration invocations. Each are quick ways to demonstrate how the actions are supposed to function.


Sample Game - Making Bacon
-------------

Let's create a simple maze game that demonstrates some other cool things we can do with actors. Create a new file named `bacon.py` and start with our typical first three lines of code:

```python
WIDTH = 30
HEIGHT = 18
TITLE = 'Making Bacon'
```
Like before, these doesn't do much just yet. Here's a line to add a simple **background** (*remember backgrounds are retrieved from the backgrounds/ directory*)

```python
# use a grass background
BACKGROUND = 'grass'
```
Next we'll define a constant for the number of piggies to create. This line of code will not have any impact just yet.

```python
# how many piggies to create
PIGGIES = 10
```
Now let's create a Daedalus maze with stone images. Remember that we must have a `stone` in image in our images directory.
```python
maze(callback=partial(image, 'stone'))
```
**CHECKPOINT** - try saving and running your code at this point. You should see something like the below picture.

![alt text](http://predicate.us/predigame/images/maze_grass.png "Bacon 1")

If all looks well with the maze, let's add our player actor. We're going for `Soldier-2`. The actor will be assigned to move on keyboard arrows and every keyboard movement will call the `evaluate` callback. This is code that we can use to "evaluate" each move to make sure the player can't walk through walls.

```python
# a callback that keeps the player from running
# into walls.
def evaluate(action, sprite, pos):
    obj = at(pos)
    if obj and obj.tag == 'wall':
        return False
    else:
        return True

# create a soldier on the bottom left grid cell
player = actor('Soldier-2', (0, HEIGHT-1), tag='player', abortable=True)

# have the solider attach to the keyboard arrows
# each move is "evaluated" to make sure the player
# doesn't walk through the wall
player.keys(precondition=evaluate)

# player moves at a speed of 5 with an animation rate of 2
# which flips the sprite image every other frame
player.speed(5).rate(2).move_to((0, HEIGHT-1))
```
Let's give this a shot. Try running the code to ensure that the player can navigate the maze maze without being able to walk through walls.

If this works, try adding some piggies. Here is one case where the `PIGGIES` constant will be used.

```python
# create a piggy function
def create_piggy(num):
    for x in range(num):
        pos = rand_pos()
        piggy = actor('Piggy', pos, tag='piggy')
        piggy.move_to((pos))
        # graze is a random walk
        piggy.wander(graze, time=0.4)

# create some piggies
create_piggy(PIGGIES)
```
Piggy is an "automated" actor of sorts. There is a special function `wander` that is called every movement and `wander` calls the `graze` callback function. Try adjusting the time a bit to see what impact that has to each piggy.

Try running saving these updates and running the game. We'll see the maze, our player, and now some piggies!

![alt text](http://predicate.us/predigame/images/maze_actors.png "Bacon 2")

The final part of our game is the shooting part! We'll create a `shoot` callback that is assigned to the space bar. It looks a little like an air shot, but the piggy effects are pretty cool.

```python
# shoot a weapon
def shoot():
    player.act(SHOOT, loop=1)

    #find the next object that is facing the player
    target = player.next_object()

    # if it's a piggy and that piggy is alive
    if target and target.tag == 'piggy' and target.health > 0:
        # kill the piggy
        target.health = 0
        # make the piggy disappear in 10 seconds
        target.destruct(5)
        # get a point
        score(1)

    # check to see if there are any piggys left
    if score() == PIGGIES:
        text('Time for some BACON!! (%s secs)' % time(), color=BLACK)
        gameover()

# register space to shoot
keydown('space', shoot)

#we're keeping score
score()

# register the 'r' key for resetting the game
keydown('r', reset)
```

Notice we use the `PIGGIES` constant a second time? That's why we made it a constant. Our game needs to track all the piggies and will stop playing when `PIGGIES` piggies have been killed. *NOTE: this code will not work if more points are assigned for each dead piggy!*
