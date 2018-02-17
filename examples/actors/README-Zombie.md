How do I?
-----
It's possible to take a game in a number of different directions. This guide walks through some common **use cases** and the underlying code that would be required for implementation.

# Background Images

## Static Backgrounds
This code will provide a single image that is used in ever level. You'll want to add to your setup function.
```python
   background('grass')
```
You can also just have single color. Here is an example of a gray background.
```python
   background(GRAY)
```
If you have a particular color in mind, it's possible to also define the background with a `(red, green, blue)` tuple.
```python
   background((25, 25, 25)
```
## Random Backgrounds
If you interested in changing backgrounds for each level, we'll want to create a list with all of our choices and then use the `choice()` function to randomly select an image file from the list.
```python
   choices = ['grass', 'ville']
   background(choice(choices))
```
We also have a pretty cool image service that will randomly pick and use a background from the Internet. This can add a little jazz to your game.
```python
   background()
```
## Progressive Backgrounds
Sometimes you'll want to have the same background be used for the same level. This can provide a hint to the user of where they are in the game. In order to accomplish progressive backgrounds, we'll need to evaluate the level and decide which background image to load. Using python, we can accomplish this with an if/else statement.
```python
   if level_number == 1:
      background('grass')
   elif level_number == 2:
      background('ville')
   else:
      background('stormy')
```
Notice that the file line is the "catch all" statement. This basically means the same `stormy` image will be used for the third and beyond levels.

# Mazes

# Computer Opponents

## Add a Opponent

**Objective:** Add a computer controlled opponent that want to find a player sprite. Have the opponent start in the upper right corner.

```python
def lose(z, p):
	p.health = 0

def create_zombie():
	name = choice(['Zombie-1', 'Zombie-2', 'Zombie-3'])
	z = actor(name, (WIDTH-1, 10), tag = 'zombie')
	z.wander(partial(track, z, p, pbad=0.05), time=0.35)
	z.collides(p, lose)
create_zombie()
```

## Schedule More Opponents
**Objective:** Add another computer opponent every 30 seconds.

```python
callback(create_zombie, 30, repeat=True)
```

## Single Target Opponent

## Make Opponents Move Away from Player(s)


# Levels

# Mazes

## Creating Mazes
Create a maze based on stone images (this assumes you have a `stone.png` file saved in your images directory.
```python
maze(callback=partial(image, 'stone'))
```
Create a maze based on black rectangles:
```python
maze(callback=partial(shape, RECT, BLACK))
```



## Add Walls
This code will register callbacks for the `w`, `a`,`s`, and `d` keys. The put function a stone wall at the grid location next to the player.
```python
def put(player, direction):
	""" put a block at the player's next location  """
	pos = player.next(direction)
	image('stone', pos, tag = 'wall')

keydown('w', callback=partial(put, player, BACK))
keydown('a', callback=partial(put, player, LEFT))
keydown('s', callback=partial(put, player, FRONT))
keydown('d', callback=partial(put, player, RIGHT))
```

## Destroy Walls
Allow a player to shoot and destroy any object, including a wall.

```python
def shoot():
	player.act(SHOOT, loop=1)

	target = player.next_object()
	if target and isinstance(target, Actor):
		target.kill()
	elif target:
		target.fade(0.5)

keydown('space', shoot)
```
# Weapons

## Shoot (real) Bullets
```python
def hit(bullet, obj):
	if obj != player:
		bullet.destroy()
		if isinstance(obj, Actor):
			obj.kill()
def shoot():
	player.act(SHOOT, loop=1)
	pos = player.facing()
	bpos = player.pos
	bullet = image('bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
	bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))
	bullet.collides(sprites(), hit)
keydown('space', shoot)
```
## Shoot Through Walls
```python
def hit(bullet, obj):
	if obj != player:
		if isinstance(obj, Actor):
			obj.kill()
		elif isinstance(obj, Sprite):
			obj.fade(0.25)

def shoot():
	player.act(SHOOT, loop=1)
	pos = player.facing()
	bpos = player.pos
	bullet = image('bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
	bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))
	bullet.collides(sprites(), hit)
keydown('space', shoot)
```
## Machine Gun Fire
Keep on firing until you stop. Load and then fire some more.
```python
def load():
	global stop
	stop = False

def stopit():
	global stop
	stop = True

def hit(bullet, obj):
	if obj != player:
		if isinstance(obj, Actor):
			obj.kill()
		elif isinstance(obj, Sprite):
			obj.fade(0.25)

def machine_gun():
	player.act(SHOOT, loop=1)
	pos = player.facing()
	bpos = player.pos
	bullet = image('bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
	bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))
	bullet.collides(sprites(), hit)
	if not stop:
		callback(machine_gun, 0.25)
```
## Throw a Punch

```python
player = actor('Soldier-2', pos=(1, 1), tag = 'player', abortable=True)
player.speed(2).keys()

def punch():
    player.act(THROW, loop=1)
    target = at(player.next(player.direction))
    if isinstance(target, Actor):
        target.kill()
    elif isinstance(target, Sprite):
        target.fade(0.5)

keydown('p', punch)
```

## Shoot in all Directions

## Limit the range of the bullet


## Throw a Bomb

## Limiting Inventory

# Scoring

##  Add a countdown timer

**Objective:** Add a countdown timer that will stop a game when the timer reaches zero.

This is an example of a timer that will start at 30 seconds, count down every second (`step=-1`), stop at zero (`goal=0`), and call the `timer()` callback function when complete. Any scoring element may have a text prefix if desired, but that is optional.

```python
# simple countdown timer example

WIDTH = 30
HEIGHT = 20
TITLE = 'Countdown Timer Example'

def timer():
        text('GAME OVER')
        gameover()

score(30, pos=UPPER_LEFT, method=TIMER, step=-1, goal=0, callback=timer, prefix='Time Left:')
```

## Adjust a countdown timer

**Objective:** Reward the player with additional time for a particular accomplishment.

 
