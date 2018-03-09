# something an Actor can use
from functools import partial
from .utils import register_keydown as keydown, at, get, has_tag, sprites
from .constants import *
from . import predigame as p
class Thing:
    def __init__(self, call=None):
        self.name = None
        self.image = None
        self.lethality = 100
        self.energy = 1
        self.quantity = 1
        self.actor = None
        self.cost = 1000

        if call is not None:
            keydown(call, self.use)

    def use(self):
        raise NotImplementedError('base class cannot be called directly')

    def __str__(self):
        return '{} {}'.format(self.name, self.quantity)

def check(thing):
    if thing.quantity == 0:
        t = p.text('out of {}'.format(thing.name), RED)
        p.callback(t.destroy, 2)
        return False
    if thing.actor.energy == 0:
        t = p.text('not enough energy for {}'.format(thing.name), RED)
        p.callback(t.destroy, 2)
        return False
    return True

class Punch(Thing):
    """ throwing a simple punch """
    def __init__(self, call='space'):
        Thing.__init__(self, call)
        self.name = 'punch'
        self.energy = -10
        self.quantity = 10
        self.cost = 1

    def use(self):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return

        self.actor.act(THROW, loop=1)
        target = at(self.actor.next(self.actor.direction))
        if isinstance(target, Actor):
            target.health -= self.lethality
        elif isinstance(target, Sprite):
            target.fade(0.5)
        self.actor.energy = self.energy
        self.quantity -= 1

class FlameThrower(Thing):
    """ a pretty cool flame thrower """
    def __init__(self, call='space'):
        Thing.__init__(self, call)
        self.name = 'flame thrower'
        self.energy = -50
        self.quantity = 2
        self.cost = 500

    def use(self):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return

        self.actor.act(THROW, loop=1)
        pos = self.actor.facing()
        bpos = self.actor.pos
        beam = p.image('flame', pos=(bpos[0]+0.5, bpos[1]+0.5), size=0.3).spin(0.2)

        def __hit__(beam, target):
            if target != self.actor:
                 if isinstance(target, Actor):
                      target.kill()
                 elif isinstance(target, Sprite):
                      target.fade(0.5)
        beam.collides(sprites(), __hit__)

        def __grow__(beam):
            beam.move_to(self.actor.facing())
            beam.scale(1.1).speed(10)
            if beam.size > 8:
                beam.fade(1)

        p.callback(partial(__grow__, beam), wait=0.1, repeat=50)
        self.actor.energy = self.energy
        self.quantity -= 1


class Grenade(Thing):
    """ throw a grenade """
    def __init__(self, call='space', distance=5, radius=5):
        Thing.__init__(self, call)
        self.name = 'grenade'
        self.energy = -50
        self.quantity = 2
        self.cost = 100
        self.radius = radius
        self.distance = distance

    def use(self):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return

        self.actor.act(THROW, loop=1)
        pos = self.actor.facing(self.distance)
        bpos = self.actor.pos
        grenade = p.image('grenade', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.3).spin(0.25)

        def __hit__(grenade, target):
            if target != grenade:
                if isinstance(target, Actor):
                    target.kill()
                elif isinstance(target, Sprite):
                    target.fade(0.5)
        def __explode__(grenade):
            grenade.destroy()
            gpos = grenade.pos
            exp = p.shape(CIRCLE, RED, (gpos[0]-1.5,gpos[1]-1.5), size=0.3)
            exp.collides(sprites(), __hit__)
            exp.scale(self.radius)
            p.callback(partial(exp.fade, 1), 0.5)
        grenade.move_to(pos, callback=p.callback(partial(__explode__, grenade), wait=1))

        self.actor.energy = self.energy
        self.quantity -= 1

class MustardGas(Thing):
    """ throw a chemical weapon (only affects actors) """
    def __init__(self, call='space', distance=5, radius=5):
        Thing.__init__(self, call)
        self.name = 'mustard gas'
        self.energy = -10
        self.quantity = 2
        self.cost = 250
        self.radius = radius
        self.distance = distance

    def use(self):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return

        self.actor.act(THROW, loop=1)
        pos = self.actor.facing(self.distance)
        bpos = self.actor.pos
        grenade = p.image('grenade', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.3).spin(0.25)

        def __explode__(grenade):
            grenade.destroy()
            gpos = grenade.pos
            exp = p.image('smoke', (gpos[0]-1.5,gpos[1]-1.5), size=0.3)
            exp.scale(self.radius)
            p.callback(partial(exp.fade, 1), 0.5)

        def __hit__(grenade, target):
            if target != grenade and target != self.actor:
                if isinstance(target, Actor):
                    __explode__(grenade)
                    target.kill()
        grenade.move_to(pos, callback=grenade.destroy)
        grenade.collides(sprites(), __hit__)

        self.actor.energy = self.energy
        self.quantity -= 1


class AirGun(Thing):
    """ Simple air shot (that kills any sprite) """
    def __init__(self, call='space'):
        Thing.__init__(self, call)
        self.name = 'air gun'
        self.cost = 2
        self.energy = 0
        self.quantity = 50

    def use(self):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return

        self.actor.act(SHOOT, loop=1)
        target = self.actor.next_object()
        if target and isinstance(target, Actor):
            target.kill()
        elif target and isinstance(target, Sprite):
            target.fade(0.5)

        self.actor.energy = self.energy
        self.quantity -= 1


class MachineGun(Thing):
    """ machine gun that shoots range limited bullets """
    def __init__(self, call='space', distance=5, repeat=5):
        Thing.__init__(self, call)
        self.name = 'machine gun'
        self.energy = 0
        self.quantity = 50
        self.cost = 2
        self.distance = distance
        self.repeat = repeat

    def use(self, _repeat=False):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return
        self.actor.act(SHOOT, loop=1)
        pos = self.actor.facing(self.distance)
        bpos = self.actor.pos
        bullet = p.image('bullet', tag='bullet', pos=(bpos[0]+0.85, bpos[1]+0.35), size=0.3)
        bullet.speed(10).move_to((pos[0]+0.5,pos[1]+0.35),callback=bullet.destroy)

        def __hit__(bullet, target):
            if target != self.actor:
                bullet.destroy()
                if isinstance(target, Actor):
                    target.kill()
                elif isinstance(target, Sprite):
                    target.fade(0.5)
        bullet.collides(sprites(), __hit__)
        if not _repeat:
            p.callback(partial(self.use, True), wait=0.2, repeat=self.repeat)

        self.actor.energy = self.energy
        self.quantity -= 1


class Landmine(Thing):
    """ plant a landmine """
    def __init__(self, call='space', delay=3):
        Thing.__init__(self, call)
        self.name = 'landmine'
        self.energy = 0
        self.cost = 50
        self.quantity = 50
        self.delay = delay

    def use(self, _repeat=False):
        from .Actor import Actor
        from .Sprite import Sprite

        if not check(self):
            return

        mine = p.image('mine', self.actor.pos, tag='mine')

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
                p.callback(partial(mine.fade, 2), 1)

        p.callback(partial(mine.collides, sprites(), __explode__), wait=self.delay)

        self.actor.energy = self.energy
        self.quantity -= 1


class C4(Thing):
    """ throw some C4 explosives """
    def __init__(self, call='space', detonate='f', distance=8, radius=10):
        Thing.__init__(self, call)
        self.name = 'c4'
        self.energy = -10
        self.quantity = 5
        self.cost = 50

        self.distance = distance
        self.radius = radius

        keydown(detonate, self.detonate)

    def use(self, _repeat=False):
        if not check(self):
            return

        self.actor.act(THROW, loop=1)
        pos = self.actor.facing(self.radius)
        bpos = self.actor.pos
        c4 = p.image('mine', tag='c4', center=(bpos[0]+0.5, bpos[1]+0.5), size=0.5).spin(0.25)
        c4.move_to(pos)

        self.actor.energy = self.energy
        self.quantity -= 1

    def detonate(self):
        from .Actor import Actor
        from .Sprite import Sprite

        def __hit__(c4, target):
            if target != c4 and target != self.actor:
                if isinstance(target, Actor):
                    target.kill()
        def __explode__(c4):
            c4.destroy()
            cpos = c4.pos
            exp = p.shape(CIRCLE, RED, (cpos[0]-1.5,cpos[1]-1.5), size=0.3)
            exp.collides(sprites(), __hit__)
            exp.scale(self.radius)
            p.callback(partial(exp.fade, 1), 0.5)
        bombs = get('c4')
        for bomb in bombs:
            p.callback(partial(__explode__, bomb), 0.25)

class WallBuster(Thing):
    """ bust through some walls """
    def __init__(self):
        Thing.__init__(self)
        self.name = 'wall buster'
        self.energy = -0.25
        self.quantity = 'unlimited'
        self.cost = 'n/a'

        p.callback(self.use, 1)

    def use(self):
       def __wall_buster__(player, wall):
           if not check(self):
	           return
           pos = wall.pos
           wall.destroy()
           p.image('smoke', center=(pos[0]+0.5, pos[1]+0.5), size=2).fade(2)
           self.actor.energy = self.energy
       self.actor.collides(get('wall'), __wall_buster__)

class WallBuilder(Thing):
    """ bust through some walls """
    def __init__(self, left, right, front, back, wall):
        Thing.__init__(self)
        self.name = 'wall builder'
        self.energy = -5
        self.quantity = 10
        self.cost = 5
        self.wall = wall

        keydown(back, callback=partial(self.put, BACK))
        keydown(left, callback=partial(self.put, LEFT))
        keydown(front, callback=partial(self.put, FRONT))
        keydown(right, callback=partial(self.put, RIGHT))

    def put(self, direction) :
        pos = self.actor.next(direction)
        self.wall(pos=pos,tag='wall')
        self.actor.energy = self.energy
        self.quantity -= 1

    def use(self):
        return None


class EnergyDrink(Thing):
    """ get a quick energy boost """
    def __init__(self):
        Thing.__init__(self)
        self.name = 'green rage'
        self.energy = 10
        self.quantity = 'unlimited'
        self.cost = 25

    def use(self):
        return None
