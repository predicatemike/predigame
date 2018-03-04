# an Inventory of things an actor can use
from pygame.locals import *
from .constants import *
from . import predigame
class Inventory:
    def __init__(self):
        self.things = {}
        self.title = None

    def add(self, thing):
        """ add something to our inventory """
        if thing.name in self.things:
            thing.quantity = self.things[thing.name].quantity
        self.things[thing.name] = thing

    def update(self, delta):
        """ update something """
        a = 1

    def draw(self,SURF):
        """ draw the inventory on a surface """
        SURF.fill((0,0,0))

        if not self.title:
            self.title = predigame.text('Actor Inventory', YELLOW, (13,1))
        self.title._draw(SURF)

        for thing in self.things:
            thing.draw(SURF)

    def __str__(self):
        r = 'Inventory: \n'
        for thing in self.things:
            r += '  ' + str(self.things[thing]) + '\n'
        return r

    def dump(self):
        print(str(self))
