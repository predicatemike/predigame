import sys, os, random, math, pygame
from functools import partial
from pygame.locals import *

background_color = (220, 220, 220)
sprites = []
show_grid = False
keys_registered = {
    'keydown': {},
    'keyup': {}
}

# hack for Python3 compatibility
try:
    basestring
except:
    basestring = str

# shapes
RECT = 'rect'
CIRCLE = 'circle'

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (200, 0, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
CYAN = (0, 200, 200)
PINK = (200, 0, 200)
PURPLE = (155, 0, 255)

class Sprite:
    def __init__(self, surface, rect):
        self.surface = surface.convert_alpha()
        self.rect = rect
        self.move_speed = 5
        self.move_vec = [0, 0, 0] # x distance, y distance, current velocity
        self.float_vec = [0, 0, 0] # x distance, y distance, total offset distance

    def update(self):
        move_vel = self.move_vec[2]
        float_dist = self.float_vec[2]

        if move_vel:
            x_move = self.move_vec[0] // move_vel
            y_move = self.move_vec[1] // move_vel
            self.rect.x += x_move
            self.rect.y += y_move
            self.move_vec[0] -= x_move
            self.move_vec[1] -= y_move
            self.move_vec[2] -= 1

        if float_dist and not move_vel:
            if not self.rect.x % float(GRID_SIZE):
                self.float_vec[0] = random.randrange(-float_dist, float_dist + 1, float_dist)
            else:
                self.float_vec[0] = -self.float_vec[0]

            if not self.rect.y % float(GRID_SIZE):
                self.float_vec[1] = random.randrange(-float_dist, float_dist + 1,float_dist)
            else:
                self.float_vec[1] = -self.float_vec[1]

            self.move_vec[0] += self.float_vec[0]
            self.move_vec[1] += self.float_vec[1]
            self.move_vec[2] = self.move_speed

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def move(self, direction, distance = 1):
        if self.move_vec[2]:
            return

        if direction == 'right' and not self.rect.x + roundup(self.rect.width, GRID_SIZE) == WIDTH:
            self.move_vec[0] += GRID_SIZE * distance
        elif direction == 'left' and not self.rect.x == 0:
            self.move_vec[0] += -GRID_SIZE * distance
        elif direction == 'up' and not self.rect.y == 0:
            self.move_vec[1] += -GRID_SIZE * distance
        elif direction == 'down' and not self.rect.y + roundup(self.rect.height, GRID_SIZE) == HEIGHT:
            self.move_vec[1] += GRID_SIZE * distance

        self.move_vec[2] = self.move_speed

    def move_keys(self, right = 'right', left = 'left', up = 'up', down = 'down'):
        if right:
            register_keydown(right, partial(self.move, 'right'))
        if left:
            register_keydown(left, partial(self.move, 'left'))
        if up:
            register_keydown(up, partial(self.move, 'up'))
        if down:
            register_keydown(down, partial(self.move, 'down'))

        return self

    def speed(self, speed):
        self.move_speed = speed

        return self

    def float(self, distance = 0.25):
        self.float_vec[2] = GRID_SIZE * distance

        return self

def init(width = 800, height = 800, title = 'PrediGame', **kwargs):
    global WIDTH, HEIGHT, FPS, GRID_SIZE, SURF, clock

    WIDTH, HEIGHT = width, height
    FPS = kwargs.get('fps', 60)
    GRID_SIZE = kwargs.get('grid', 100)

    pygame.init()
    pygame.display.set_caption(title)
    SURF = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    SURF.fill((0, 0, 0))
    loading_font = pygame.font.Font(None, 72)
    SURF.blit(loading_font.render('LOADING...', True, (235, 235, 235)), (25, 25))
    pygame.display.update()

def create_image(path, pos, size):
    image = pygame.image.load(path)
    rect = image.get_rect()
    rect.topleft = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE

    new_width = 0
    new_height = 0
    if rect.width >= rect.height:
        new_width = size * float(GRID_SIZE)
        new_height = rect.height * (new_width / rect.width)
    elif rect.width < rect.height:
        new_height = size * float(GRID_SIZE)
        new_width = rect.width * (new_height / rect.height)
    rect.size = new_width, new_height
    surface = pygame.transform.scale(image, rect.size)

    return Sprite(surface, rect)

def create_rectangle(color, pos, size, outline):
    rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, size[0] * GRID_SIZE, size[1] * GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(background_color)
    surface.set_colorkey(background_color)
    pygame.draw.rect(surface, color, (0, 0, rect.width, rect.height), outline)

    return Sprite(surface, rect)

def create_circle(color, pos, size, outline):
    rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, size * GRID_SIZE, size * GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(background_color)
    surface.set_colorkey(background_color)
    pygame.draw.circle(surface, color, (rect.width // 2, rect.height // 2), rect.width // 2, outline)

    return Sprite(surface, rect)

def img(name = None, pos = None, size = 1):
    if name:
        path = 'images/' + name + '.'
        if os.path.isfile(path + 'png'):
            path += 'png'
        elif os.path.isfile(path + 'jpg'):
            path += 'jpg'
        elif os.path.isfile(path + 'jpeg'):
            path += 'jpeg'
        elif os.path.isfile(path + 'gif'):
            path += 'gif'
        else:
            path = 'images/__error__.png'
    else:
        images = []
        for image in os.listdir('images/'):
            if image.endswith('.png') or image.endswith('.jpg') or image.endswith('.jpeg') or images.endswith('.gif'):
                images.append(image)
        path = 'images/' + random.choice(images)

    if not pos:
        pos = rand_pos()

    image = create_image(path, pos, size)
    sprites.append(image)
    return sprites[-1]

def shape(shape = None, color = None, pos = None, size = (1, 1), **kwargs):
    if not shape:
        shape = random.choice([CIRCLE, RECT])

    if not color:
        color = rand_color()

    if not pos:
        pos = rand_pos()

    outline = kwargs.get('outline', 0)

    if shape == 'circle':
        shape = create_circle(color, pos, size[0], outline)
    elif shape == 'rect':
        shape = create_rectangle(color, pos, size, outline)
    else:
        print('Shape, ' + shape + ', is not a valid shape name')
        return False

    sprites.append(shape)
    return sprites[-1]

def grid():
    global show_grid
    show_grid = True

def register_keydown(key, callback):
    if key in keys_registered['keydown']:
        keys_registered['keydown'][key].add(callback)
    else:
        keys_registered['keydown'][key] = set([callback])

def rand_pos():
    x = random.randrange(0, WIDTH / GRID_SIZE)
    y = random.randrange(0, HEIGHT / GRID_SIZE)
    return x, y

def rand_color():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    if (r, g, b) == background_color:
        r, g, b = rand_color()
    return r, g, b

def roundup(num, step):
    return int(math.ceil(num / float(step))) * step

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(SURF, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(SURF, BLACK, (0, y), (WIDTH, y))

def update():
    for sprite in sprites:
        sprite.update()

def draw(SURF):
    SURF.fill(background_color)

    for sprite in sprites:
        sprite.draw(SURF)

    if show_grid:
        draw_grid()

def main_loop():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            key = pygame.key.name(event.key)
            if key in keys_registered['keydown']:
                for callback in keys_registered['keydown'][key]:
                    callback()

            if key == 'escape':
                pygame.event.post(pygame.event.Event(QUIT))

        if event.type == KEYUP:
            key = pygame.key.name(event.key)
            if key in keys_registered['keyup']:
                for callback in keys_registered['keyup'][key]:
                    callback()

    update()
    draw(SURF)

    pygame.display.update()
    clock.tick(FPS)
