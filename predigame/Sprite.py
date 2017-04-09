import random
from functools import partial
from .utils import *
from . import globs

class Sprite:
    def __init__(self, surface, rect):
        self.surface = surface.convert_alpha()
        self.origin_surface = self.surface
        self.rect = rect
        self.move_speed = 5
        self.move_vec = [self.rect.x, self.rect.y] # destination coordinates
        self.float_vec = [0, 0, 0] # x distance, y distance, offset distance
        self.collisions = []

    def _update(self):
        if not self.rect.x == self.move_vec[0]:
            dist = self.move_vec[0] - self.rect.x
            if abs(dist) < self.move_speed:
                move = dist
            else:
                move = (dist) / abs(dist) * self.move_speed
            self.rect.x += move

        if not self.rect.y == self.move_vec[1]:
            dist = self.move_vec[1] - self.rect.y
            if abs(dist) < self.move_speed:
                move = dist
            else:
                move = (dist) / abs(dist) * self.move_speed
            self.rect.y += move

        float_dist = self.float_vec[2]
        if float_dist and not self._is_moving():
            if not self.rect.x % float(globs.GRID_SIZE):
                self.float_vec[0] = random.randrange(-float_dist, float_dist + 1, float_dist)
            else:
                self.float_vec[0] = -self.float_vec[0]

            if not self.rect.y % float(globs.GRID_SIZE):
                self.float_vec[1] = random.randrange(-float_dist, float_dist + 1,float_dist)
            else:
                self.float_vec[1] = -self.float_vec[1]

            self.move_vec[0] += self.float_vec[0]
            self.move_vec[1] += self.float_vec[1]

        self._handle_collisions()

    def _draw(self, surface):
        surface.blit(self.surface, self.rect)

    def _handle_collisions(self):
        for collision in self.collisions:
            if not collision['sprite'] in globs.sprites:
                self.collisions.remove(collision)
                continue

            if self.rect.colliderect(collision['sprite'].rect):
                collision['cb'](self, collision['sprite'])

    def _is_moving(self):
        if self.rect.x == self.move_vec[0] and self.rect.y == self.move_vec[1]:
            return False
        return True

    def _move(self, direction, distance = 1):
        if self._is_moving():
            return

        if direction == 'right' and not self.rect.x + roundup(self.rect.width, globs.GRID_SIZE) == globs.WIDTH:
            self.move_vec[0] += globs.GRID_SIZE * distance
        elif direction == 'left' and not self.rect.x == 0:
            self.move_vec[0] += -globs.GRID_SIZE * distance
        elif direction == 'up' and not self.rect.y == 0:
            self.move_vec[1] += -globs.GRID_SIZE * distance
        elif direction == 'down' and not self.rect.y + roundup(self.rect.height, globs.GRID_SIZE) == globs.HEIGHT:
            self.move_vec[1] += globs.GRID_SIZE * distance

    def move_keys(self, right = 'right', left = 'left', up = 'up', down = 'down'):
        if right:
            register_keydown(right, partial(self._move, 'right'))
        if left:
            register_keydown(left, partial(self._move, 'left'))
        if up:
            register_keydown(up, partial(self._move, 'up'))
        if down:
            register_keydown(down, partial(self._move, 'down'))

        return self

    def speed(self, speed):
        self.move_speed = int(speed)

        return self

    def float(self, distance = 0.25):
        self.float_vec[2] = int(globs.GRID_SIZE * distance)

        return self

    def when_collides(self, sprite, callback):
        self.collisions.append({ 'sprite': sprite, 'cb': callback })

        return self

    def scale(self, size):
        width = self.rect.width * size
        height = self.rect.height * size
        self.rect.width = width
        self.rect.height = height
        self.surface = pygame.transform.smoothscale(self.origin_surface, self.rect.size).convert_alpha()

        return self

    def destroy(self):
        globs.sprites.remove(self)

        return self
