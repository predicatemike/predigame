import sys, os, random, pygame
from pygame.locals import *
from . import globs
from .utils import *
from .Sprite import Sprite

show_grid = False

def init(width = 800, height = 800, title = 'PrediGame', **kwargs):
    global WIDTH, HEIGHT, FPS, GRID_SIZE, SURF, clock

    WIDTH, HEIGHT = width, height
    FPS = kwargs.get('fps', 60)
    GRID_SIZE = kwargs.get('grid', 50)

    globs.init(WIDTH, HEIGHT, GRID_SIZE)

    pygame.mixer.pre_init(22050, -16, 2, 1024) # sound delay fix
    pygame.init()
    pygame.display.set_caption(title)
    SURF = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    SURF.fill((0, 0, 0))
    loading_font = pygame.font.Font(None, 72)
    SURF.blit(loading_font.render('LOADING...', True, (235, 235, 235)), (25, 25))
    pygame.display.update()

def _create_image(path, pos, size):
    image = pygame.image.load(path)
    rect = image.get_rect()
    rect.topleft = pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE

    new_width = 0
    new_height = 0
    if rect.width >= rect.height:
        new_width = size * float(globs.GRID_SIZE)
        new_height = rect.height * (new_width / rect.width)
    elif rect.width < rect.height:
        new_height = size * float(globs.GRID_SIZE)
        new_width = rect.width * (new_height / rect.height)
    rect.size = new_width, new_height
    surface = pygame.transform.scale(image, rect.size)

    return Sprite(surface, rect)

def _create_rectangle(color, pos, size, outline):
    rect = pygame.Rect(pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE, size[0] * globs.GRID_SIZE, size[1] * globs.GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(globs.background_color)
    surface.set_colorkey(globs.background_color)
    pygame.draw.rect(surface, color, (0, 0, rect.width, rect.height), outline)

    return Sprite(surface, rect)

def _create_circle(color, pos, size, outline):
    rect = pygame.Rect(pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE, size * globs.GRID_SIZE, size * globs.GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(globs.background_color)
    surface.set_colorkey(globs.background_color)
    pygame.draw.circle(surface, color, (rect.width // 2, rect.height // 2), rect.width // 2, outline)

    return Sprite(surface, rect)

def _create_ellipse(color, pos, size, outline):
    rect = pygame.Rect(pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE, size[0] * globs.GRID_SIZE, size[1] * globs.GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(globs.background_color)
    surface.set_colorkey(globs.background_color)
    pygame.draw.ellipse(surface, color, (0, 0, rect.width, rect.height), outline)

    return Sprite(surface, rect)

def img(name = None, pos = None, size = 1):
    error_path = os.path.join(os.path.dirname(__file__), '__error__.png')

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
            path = error_path
    else:
        if os.path.isdir('images/'):
            images = []
            for image in os.listdir('images/'):
                if image.endswith('.png') or image.endswith('.jpg') or image.endswith('.jpeg') or images.endswith('.gif'):
                    images.append(image)
            if len(images):
                path = 'images/' + random.choice(images)
            else:
                path = error_path
        else:
            path = error_path

    if not pos:
        pos = rand_pos()

    image = _create_image(path, pos, size)
    globs.sprites.append(image)
    return globs.sprites[-1]

def shape(shape = None, color = None, pos = None, size = (1, 1), **kwargs):
    if not shape:
        shape = random.choice(['circle', 'rect', 'ellipse'])

    if not color:
        color = rand_color()

    if not pos:
        pos = rand_pos()

    outline = kwargs.get('outline', 0)

    if shape == 'circle':
        if not isinstance(size, (int, float)):
            size = size[0]
        shape = _create_circle(color, pos, size, outline)
    elif shape == 'rect':
        shape = _create_rectangle(color, pos, size, outline)
    elif shape == 'ellipse':
        shape = _create_ellipse(color, pos, size, outline)
    else:
        print('Shape, ' + shape + ', is not a valid shape name')
        return False

    globs.sprites.append(shape)
    return globs.sprites[-1]

def grid():
    global show_grid
    show_grid = True

def _draw_grid():
    for x in range(0, globs.WIDTH, globs.GRID_SIZE):
        pygame.draw.line(SURF, (0, 0, 0), (x, 0), (x, globs.HEIGHT))
    for y in range(0, globs.HEIGHT, globs.GRID_SIZE):
        pygame.draw.line(SURF, (0, 0, 0), (0, y), (globs.WIDTH, y))

def _update():
    for sprite in globs.sprites:
        sprite._update()

def _draw(SURF):
    SURF.fill(globs.background_color)

    for sprite in globs.sprites:
        sprite._draw(SURF)

    if show_grid:
        _draw_grid()

def main_loop():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            key = pygame.key.name(event.key)
            if key in globs.keys_registered['keydown']:
                for callback in globs.keys_registered['keydown'][key]:
                    callback()

            if key == 'escape':
                pygame.event.post(pygame.event.Event(QUIT))

        if event.type == KEYUP:
            key = pygame.key.name(event.key)
            if key in globs.keys_registered['keyup']:
                for callback in globs.keys_registered['keyup'][key]:
                    callback()

    _update()
    _draw(SURF)

    pygame.display.update()
    clock.tick(FPS)
