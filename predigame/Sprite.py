import sys, random, math, pygame
from functools import partial
from .utils import register_keydown, animate, randrange_float, sign
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
        self.moving = False
        self.float_vec = (self.rect.x, self.rect.y)
        self.bounce_vec = (0, 0)
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

        self.surface = pygame.transform.smoothscale(self.origin_surface, (int(self.virt_rect[2]), int(self.virt_rect[3]))).convert_alpha()

    def _update(self, delta):
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

    def _update_float(self, distance, time):
        float_x, float_y = self.float_vec
        time = self._calc_time((distance, distance))

        if self.virt_rect[0] == float_x:
            move_x = randrange_float(-distance, distance, distance * 2)
        else:
            move_x = -distance * sign(self.virt_rect[0] - float_x)

        if self.virt_rect[1] == float_y:
            move_y = randrange_float(-distance, distance, distance * 2)
        else:
            move_y = -distance * sign(self.virt_rect[1] - float_y)

        animate(self, time, partial(self._update_float, distance, time), x = self.x + move_x, y = self.y + move_y)

    def _update_bounce(self):
        if self.virt_rect[0] + self.virt_rect[2] > globs.WIDTH and self.bounce_vec[0] > 0:
            self.bounce(True, False)
        elif self.virt_rect[0] < 0 and self.bounce_vec[0] < 0:
            self.bounce(True, False)

        if self.virt_rect[1] + self.virt_rect[3] > globs.HEIGHT and self.bounce_vec[1] > 0:
            self.bounce(False, True)
        elif self.virt_rect[1] < 0 and self.bounce_vec[1] < 0:
            self.bounce(False, True)

        distance = self.move_speed / globs.GRID_SIZE
        time = self._calc_time((distance, distance))

        animate(self, time, partial(self._update_bounce), x = self.x + distance * self.bounce_vec[0], y = self.y + distance * self.bounce_vec[1])

    def _handle_click(self, button):
        for click in self.clicks:
            if button == click['btn']:
                click['cb'](self)

    def _calc_time(self, vector):
        cur_x, cur_y = self.virt_rect[0:2]
        new_x = cur_x + vector[0] * globs.GRID_SIZE
        new_y = cur_y + vector[1] * globs.GRID_SIZE
        distance = math.sqrt((new_x - cur_x)**2 + (new_y - cur_y)**2)
        time = (abs(distance) / self.move_speed) / 60

        return time

    def move(self, vector):
        if self.moving:
            return self
        self.moving = True

        x_dest = self.x + vector[0]
        y_dest = self.y + vector[1]
        time = self._calc_time(vector)

        animate(self, time, lambda: setattr(self, 'moving', False), x = x_dest, y = y_dest)

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
        self.move_speed = abs(speed)

        return self

    def float(self, distance = 0.25):
        if self.moving:
            return self
        self.moving = True

        self.float_vec = (self.virt_rect[0], self.virt_rect[1])
        time = self._calc_time((distance, distance))

        animate(self, time, partial(self._update_float, distance, time), x = self.x + distance, y = self.y + distance)

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
        if self.virt_rect[2] > globs.WIDTH and self.virt_rect[3] > globs.HEIGHT:
            return self
        width = self.virt_rect[2] * size
        height = self.virt_rect[3] * size

        self.virt_rect[2] = width
        self.virt_rect[3] = height
        self.surface = pygame.transform.smoothscale(self.origin_surface, (int(self.virt_rect[2]), int(self.virt_rect[3]))).convert_alpha()

        return self

    def bounce(self, bounce_x = True, bounce_y = True):
        x_dir, y_dir = self.bounce_vec
        if bounce_x:
            x_dir = -x_dir
        if bounce_y:
            y_dir = -y_dir

        self.bounce_vec = x_dir, y_dir

        return self

    def bouncy(self):
        if self.moving:
            return self
        self.moving = True

        self.bounce_vec = (random.choice([-1, 1]), random.choice([-1, 1]))
        distance = self.move_speed / globs.GRID_SIZE
        time = self._calc_time((distance, distance))

        animate(self, time, partial(self._update_bounce), x = self.x + distance * self.bounce_vec[0], y = self.y + distance * self.bounce_vec[1])

        return self

    def pulse(self, time = 1, size = None):
        if not size:
            size = self.size * 2
        animate(self, time, partial(self.pulse, time, self.size), size = size)

        return self

    def destroy(self, *args):
        globs.sprites.remove(self)

        return self
