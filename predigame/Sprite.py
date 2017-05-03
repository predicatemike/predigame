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
        self.move_method = None
        self.vel = (0, 0)
        self.move_pos = [self.rect.x, self.rect.y]
        self.float_vec = [self.rect.x, self.rect.y, 0]
        self.collisions = []
        self.clicks = []

    @property
    def pos(self):
        return self.rect.x / globs.GRID_SIZE, self.rect.y / globs.GRID_SIZE

    @property
    def width(self):
        return self.rect.width / globs.GRID_SIZE

    @property
    def height(self):
        return self.rect.height / globs.GRID_SIZE

    def _update(self):
        if self.move_method:
            self.move_method()

            x_vel, y_vel = self.vel
            if x_vel and not abs(x_vel) == self.move_speed:
                x_vel = self.move_speed * (x_vel / abs(x_vel))
            if y_vel and not abs(y_vel) == self.move_speed:
                y_vel = self.move_speed * (y_vel / abs(y_vel))

            self.vel = (x_vel, y_vel)

            self.rect.x += self.vel[0]
            self.rect.y += self.vel[1]

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

    def _update_move(self):
        if self.rect.x == self.move_pos[0] and self.rect.y == self.move_pos[1] and self.move_method == self._update_move:
            self.move_method = None

        x_dist = self.move_pos[0] - self.rect.x
        y_dist = self.move_pos[1] - self.rect.y
        x_vel, y_vel = self.vel
        if abs(x_dist) < self.move_speed:
            x_vel = x_dist
        else:
            x_vel = (x_dist) / abs(x_dist) * self.move_speed

        if abs(y_dist) < self.move_speed:
            y_vel = y_dist
        else:
            y_vel = (y_dist) / abs(y_dist) * self.move_speed

        self.vel = x_vel, y_vel

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
        float_x, float_y, float_dist = self.float_vec

        if abs(self.rect.x - float_x) >= float_dist:
            self.move_pos[0] = float_x
        elif self.rect.x == float_x:
            self.move_pos[0] += random.randrange(-float_dist, float_dist + 1, float_dist)

        if abs(self.rect.y - float_y) >= float_dist:
            self.move_pos[1] = float_y
        elif self.rect.y == float_y:
            self.move_pos[1] += random.randrange(-float_dist, float_dist + 1,float_dist)

        self._update_move()

    def _handle_click(self, button):
        for click in self.clicks:
            if button == click['btn']:
                click['cb'](self)

    def move(self, vector):
        if self.move_method:
            return self

        self.move_pos[0] += vector[0] * globs.GRID_SIZE
        self.move_pos[1] += vector[1] * globs.GRID_SIZE

        self.move_method = self._update_move

        return self

    def keys(self, right = 'right', left = 'left', up = 'up', down = 'down', **kwargs):
        distance = kwargs.get('spaces', 1)
        if right:
            register_keydown(right, partial(self.move, (1 * distance, 0)))
        if left:
            register_keydown(left, partial(self.move, (-1 * distance, 0)))
        if up:
            register_keydown(up, partial(self.move, (0, -1 * distance)))
        if down:
            register_keydown(down, partial(self.move, (0, 1 * distance)))

        return self

    def speed(self, speed):
        self.move_speed = int(speed)

        return self

    def float(self, distance = 0.25):
        self.float_vec = self.rect.x, self.rect.y, int(globs.GRID_SIZE * distance)
        self.move_method = self._update_float

        return self

    def collides(self, sprites, callback):
        if not isinstance(sprites, list):
            sprites = [sprites]

        for sprite in sprites:
            if sprite == self:
                continue
            self.collisions.append({ 'sprite': sprite, 'cb': callback })

        return self

    def clicked(self, callback, button = 1):
        self.clicks.append({'btn': button, 'cb': callback})

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
        x_vel = random.randrange(-self.move_speed, self.move_speed + 1, self.move_speed * 2)
        y_vel = random.randrange(-self.move_speed, self.move_speed + 1, self.move_speed * 2)
        self.vel = x_vel, y_vel
        self.move_method = self._update_bounce

        return self

    def destroy(self, *args):
        globs.sprites.remove(self)

        return self
