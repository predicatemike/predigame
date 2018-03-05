# an Inventory of things an actor can use
from pygame.locals import *
from .constants import *
from . import predigame as p
from .Globals import Globals
class Inventory:
    def __init__(self):
        self.things = {}
        self.display_things = []
        self.title = None
        self.actor = None

    def add(self, thing):
        """ add something to our inventory """
        if thing.name in self.things:
            thing.quantity = self.things[thing.name].quantity
        self.things[thing.name] = thing

    def update(self, delta):
        """ update something """
        for dthing in self.display_things:
            dthing._update(delta)

    def setup(self):
        """ build all the things """

        if not self.title:
            self.display_things.append(p.text('Actor Inventory', YELLOW, (13,1)))

        offset = 4
        for key, thing in sorted(self.things.items()):
            self.display_things.append(p.image('buy', RED, (11, offset+0.35)))
            self.display_things.append(p.text(thing.name, RED, (12, offset)))
            self.display_things.append(p.text(thing.quantity, RED, (19, offset)))
            offset += 1

        player = p.actor(self.actor.name, pos=(2,2), size=3)
        player.act(IDLE_FRONT, FOREVER)
        self.display_things.append(player)
        self.display_things.append(p.text('energy', GREEN, (1, 5)))
        self.display_things.append(p.text("{:3d}".format(int(self.actor.energy)), GREEN, (4,5)))
        self.display_things.append(p.text('health', GREEN, (1, 6)))
        self.display_things.append(p.text("{:3d}".format(int(self.actor.health)), GREEN, (4,6)))
        self.display_things.append(p.text('wealth', GREEN, (1, 7)))
        self.display_things.append(p.text("{:3d}".format(int(self.actor.wealth)), GREEN, (4,7)))


    def destroy(self):
        """ tear it all down """
        for t in self.display_things:
            t.destroy()
        self.display_things = []


    def draw(self,SURF):
        """ draw the inventory on a surface """
        SURF.fill((0,0,0))
        for dthing in self.display_things:
            dthing._draw(SURF)

    def __str__(self):
        r = 'Inventory: \n'
        for thing in self.things:
            r += '  ' + str(self.things[thing]) + '\n'
        return r

    def dump(self):
        print(str(self))
