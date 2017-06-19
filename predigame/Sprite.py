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
        self.virt_rect = [float(self.rect.x), float(self.rect.y), float(self.rect.width), float(self.rect.height)]
        self.surface = pygame.transform.scale(self.origin_surface, rect.size)
        self.move_speed = 5
        self.move_method = None
        self.vel = (0, 0)
        self.move_pos = [self.rect.x, self.rect.y]
        self.float_vec = [self.rect.x, self.rect.y, 0]
        self.collisions = []
        self.clicks = []

    @property
    def x(self):
        return self.virt_rect[0] / globs.GRID_SIZE

    @x.setter
    def x(self, value):
        self.virt_rect[0] = float(value) * globs.GRID_SIZE

    @property
    def y(self):
        return self.virt_rect[1] / globs.GRID_SIZE

    @y.setter
    def y(self, value):
        self.virt_rect[1] = float(value) * globs.GRID_SIZE

    @property
    def pos(self):
        return self.x, self.y

    @property
    def width(self):
        return self.virt_rect[2] / globs.GRID_SIZE

    @property
    def height(self):
        return self.virt_rect[3] / globs.GRID_SIZE

    @property
    def size(self):
        return max(self.width, self.height)

    @size.setter
    def size(self, value):
        new_width = 0
        new_height = 0
        if self.virt_rect[2] >= self.virt_rect[3]:
            new_width = float(value) * globs.GRID_SIZE
            new_height = self.virt_rect[3] * (new_width / self.virt_rect[2])
        elif self.virt_rect[2] < self.virt_rect[3]:
            new_height = float(value) * globs.GRID_SIZE
            new_width = self.virt_rect[2] * (new_height / self.virt_rect[3])

        center = self.virt_rect[0] + self.virt_rect[2] / 2, self.virt_rect[1] + self.virt_rect[3] / 2
        self.virt_rect[2] = new_width
        self.virt_rect[3] = new_height
        self.virt_rect[0] = center[0] - self.virt_rect[2] / 2
        self.virt_rect[1] = center[1] - self.virt_rect[3] / 2

        self.surface = pygame.transform.smoothscale(self.origin_surface, self.rect.size).convert_alpha()

    def _update(self, delta):
        if self.move_method:
            x_vel, y_vel = self.vel

            x_dir = 1
            if x_vel:
                x_dir = x_vel / abs(x_vel)
            x_vel = self.move_speed * x_dir

            y_dir = 1
            if y_vel:
                y_dir = y_vel / abs(y_vel)
            y_vel = self.move_speed * y_dir

            self.vel = x_vel * (delta / 16), y_vel * (delta / 16)
            self.move_method()

            self.virt_rect[0] += self.vel[0]
            self.virt_rect[1] += self.vel[1]

        self.rect.topleft = self.virt_rect[0:2]
        self.rect.size = self.virt_rect[2:]
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

        if abs(x_dist) <= abs(x_vel):
            x_vel = x_dist
        else:
            x_vel = (x_dist / abs(x_dist)) * abs(x_vel)

        if abs(y_dist) <= abs(y_vel):
            y_vel = y_dist
        else:
            y_vel = (y_dist / abs(y_dist)) * abs(y_vel)

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

        self.move_pos = [self.rect.x, self.rect.y]
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
        self.move_speed = speed

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

    def flip(self, flip_x = True, flip_y = False):
        self.origin_surface = pygame.transform.flip(self.origin_surface, flip_x, flip_y)
        self.surface = pygame.transform.flip(self.surface, flip_x, flip_y)

        return self

    def scale(self, size):
        if self.rect.width > globs.WIDTH and self.rect.height > globs.HEIGHT:
            return self
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

    def pulse(self, time = 1, size = None):
        if not size:
            size = self.size * 2
        animate(self, time, partial(self.pulse, time, self.size), size = size)

        return self

    def destroy(self, *args):
        globs.sprites.remove(self)

        return self
