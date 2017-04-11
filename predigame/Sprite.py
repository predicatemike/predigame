import sys, random, pygame
from functools import partial
from .utils import *
from . import globs

class Sprite:
    def __init__(self, surface, rect):
        if len(globs.sprites) >= 9000:
            sys.exit('Too many sprites! You\'re trying to spawn over 9,000!')
        self.surface = surface.convert_alpha()
        self.origin_surface = self.surface
        self.rect = rect
        self.move_speed = 5
        self.vel = (0, 0)
        self.move_vec = [self.rect.x, self.rect.y]
        self.float_vec = [0, 0, 0] # x distance, y distance, offset distance
        self.collisions = []

    def _update(self):
        x_vel, y_vel = self.vel
        if x_vel and not abs(x_vel) == self.move_speed:
            x_vel = self.move_speed * (x_vel / abs(x_vel))
        if y_vel and not abs(y_vel) == self.move_speed:
            y_vel = self.move_speed * (y_vel / abs(y_vel))

        self.vel = (x_vel, y_vel)

        self.move_vec[0] += self.vel[0]
        self.move_vec[1] += self.vel[1]

        self._update_bounce()

        self._update_float()

        self._update_move()

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
                break # only handle one collision per frame (for now)

    def _is_moving(self):
        if self.rect.x == self.move_vec[0] and self.rect.y == self.move_vec[1]:
            return False
        return True

    def _update_move(self):
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

    def _update_bounce(self):
        if self.rect.x + self.rect.width > globs.WIDTH and self.vel[0] > 0:
            self.bounce(True, False)
        elif self.rect.x < 0 and self.vel[0] < 0:
            self.bounce(True, False)

        if self.rect.y + self.rect.height > globs.HEIGHT and self.vel[1] > 0:
            self.bounce(False, True)
        elif self.rect.y < 0 and self.vel[1] < 0:
            self.bounce(False, True)

    def _update_float(self):
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

    def keys(self, right = 'right', left = 'left', up = 'up', down = 'down'):
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
        if float(distance).is_integer():
            distance += 0.1
        self.float_vec[2] = int(globs.GRID_SIZE * distance)

        return self

    def collides(self, sprites, callback):
        if not isinstance(sprites, list):
            sprites = [sprites]

        for sprite in sprites:
            if sprite == self:
                continue
            self.collisions.append({ 'sprite': sprite, 'cb': callback })

        return self

    def scale(self, size):
        width = self.rect.width * size
        height = self.rect.height * size
        self.rect.width = width
        self.rect.height = height
        self.surface = pygame.transform.smoothscale(self.origin_surface, self.rect.size).convert_alpha()

        return self

    def bounce(self, bounce_x = True, bounce_y = True):
        x_vel, y_vel = self.vel
        if bounce_x:
            x_vel = -x_vel
        if bounce_y:
            y_vel = -y_vel

        self.vel = x_vel, y_vel

        return self

    def bouncy(self):
        if not self._is_moving():
            x_vel = random.randrange(-self.move_speed, self.move_speed + 1, self.move_speed * 2)
            y_vel = random.randrange(-self.move_speed, self.move_speed + 1, self.move_speed * 2)
            self.vel = x_vel, y_vel

        return self

    def destroy(self):
        globs.sprites.remove(self)

        return self
