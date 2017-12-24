import sys, random, math, pygame
from functools import partial
from .utils import register_keydown, register_keyup, animate, randrange_float, sign
from . import globs

class Sprite:
    def __init__(self, surface, rect, tag=None, name=None):
        if len(globs.sprites) >= 9000:
            sys.exit('Too many sprites! You\'re trying to spawn over 9,000!')
        self.surface = surface.convert_alpha()
        self.origin_surface = self.surface
        self.rect = rect
        self.virt_rect = [float(self.rect.x), float(self.rect.y), float(self.rect.width), float(self.rect.height)]
        self.surface = pygame.transform.scale(self.origin_surface, rect.size)
        self.needs_rotation = False
        self.move_speed = 5
        self.moving = False
        self.float_vec = (self.rect.x, self.rect.y)
        self.bounce_vec = (0, 0)
        self.sprite_scale = max(self.width, self.height)
        self.rotate_angle = 0
        self.collisions = []
        self.clicks = []
        self.alpha = 255
        self._pixelated = 0
        self.name = name
        self._tag = tag
        if tag not in globs.tags.keys():
            globs.tags[tag] = [self]
        else:
            globs.tags[tag].append(self)

    @property
    def pixelated(self):
        return self._pixelated

    @pixelated.setter
    def pixelated(self, value):
        self._pixelated = value
        self.pixelate(math.ceil(value))

    @property
    def x(self):
        return int(self.virt_rect[0] / globs.GRID_SIZE)

    @x.setter
    def x(self, value):
        self.needs_rotation = True
        self.virt_rect[0] = int(float(value) * globs.GRID_SIZE)

    @property
    def y(self):
        return int(self.virt_rect[1] / globs.GRID_SIZE)

    @y.setter
    def y(self, value):
        self.needs_rotation = True
        self.virt_rect[1] = int(float(value) * globs.GRID_SIZE)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x = int(value[0])
        self.y = int(value[1])

    @property
    def width(self):
        return self.virt_rect[2] / globs.GRID_SIZE

    @property
    def height(self):
        return self.virt_rect[3] / globs.GRID_SIZE

    @property
    def size(self):
        return self.sprite_scale

    @size.setter
    def size(self, value):
        self.needs_rotation = True
        self.sprite_scale = value

    @property
    def angle(self):
        return self.rotate_angle

    @angle.setter
    def angle(self, value):
        self.needs_rotation = True
        self.rotate_angle = value

    @property
    def tag(self):
        return self._tag

    @property
    def center(self):
        x, y, width, height = self.virt_rect[:]
        return (x + width/2.0)/ globs.GRID_SIZE, (y + height/2.0)/ globs.GRID_SIZE

    def _update(self, delta):
        if self.needs_rotation:
            self.rotate(0)
            self.needs_rotation = False
        self._handle_collisions()

    def _draw(self, surface):
        if self.alpha != 255:
            #http://www.nerdparadise.com/programming/pygameblitopacity
            temp = pygame.Surface((self.surface.get_width(), self.surface.get_height())).convert()
            temp.blit(surface, (-self.rect[0], -self.rect[1]))
            temp.blit(self.surface, (0, 0))
            temp.set_alpha(self.alpha)        
            surface.blit(temp, self.rect)            
        else:
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
        if self.virt_rect[0] + self.virt_rect[2] >= globs.WIDTH and self.bounce_vec[0] > 0:
            self.bounce(True, False)
        elif self.virt_rect[0] <= 0 and self.bounce_vec[0] < 0:
            self.bounce(True, False)

        if self.virt_rect[1] + self.virt_rect[3] >= globs.HEIGHT and self.bounce_vec[1] > 0:
            self.bounce(False, True)
        elif self.virt_rect[1] <= 0 and self.bounce_vec[1] < 0:
            self.bounce(False, True)

        x_dist = self.x
        if self.bounce_vec[0] >= 1:
            x_dist = globs.WIDTH / globs.GRID_SIZE - x_dist
        y_dist = self.y
        if self.bounce_vec[1] >= 1:
            y_dist = globs.HEIGHT / globs.GRID_SIZE - y_dist

        distance = min(x_dist, y_dist)
        time = self._calc_time((distance, distance))

        animate(self, time, self._update_bounce, x = self.x + distance * self.bounce_vec[0], y = self.y + distance * self.bounce_vec[1])

    def _handle_click(self, button):
        for click in self.clicks:
            if button == click['btn']:
                click['cb'](self)

    def _calc_time(self, vector, position = None):
        if not position:
            position = self.virt_rect[0:2]
        cur_x, cur_y = position
        new_x = cur_x + vector[0] * globs.GRID_SIZE
        new_y = cur_y + vector[1] * globs.GRID_SIZE
        distance = math.sqrt((new_x - cur_x)**2 + (new_y - cur_y)**2)
        time = (abs(distance) / self.move_speed) / 60

        return time

    def _complete_move(self, callback = None):
        self.moving = False
        if callback:
            callback()

    def fade(self, time=1, **kwargs):
        #callback = kwargs.get('callback', None)
        animate(self, time, partial(self.destroy), pixelated = 100, alpha = 0)

    def move(self, vector, **kwargs):
        self.moving = True
        callback = kwargs.get('callback', None)
        precondition = kwargs.get('precondition', None)

        x_dest = int(self.x + vector[0])
        y_dest = int(self.y + vector[1])
        time = self._calc_time(vector)
        if precondition == None or precondition('move', self, (x_dest, y_dest)):
            animate(self, time, partial(self._complete_move, callback), x = x_dest, y = y_dest)
        else:
            animate(self, time, partial(self._complete_move, callback), x = self.x, y = self.y)
        return self

    def move_to(self, *points, **kwargs):
        #if self.moving:
        #    return self
        self.moving = True

        callback = partial(self._complete_move, kwargs.get('callback', None))
        times = []

        for index, point in enumerate(points):
            if index == 0:
                prev_point = self.pos
            else:
                prev_point = points[index - 1]
            vector = (point[0] - prev_point[0], point[1] - prev_point[1])
            time = self._calc_time(vector, prev_point)
            times.append(time)

        for point in reversed(points):
            time = times.pop(-1)
            callback = partial(animate, self, time, callback, x = point[0], y = point[1])

        callback()

    def _continue_key(self, key, distance, **kwargs):
        precondition = kwargs.get('precondition', None)
        if key in globs.keys_pressed:
            self.move(distance, callback = partial(self._continue_key, key, distance, precondition = precondition), precondition = precondition)

    def keys(self, right = 'right', left = 'left', up = 'up', down = 'down', **kwargs):
        precondition = kwargs.get('precondition', None)
        distance = kwargs.get('spaces', 1)

        register_key = None
        if kwargs.get('direction', 'down') == 'down':
            register_key = register_keydown
        else:
            register_key = register_keyup

        if right:
            register_key(right, partial(self.move, (1 * distance, 0), callback = partial(self._continue_key, right, (1 * distance, 0), precondition = precondition), precondition = precondition))
        if left:
            register_key(left, partial(self.move, (-1 * distance, 0), callback = partial(self._continue_key, left, (-1 * distance, 0), precondition = precondition), precondition = precondition))
        if up:
            register_key(up, partial(self.move, (0, -1 * distance), callback = partial(self._continue_key, up, (0, -1 * distance), precondition = precondition), precondition = precondition))
        if down:
            register_key(down, partial(self.move, (0, 1 * distance), callback = partial(self._continue_key, down, (0, 1 * distance), precondition = precondition), precondition = precondition))

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

        animate(self, 0.016, partial(self._update_float, distance, time))

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

    def pixelate(self, pixel_size = 10):
        x_start = 0
        x_range = int(self.virt_rect[2])
        y_start = 0
        y_range = int(self.virt_rect[3])

        for x_offset in range(x_start, x_range, pixel_size):
            for y_offset in range(y_start, y_range, pixel_size):
                avg_color = pygame.transform.average_color(self.surface, (x_offset, y_offset, pixel_size, pixel_size))
                pygame.draw.rect(self.surface, avg_color, (x_offset, y_offset, pixel_size, pixel_size))

        return self

    def rotate(self, angle):

        self.rotate_angle += angle
        if self.rotate_angle > 360:
            self.rotate_angle -= 360

        x, y, width, height = self.virt_rect[:]
        center = (x + width/2), (y + height/2)

        scale_width = self.sprite_scale * globs.GRID_SIZE
        scale_height = self.sprite_scale * globs.GRID_SIZE

        self.surface = pygame.transform.scale(self.origin_surface, (int(scale_width), int(scale_height)))
        self.surface = pygame.transform.rotate(self.surface, self.rotate_angle)

        self.rect = self.surface.get_rect(center=center)
        new_rect = self.surface.get_rect()
        self.virt_rect[2] = new_rect[2]
        self.virt_rect[3] = new_rect[3]

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
        self.sprite_scale = self.sprite_scale * size

        self.surface = pygame.transform.smoothscale(self.origin_surface, (int(self.virt_rect[2]), int(self.virt_rect[3]))).convert_alpha()

        return self

    def bounce(self, bounce_x = True, bounce_y = True):
        x_dir, y_dir = self.bounce_vec
        if bounce_x:
            x_dir = -x_dir
        if bounce_y:
            y_dir = -y_dir
        self.bounce_vec = x_dir, y_dir

        for animation in globs.animations:
            if animation.obj == self and animation.callback == self._update_bounce:
                globs.animations.remove(animation)
                break

        self._update_bounce()

        return self

    def bouncy(self):
        if self.moving:
            return self
        self.moving = True

        self.bounce_vec = (random.choice([-1, 1]), random.choice([-1, 1]))
        animate(self, 0.016, self._update_bounce)

        return self

    def pulse(self, time = 1, size = None):
        if not size:
            size = self.size * 2
        animate(self, time, partial(self.pulse, time, self.size), size = size)

        return self

    def spin(self, time = 1, **kwargs):
        #if self.moving and not kwargs.get('spinning', False):
        #    return self
        self.moving = True
        animate(self, time, partial(self.spin, time, spinning = True), angle = self.angle + 360)

        return self

    def destroy(self, *args):
        globs.sprites.remove(self)
        globs.tags[self._tag].remove(self)
        return self

    def wander(self, callback, time = 1):
        callback(self)

        animate(self, time, partial(self.wander, callback, time))
        return self
