Zombie Madness
---------
It's possible to take this game in a number of different directions. This README walks through some common **use cases** and the underlying code that would be required for implementation. Each example includes a **LOCATION GUIDE** that will detail where in the `zombie_plugins.py` file to insert and modify the code.

# Background Images

## Static backgrounds
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

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
## Random backgrounds
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

If you interested in changing backgrounds for each level, we'll want to create a list with all of our choices and then use the `choice()` function to randomly select an image file from the list.
```python
   choices = ['grass', 'ville']
   background(choice(choices))
```
We also have a pretty cool image service that will randomly pick and use a background from the Internet. This can add a little jazz to your game.
```python
   background()
```
## Progressive backgrounds
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

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

## Generated maze
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

It's possible, also within the `setup` function, to define the type of maze should be drawn on the game service. Assuming that there is an image with the name `'stone'`, it's possible to use that to draw the maze.
```python
   maze(callback=partial(image, 'stone'))
```
Likewise, it's also possibly to simply draw a maze with colors. For example,
```python
   maze(callback=partial(shape, RECT, BLACK))
```
## Random maze
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

Sometimes it may be desirable to have some randomly placed blocks to create as obstacles. It's possible to tweak the `2.75` number to draw more or less blocks. The numbers `19` and `31` signify the HEIGHT and WIDTH of the window, in terms of grid cells.
```python
   for y in range(19):
      for x in range(31):
         if rand(1, 3) > 2.75:
            shape(RECT, RED, (x, y), tag='wall')
```

# Player Actions

## Keyboard Shortcuts
**NOTE:** some of these shortcuts use the same keys. They can be easily changed to something else. It is not possible to assign more than one shortcut to the same keyboard key.

### Change the walking keys
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

The game uses arrow keys for walking by default. It's possible to change them to something else. The below example changes them to `w`, `a`, `s`,  and `d`. This code will need to be added to your `setup` function
```python
   player.keys(right = 'd', left = 'a', up = 'w', down = 's', precondition=player_physics)
```
This code will obey the maze walls. If you want to walk through them, remove the `, precondition=player_physics` ending. The resulting code will look like this:
```python
   player.keys(right = 'd', left = 'a', up = 'w', down = 's')
```
### Change facing direction (without moving)
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

Sometimes you may want to quickly change direction and shoot without having to move. This code will rebind the arrow keys to changing the facing direction. Keep in mind that you'll need to **change the walking keys** or **register different keys for the facing direction**. This code will need to be added to your `setup` function.
```python
   def __direction__(player, direction):
      """ change the players direction  """
      player.direction = direction
      player.act(IDLE, FOREVER)

   keydown('left', callback=partial(__direction__,player, LEFT))
   keydown('right', callback=partial(__direction__,player, RIGHT))
   keydown('up', callback=partial(__direction__,player, BACK))
   keydown('down', callback=partial(__direction__,player, FRONT))
```
## Inventory Controlled Weapons
**LOCATION GUIDE (ALL WEAPONS)**: *insert inside the setup function* -- `def setup(player, level):`


| weapon        | cost           | energy impact  |
| ---------------- |:-------------:| :-----:|
| air gun      | 2 | 0 |
| c4 explosive      | 50      |   -10 |
| flame thrower | 500      |    -50 |
| green rage | 25      |    10 |
| grenade | 100      |    -50 |
| landmine | 50      |   0 |
| machine gun | 2      |    0 |
| mustard gas | 250      |    -10 |
| punch | 1      |    -10 |
| wall builder | 5      |    -5 |
| wall buster | n/a      |    -0.25 |
| nuclear bomb (custom) | mucho grande      |    0 |

*Core conceptual language* - A player "takes" a Thing (can be anything) that is later used.

### Inventory Market Place
Buy weapons, restore energy at the market place! Be sure to add this line to your `setup` function.

```python
   display('f1', 'inventory', player._inventory)
```

### Air Gun
Shoots "air" bullets. Default activation is with the `space` bar.

```python
   player.take(AirGun(call='space'))
```

### C4 Explosives
Drops C4 explosives. Thrown with the `7` key, detonated with the `8` key. Default throwing distance is `8` blocks and blast radius is `10` (which is about four blocks). Explosives only kill actors and do not destroy walls.

```python
   player.take(C4(call='7', detonate='8', distance=8, radius=10))
```

### Flame Thrower
Throws a devastating ball of fire. It takes quite a bit of energy to generate a the fiery ball, but it's a sure way to clear out the bad guys. The flame had an internal compass that shadows the player's orientation, so move the player around for maximum effect.

Generated and thrown with the `2` key. Use player directional keys after thrown to control flame ball.

```python
   player.take(FlameThrower(call='2'))
```

### Green Rage (Energy Drink)
Give your player a dose of caffeine for continued rage! Only accessible from the inventory panel.  


### Grenade
Throw a grenade with the `3` key. Default throwing distance is `6` blocks and blast radius is `10` (which is about four blocks). Grenade destroys anything in it's blasting radius - including walls!

```python
   player.take(Grenade(call='3', distance=6, radius=10))
```

### Landmine
Plant a landmine with the `6` key. The bomb is activated in one second. **BE CAREFUL!!** - your player can fall victim to the explosive.

```python
   player.take(Landmine(call='6', delay=1))
```

### Machine Gun
Keep your blue forces safe with the trusty machine gun! Default trigger is the `5` key with single bullets that travel `15` blocks. Want rapid fire more bullets? Be sure to set the `repeat` parameter.

```python
   player.take(MachineGun(call='5', distance=15, repeat=1))
```

### Mustard Gas
Take out your enemies with a harmful chemical weapon. Thrown with the `4` key, a mustard gas capsule travels `10` blocks and has an effective radius of `20` (about 5 blocks). The gas capsule only explodes if it hits an actor instance.

```python
   player.take(MustardGas(call='4', distance=10, radius=20))
```
### Punch
When all else fails, use your hands! The simple punch is activated with the `1` key. Make sure you sneak behind your enemy as they can attack you otherwise!

```python
   player.take(Punch(call='1'))
```
### Wall Builder
Have your player use walls to provide defense from the zombies. The first line sets the wall image, the second sets the directional callback keys.

```python
   wall = partial(image, 'stone')
   player.take(WallBuilder(left='left', right='right', front='up', back='down', wall=wall))
```
Want to use colored rectangles instead? Give this a shot:
```python
   wall = partial(shape, RECT, BLACK)
   player.take(WallBuilder(left='left', right='right', front='up', back='down', wall=wall))
```

### Wall Buster
Let your player bust through the maze walls. Make sure you reset player walking keys (see above). A player that obeys physics can't bust walls!

```python
   player.take(WallBuster())
```

### Nuclear Bomb [HARD]
The nuclear bomb is provided as a custom **thing** that you can add to your game.

#### Part 1: Define the Thing
This code describes the `NuclearBomb` as a child or subclass of a `Thing`. A `Thing` has a name (`da bomb`), a quantity (`1`), energy impact (`0`), and cost to purchase (`5000`). As these attributes are written, one bomb is included in the definition.

The rest of the code is documented inline with comments that describe each action.

This code should be copied to the top of the plugins file.

```python
class NuclearBomb(Thing):
   """ make a custom weapon """
   def __init__(self, call='n'):
      Thing.__init__(self, call)
      self.name = 'da bomb'
      self.quantity = 1
      self.energy = 0
      self.cost = 5000

   def use(self):
      # do we have the inventory to use this weapon?
      if not check(self):
         return

      # explode a bomb, wrap image with explosion, only kill reds
      def explode(bomb):
         # destroy the bomb image
         bomb.destroy()

         # display the nuke image for 1 second
         image('nuke', pos=(0,0), size=40).destruct(1)

         # kill only red forces
         for r in get('red'):
            r.kill()

      # drop a bomb to the half way point, make it explode
      def dropit(jet):
         bomb = image('bomb', pos=(15,1), size=4)
         bomb.move_to((15,10), callback=partial(explode, bomb)).speed(10)
         jet.move_to((35,0), callback=jet.destroy)

      # fly a plane across the screen, stop half way
      # flip the image so the plane faces right
      jet = image('jet', pos=(-5, 0), size=4).flip()

      # fly the plane to the halfway point, drop by bomb
      jet.speed(10).move_to((15, 0), callback=partial(dropit, jet))

      # deduct inventory by 1
      self.quantity -= 1

```

#### Part 2: Register the Weapon
Once the code is copied, the weapon can now be registered and used. By default our bomb can be called in with the `4` key.

```python
   player.take(NuclearBomb(call='n'))
```

## Legacy Weapons

**NOTE:** The following legacy weapons can still be used (and without inventory control). They all require adding the following callback in the `setup` function.

```python
   keydown('1', partial(punch, level, player))
   keydown('2', partial(throw, level, player))
```

### Simple air shot
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing shoot function prior to insertion**

```python
def shoot(level, player):
   """ simple air shot """
   player.act(SHOOT, loop=1)
   target = player.next_object()

   if target and isinstance(target, Actor):
      target.kill()
```
### Simple air shot (that kills any sprite)
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing shoot function prior to insertion**

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
### Shooting bullets (that kills any sprite)
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing shoot function prior to insertion**

**Customizations:**
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
### Shooting range limiting bullets
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing shoot function prior to insertion**

By default there is no limit the the distance a bullet can fly. At times that can be a little unrealistic. Here's the modification to the code that will allow bullets to fly just a few grid cells.
```python
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

### Flame thrower
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing throw function prior to insertion**

This one goes without any explanation. It's just really awesome. Keep in mind that the throw key is `2` on your keyboard.
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
### Throw a grenade
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing throw function prior to insertion**

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
      gpos = grenade.pos
      exp = shape(CIRCLE, RED, (gpos[0]-1.5,gpos[1]-1.5), size=0.3)
      exp.collides(sprites(), __hit__)
      exp.scale(10)
      callback(partial(exp.fade, 1), 0.5)
   grenade.move_to(pos, callback=callback(partial(__explode__, grenade), wait=1))
```
### Throw a grenade (that explodes on impact and doesn't destroy walls)
```python
def throw(level, player, repeat=False):
   """ throw an explode on impact grenade (just kills actors)"""
   player.act(THROW, loop=1)
   # set the range of the grenade
   pos = player.facing(5)
   bpos = player.pos
   grenade = image('grenade', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.3).spin(0.25)

   def __explode__(grenade):
      grenade.destroy()
      gpos = grenade.pos
      exp = shape(CIRCLE, RED, (gpos[0]-1.5,gpos[1]-1.5), size=0.3)
      exp.scale(10)
      callback(partial(exp.fade, 1), 0.5)

   def __hit__(grenade, target):
      if target != grenade and target != player:
         if isinstance(target, Actor):
            __explode__(grenade)
            target.kill()
   grenade.move_to(pos, callback=grenade.destroy)
   grenade.collides(sprites(), __hit__)
```
### Throw a punch
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing punch function prior to insertion**

```python
def punch(level, player):
   player.act(THROW, loop=1)
   target = at(player.next(player.direction))
   if isinstance(target, Actor):
       target.kill()
   elif isinstance(target, Sprite):
       target.fade(0.5)
```
### Plant a landmine
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

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
### Throw some c-4 explosives
**LOCATION GUIDE**: *insert as a top-level function* -- **must delete existing throw**

This is a two-part weapon. By default `2` will throw the c-4 (you can throw many), and then `3` will detonate.

```python
def throw(level, player, repeat=False):
   """ throw some c-4 (explodes on '3' button press)"""
   player.act(THROW, loop=1)
   # set the range of the c4
   pos = player.facing(8)
   bpos = player.pos
   c4 = image('mine', tag='c4', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.5).spin(0.25)

   def __hit__(c4, target):
      if target != c4 and target != player:
         if isinstance(target, Actor):
            target.kill()
   def __explode__(c4):
      c4.destroy()
      cpos = c4.pos
      exp = shape(CIRCLE, RED, (cpos[0]-1.5,cpos[1]-1.5), size=0.3)
      exp.collides(sprites(), __hit__)
      exp.scale(10)
      callback(partial(exp.fade, 1), 0.5)
   def __detonate__():
      bombs = get('c4')
      for bomb in bombs:
         callback(partial(__explode__, bomb), 0.25)
   keydown('3', __detonate__)
   c4.move_to(pos)
```

### Walk through walls (and destroy them too!!)
 **LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

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
### Add walls
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

This code will register callbacks for the `w`, `a`,`s`, and `d` keys. The put function a stone wall at the grid location next to the player. Run this code as part of your `setup` function since the code needs a reference to the player actor.
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


# Friendlies
**LOCATION GUIDE**: *insert as a top-level function*

Your objective is to save the life of friendly forces.
```python
def get_blue():
   """ create a blue (friendly) actor """
   # return name of actor and grazing speed
   return 'Piggy', 3
```
## Custom destination image
**LOCATION GUIDE**: *insert as a top-level function*

Don't like the default pig pen image? It's possible to create your own with this function and then change `pigpen` with whatever image you want!
```python
def blue_destination():
   return 'pigpen'
```
## Self defense [HARD]
**LOCATION GUIDE**: *insert as a top-level function and modify `get_blue`*

It's possible to have your blue forces automate a self defense. This code is a bit weird and it still may allow hostiles to kill blue forces.

**Step 1:** Define a self-defense function
This code checks all directions to see if any red forces are within `5` blocks. If your blue force is not a Piggy, you'll want to change `HAPPY` to `ATTACK`.  When a red force is nearby, Piggy performs an air shot -- instantly killing the enemy.
```python
def blue_defend(actor):
   """ activate self defense """
   for direction in [BACK, FRONT, LEFT, RIGHT]:
      things = actor.next_object(direction=direction, distance=5)
      if things and has_tag(things, 'red'):
            actor.direction = direction
            actor.stop = True
            actor.act(HAPPY, 5)
            target = actor.next_object()
            if target and isinstance(target, Actor):
               target.kill()
            callback(partial(actor.act, IDLE, FOREVER), 5)
```
**Step 2:** Change the `get_blue` function to include the newly added `blue_defend` self defense function.

```python
def get_blue():
   """ create a blue (friendly) actor """
   # return name of actor, grazing speed, self defense
   return 'Piggy', 2, blue_defend
```


## Make Friendlies Away from Hostiles(s)
*Under Development*

## Schedule more friendlies
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

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
**LOCATION GUIDE**: *insert as a top-level function*

Your object is to eliminate all hostile actors.
```python
def get_red():
   """ create a red (hostile) actor """
   # return name of actor, movement speed
   return 'Zombie-1', 1
```

Spawn different types of zombies at different speeds!
```python
def get_red():
   """ create a red (hostile) actor """
   # return name of actor, movement speed
   zombies = ['Zombie-1','Zombie-2','Zombie-3']
   return choice(zombies), randint(1,4)

```

## Schedule more hostiles
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

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

# Levels
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

## Overriding the default behavior (MUST ADD)
It's possible to change how the story ends! Here's a few possible tricks you can try. Be sure to **register** your `__completed__` function first!

```python
   def __completed__(self):
      # promote level by killing all the hostiles
      if len(get('red')) == 0:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True

   # register the __completed__ function to control how the level decisions are made
   level.completed = MethodType(__completed__, level)
```

You'll notice that plugging in this code will drastically change how the levels end. What happens if all the piggies die? What happens if your player dies?

The rest of the the updates will be specific to the `__completed__` function. There is no need to register that function more than once.


### Option 1: All Piggies Go Home
This code will promote the level if all blue forces (piggies) go home. It will also end the game if one dies. Again, you'll want to replace your existing `__completed__` function with this code.
```python
   def __completed__(self):
      if self.blue_spawned == self.blue_safe:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True
      elif self.blue_killed > 0:
         text('GAME OVER')
         gameover()

```

### Option 2: Option 1 + Player Survives
```python
   def __completed__(self):
      if self.blue_spawned == self.blue_safe:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True
      elif self.blue_killed > 0 or len(get('player')) == 0:
         text('GAME OVER')
         gameover()
```

### Option 3: Option 2 + Kill all the hostiles
```python
   def __completed__(self):
      if self.blue_spawned == self.blue_safe:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True
      elif len(get('red')) == 0:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True
      elif self.blue_killed > 0 or len(get('player')) == 0:
         text('GAME OVER')
         gameover()  
```
### Option 4: Piggies go home and their house survives
```python
   def __completed__(self):
      if self.blue_spawned == self.blue_safe:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True
      elif len(get('destination')) == 0:
        text('DESTINATION DESTROYED! GAME OVER!')
        gameover()  
      elif self.blue_killed > 0 or len(get('player')) == 0:
         text('GAME OVER')
         gameover()  
```
### Option 5: Option 4 + all reds die
```python
   def __completed__(self):
      if self.blue_spawned == self.blue_safe and len(get('red')) == 0:
         self.player.energy = 50
         self.player.wealth = 250
         save_state(self.player, 'player.pg')
         return True
      elif len(get('destination')) == 0:
        text('DESTINATION DESTROYED! GAME OVER!')
        gameover()  
      elif self.blue_killed > 0 or len(get('player')) == 0:
         text('GAME OVER')
         gameover()  
```

# Scoring

## Add  countdown timer
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

This code should be added to the end of the `setup` function.
```python
   timer(color=WHITE, value=30)
 ```
If desired, it's also possible to add a countdown time that adds additional time for each level. The following code will add 30 seconds for each level.
```python
   timer(color=WHITE, value=30*level.level)
 ```
