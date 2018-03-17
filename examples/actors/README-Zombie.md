
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

# Bonus Sprites
**LOCATION GUIDE**: *insert inside the setup function* -- `def setup(player, level):`

These boost sprites allow your player to earn extra energy and wealth bonuses during the game. Blue and red forces are immune to boost sprites.

## Energy Boost
This code will drop `sprite` images with a `5%` probability. Anytime the player collides with a `sprite` image, the player is rewarded with a `10%` energy boost.

```python
   def drink(soda, player):
      soda.destroy()
      player.energy = 10
   fill(partial(image,'sprite', size=1.0), 0.05, player, drink)
```

## Wealth Boost
This code will drop `coin` images with a `25%` probability. Anytime the player collides with a `coin` image, the player is rewarded with a `5` point wealth boost.

```python
   def claim(coin, player):
      coin.destroy()
      player.wealth = 5
   fill(partial(image,'coin', size=1.0), 0.25, player, claim)
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
