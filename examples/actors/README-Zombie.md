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
   background((25, 25, 25))
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
   if level.level == 1:
      background('grass')
   elif level.level == 2:
      background('ville')
   else:
      background('stormy')
```
Notice that the file line is the "catch all" statement. This basically means the same `stormy` image will be used for the third and beyond levels.

# Mazes

## Generated Maze
It's possible, also within the `setup` function, to define the type of maze should be drawn on the game service. Assuming that there is an image with the name `'stone'`, it's possible to use that to draw the maze.
```python
   maze(callback=partial(image, 'stone'))
```
Likewise, it's also possibly to simply draw a maze with colors. For example,
```python
   maze(callback=partial(shape, RECT, BLACK))
```
## Random Maze
Sometimes it may be desirable to have some randomly placed blocks to create as obstacles. It's possible to tweak the `2.75` number to draw more or less blocks. The numbers `19` and `31` signify the HEIGHT and WIDTH of the window, in terms of grid cells.
```python
   for y in range(19):
      for x in range(31):
         if rand(1, 3) > 2.75:
            shape(RECT, RED, (x, y), tag='wall')
```
## Add Walls
This code will register callbacks for the `w`, `a`,`s`, and `d` keys. The put function a stone wall at the grid location next to the player. Run this code as part of `setup` since the code needs a reference to the player actor.
```python
   def __put__(player, direction):
      """ put a block at the player's next location  """
      pos = player.next(direction)
      image('stone', pos, tag = 'wall')

   keydown('w', callback=partial(__put__, player, BACK))
   keydown('a', callback=partial(__put__, player, LEFT))
   keydown('s', callback=partial(__put__, player, FRONT))
   keydown('d', callback=partial(__put__, player, RIGHT))
```

# Basic Weapons
The signature (function name) of each weapon will need to remain the same. These should be copied into the plugin code without indentation. All weapons have 100% lethality.

## Simple Air Shot
```python
def shoot(level, player):
   """ simple air shot """
   player.act(SHOOT, loop=1)
   target = player.next_object()

   if target and isinstance(target, Actor):
      target.kill()
```
## Simple Air Shot (that kills any sprite)
```python
def shoot(level, player):
   """ air shot that will kill any actor or sprite """
   player.act(SHOOT, loop=1)
   target = player.next_object()
   if target and isinstance(target, Actor):
      target.kill()
   elif target and isinstance(target, Sprite):
      target.fade(0.5)
```
## Bullets (that kills any sprite) [HARD]
Challenges:
* try having bullets only destroy actors
* try changing the bullet image
```python
def shoot(level, player, repeat=False):
   """ shoot real bullets """
   player.act(SHOOT, loop=1)
   pos = player.facing()
   bpos = player.pos
   bullet = image('bullet', tag='bullet', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)
   bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.5))

   def __hit__(bullet, target):
      if target != player:
         bullet.destroy()
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   bullet.collides(sprites(), __hit__)
```
At the very end of this function, it's possible to add a machine gun fire with the following lines:
```python
   if not repeat:
      callback(partial(shoot, level, player, True), wait=0.2, repeat=5)
```
Try changing the `wait` attributes. If it's too small you'll notice that the bullets collide with each other. Try also changing the `repeat` option for more bullets.

If the following line is removed, bullet will push through multiple objects, making it VERY LETHAL!!
```python
         bullet.destroy()
```


## Flame Thrower [EASY]
This one goes without any explanation. It's just really awesome. Keep in mind that the throw key is `1` on your keyboard.
```python
def throw(level, player, repeat=False):
   """ flame thrower """
   player.act(THROW, loop=1)
   pos = player.facing()
   bpos = player.pos
   beam = shape(ELLIPSE, RED, pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3)

   def __hit__(beam, target):
      if target != player:
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   beam.collides(sprites(), __hit__)

   def __grow__(beam):
      beam.move_to(player.facing())
      beam.scale(1.1).speed(10)
      if beam.size > 20:
        beam.fade(1)

   if not repeat:
      callback(partial(__grow__, beam), wait=0.1, repeat=50)
```
## Throw a Grenade
Another cool throwing option..
```python
def throw(level, player, repeat=False):
   """ grenade thrower """
   player.act(THROW, loop=1)
   # set the range of the grenade
   pos = player.facing(5)
   bpos = player.pos
   grenade = image('grenade', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.3).spin(0.25)

   def __hit__(grenade, target):
      if target != grenade:
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   def __explode__(grenade):
      grenade.destroy()
      exp = shape(CIRCLE, RED, grenade.pos, size=0.3)
      exp.collides(sprites(), __hit__)
      exp.scale(10)
      callback(partial(exp.fade, 1), 0.5)
   grenade.move_to(pos, callback=callback(partial(__explode__, grenade), wait=1))
```

## Throw a Punch [EASY]
```python
def punch(level, player):
   player.act(THROW, loop=1)
   target = at(player.next(player.direction))
   if isinstance(target, Actor):
       target.kill()
   elif isinstance(target, Sprite):
       target.fade(0.5)
```
## Limit the range of the bullet
By default there is no limit the the distance a bullet can fly. At times that can be a little unrealistic. Here's the modification to the code that will allow bullets to fly just a few grid cells.
```Python
def shoot(level, player, repeat=False):
   """ shoot real bullets """
   distance = 4
   player.act(SHOOT, loop=1)
   pos = player.facing(distance)
   bpos = player.pos
   bullet = image('bullet', tag='bullet', pos=(bpos[0]+0.85, bpos[1]+0.35), size=0.3)
   bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.35),callback=bullet.destroy)

   def __hit__(bullet, target):
      if target != player:
         bullet.destroy()
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)
   bullet.collides(sprites(), __hit__)
   if not repeat:
      callback(partial(shoot, level, player, True), wait=0.2, repeat=5)
```
The way this code works is quite simple. Bullets will travel for `distance` number of grid cells before disappearing. In the example above, the distance is `4`, but this can be changed to any number. Keep in mind that there are some sensitive targets in the game so it may be wise to limit the distance that a bullet can fly!

## Walk Through Walls (and destroy them too!!)
Friendlies and hostiles must obey the ways, but it's possible to have the player be a little stealthy. Add this line to your `setup` function.
```python
   player.keys()
```
Want to clear a path through the walls? Be sure the add these lines right under the keys override (it won't work otherwise). Keep in mind that this is pretty easy to move around, but it also makes you and your friendlies a little easier to find!
```python
   def __wall_buster__(player, wall):
      wall.fade(0.25)
   player.collides(get('wall'), __wall_buster__)
```

## Multidirectional Bullets
*Under Development*

## Plant a Landmine
Mines are cool! This will use the `m` key drop the mine. It'll be active within three seconds, so be sure to get out of the way! There are quite a few numbers here that can be tweaked, so you'll want to try a few things until you end up with the perfect mine.
```python
   def __drop__(player):
      """ put a landmine right where the player is standing """
      mine = image('mine', player.pos, tag = 'mine')

      def __hit__(mine, target):
         """ mine hits something and that something dies """
         if isinstance(target, Actor):
            target.kill()
         elif isinstance(target, Sprite):
            target.fade(0.5)

      def __explode__(mine, sprite):
         """ explode the mine """
         if mine != sprite:
            mine.collides(sprites(), __hit__)
            callback(partial(mine.fade, 2), 1)
      # wait three seconds to activate the mine
      callback(partial(mine.collides, sprites(), __explode__), wait=3)
   keydown('m', callback=partial(__drop__, player))
```

## Limiting Inventory
*Under Development*

# Friendlies
Your objective is to save the life of friendly forces.
```python
def get_blue():
   """ create a blue (friendly) actor """
   # return name of actor and grazing speed
   return 'Piggy', 3
```
## Custom Destination Image
Don't like the default pig pen image? It's possible to create your own with this function and then change `pigpen` with whatever image you want!
```python
def default_blue_destination():
   return 'pigpen'
```

## Make Friendlies Away from Hostiles(s)
*Under Development*

## Schedule More Friendlies
It's easy to schedule more friendlies with a callback function. Here's a couple of variations. All will need to be added to your `setup` function.

**schedule a single friendly (1 second delay)**
```python
   callback(level.create_blue, wait=1)
```
**schedule a friendly every 10 seconds and repeat 5 times**
```python
   callback(level.create_blue, wait=10, repeat=5)
```

**schedule a friendly every 10 seconds and repeat forever**
```python
   callback(level.create_blue, wait=10, repeat=FOREVER)
```


# Hostiles
Your object is to eliminate all hostile actors.
```python
def get_red():
   """ create a red (hostile) actor """
   # return name of actor, movement speed
   return 'Zombie-1', 1
```
## Schedule More Hostiles
It's easy to schedule more hostiles with a callback function. Here's a couple of variations. All will need to be added to your `setup` function.

**schedule a single hostile (1 second delay)**
```python
   callback(level.create_red, wait=1)
```
**schedule a hostile every 10 seconds and repeat 5 times**
```python
   callback(level.create_red, wait=10, repeat=5)
```

**schedule a hostile every 10 seconds and repeat forever**
```python
   callback(level.create_red, wait=10, repeat=FOREVER)
```


# Scoring

## Add  Countdown Timer
This code should be added to the end of the `setup` function.
```python
   timer(color=WHITE, value=30)
 ```
If desired, it's also possible to add a countdown time that adds additional time for each level. The following code will add 30 seconds for each level.
```python
   timer(color=WHITE, value=30*level_number)
 ```
