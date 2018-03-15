# A Place for Gamer Customizations

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


def setup(player, level):
   """ setup is called for every level. this is a place to add new things. """
   display('f1', 'inventory', player._inventory)

   maze(callback=partial(image, 'stone'))

   player.keys(right = 'd', left = 'a', up = 'w', down = 's')

   # randomly pick a background
   background()

   player.take(Punch(call='1'))
   player.take(FlameThrower(call='2'))
   player.take(Grenade(call='3', distance=6, radius=10))
   player.take(MustardGas(call='4', distance=10, radius=20))
   player.take(AirGun(call='space'))
   player.take(MachineGun(call='5', distance=15, repeat=3))
   player.take(Landmine(call='6', delay=1))
   player.take(C4(call='7', detonate='8', distance=8, radius=10))
   player.take(NuclearBomb(call='n'))

   player.take(WallBuster())
   #wall = partial(image, 'stone')
   #player.take(WallBuilder(left='left', right='right', front='up', back='down', wall=wall))
   display('f1', 'inventory', player._inventory)

   def drink(soda, player):
      soda.destroy()
      player.energy = 10
   fill(partial(image,'sprite', size=1.0), 0.05, player, drink)

   def claim(coin, player):
      coin.destroy()
      player.wealth = 5
   fill(partial(image,'coin', size=1.0), 0.25, player, claim)

def get_blue():
   """ create a blue (friendly) actor """
   # return name of actor, grazing speed, self defense
   return 'Piggy', 2

def get_red():
   """ create a red (hostile) actor """
   # return name of actor, movement speed
   zombies = ['Zombie-1','Zombie-2','Zombie-3']
   return choice(zombies), randint(1,4)

def get_player():
   # name of player sprite (must exist in actors/ directory)
   # pick a random Soldier
   choices = ['Soldier-1', 'Soldier-2', 'Soldier-3', 'Soldier-4', 'Soldier-5',
              'Soldier-6', 'Soldier-7', 'Soldier-8', 'Soldier-9', 'Soldier-10']
   return choice(choices)
