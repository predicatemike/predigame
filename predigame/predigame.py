import sys, os, random, datetime, mimetypes, pygame
from time import time as get_time
from pygame.locals import *
from . import globs
from .utils import load_module, register_keydown, rand_pos, rand_color, roundup, animate
from .Sprite import Sprite

show_grid = False
update_game = True
sounds = {}
images = {}

def init(path, width = 800, height = 800, title = 'PrediGame', **kwargs):
    global RUN_PATH, WIDTH, HEIGHT, FPS, GRID_SIZE, SURF, clock, start_time, sounds

    RUN_PATH = path
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

    images['__error__'] = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images', 'error.png'))
    images['__screenshot__'] = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images', 'screenshot.png'))

    start_time = get_time()

def _create_image(name, pos, size):
    img = images[name]
    rect = img.get_rect()
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

    return Sprite(img, rect)

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

def image(name = None, pos = None, size = 1):
    if not name:
        if os.path.isdir('images/'):
            imgs = []
            mime_types = ('image/png', 'image/jpeg', 'image/gif')
            for img in os.listdir('images/'):
                if mimetypes.guess_type(img)[0] in mime_types:
                    imgs.append(img)
            if len(imgs):
                name = os.path.splitext(random.choice(imgs))[0]
            else:
                name = '__error__'
        else:
            name = '__error__'

    if not name in images:
        for img in os.listdir('images/'):
            if os.path.splitext(img)[0] == name:
                try:
                    img = pygame.image.load(os.path.join('images', img))
                    images[name] = img
                except:
                    continue

                break
        else: # if no image is found and the loop continues ubroken
            name = '__error__'

    if not pos:
        pos = rand_pos(size - 1, size - 1)

    img = _create_image(name, pos, size)
    globs.sprites.append(img)
    return globs.sprites[-1]

def shape(shape = None, color = None, pos = None, size = (1, 1), **kwargs):
    if not shape:
        shape = random.choice(['circle', 'rect', 'ellipse'])

    if not color:
        color = rand_color()

    if isinstance(size, (int, float)):
        size = (size, size)

    if not pos:
        pos = rand_pos(size[0] - 1, size[1] - 1)

    outline = kwargs.get('outline', 0)

    if shape == 'circle':
        shape = _create_circle(color, pos, size[0], outline)
    elif shape == 'rect':
        shape = _create_rectangle(color, pos, size, outline)
    elif shape == 'ellipse':
        shape = _create_ellipse(color, pos, size, outline)
    else:
        print('Shape, ' + shape + ', is not a valid shape name')
        return False

    globs.sprites.append(shape)
    return globs.sprites[-1]

def text(string, color = None, pos = None, size = 1):
    string = str(string)
    size = int(size * globs.GRID_SIZE)
    font = pygame.font.Font(None, size)
    font_width, font_height = font.size(string)

    if not color:
        color = rand_color()

    if not pos:
        pos = (globs.WIDTH / 2 -  font_width / 2) / globs.GRID_SIZE, (globs.HEIGHT / 2 - font_height / 2) / globs.GRID_SIZE

    pos = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE

    surface = font.render(string, True, color)
    text = Sprite(surface, pygame.Rect(pos[0], pos[1], font_width, font_height))

    globs.sprites.append(text)
    return globs.sprites[-1]

def sound(name = None, plays = 1, duration = 0):
    plays = plays - 1
    duration = int(duration * 1000)

    path = None
    snd_exts = ('wav', 'ogg')
    if name:
        path = 'sounds/' + name + '.'
        for ext in snd_exts:
            if os.path.isfile(path + ext.lower()):
                path += ext.lower()
                break

            if os.path.isfile(path + ext.upper()):
                path += ext.upper()
                break
        else:
            print('Error: Sound ' + name + ' not found')
    else:
        if os.path.isdir('sounds/'):
            snds = []
            for snd in os.listdir('sounds/'):
                for ext in snd_exts:
                    if snd.lower().endswith(ext):
                        snds.append(snd)
            if len(snds):
                path = 'sounds/' + random.choice(snds)
                name = path[7:-4]
            else:
                print('Error: No sound files found')
        else:
            print('Error: Sounds directory does not exist')

    if not name in sounds:
        snd = pygame.mixer.Sound(path)
        sounds[name] = snd

    sounds[name].play(plays, duration)

def grid():
    global show_grid
    show_grid = True

def time():
    return float('%.3f'%(get_time() - start_time))

def destroyall():
    del globs.sprites[:]

def pause():
    global update_game
    update_game = False

def resume():
    global update_game
    update_game = True

def reset():
    destroyall()
    globs.keys_registered['keydown'] = {}
    globs.keys_registered['keyup'] = {}
    del globs.animations[:]

    from . import api
    code, mod = load_module(RUN_PATH, api)
    exec(code, mod.__dict__)
    start_time = get_time()

def quit():
    pygame.quit()
    sys.exit()

def screenshot(directory = 'screenshots', filename = None):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    if not filename:
        filename = pygame.display.get_caption()[0] + ' - ' + str(datetime.datetime.today()) + '.jpg'
    pygame.image.save(SURF, os.path.join(directory, filename))

    size = 100 / globs.GRID_SIZE
    pos = (globs.WIDTH / globs.GRID_SIZE) / 2 - size / 2, (globs.HEIGHT / globs.GRID_SIZE) / 2 - (size / 1.36) / 2

    img = _create_image('__screenshot__', pos, size)
    globs.sprites.append(img)
    camera = globs.sprites[-1]
    animate(camera, 0.45, camera.destroy, size = size / 1.5)

def _draw_grid():
    for x in range(0, globs.WIDTH, globs.GRID_SIZE):
        pygame.draw.line(SURF, (0, 0, 0), (x, 0), (x, globs.HEIGHT))
    for y in range(0, globs.HEIGHT, globs.GRID_SIZE):
        pygame.draw.line(SURF, (0, 0, 0), (0, y), (globs.WIDTH, y))

def _update_animation(animation, delta):
    animation.update(delta)

def _update(delta):
    time = get_time()
    for sprite in globs.sprites:
        sprite._update(delta)

    animations = globs.animations

    for animation in animations:
        animation.update(delta + 1000 * (get_time() - time))

    for index, animation in enumerate(animations):
        if animation.finished:
            del globs.animations[index]
            animation.finish()

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

            if key == 'f12':
                screenshot()

        if event.type == KEYUP:
            key = pygame.key.name(event.key)
            if key in globs.keys_registered['keyup']:
                for callback in globs.keys_registered['keyup'][key]:
                    callback()

        if event.type == MOUSEBUTTONDOWN:
            for sprite in globs.sprites:
                if sprite.rect.collidepoint(event.pos):
                    sprite._handle_click(event.button)

    if update_game:
        _update(clock.get_time())
        _draw(SURF)

    pygame.display.update()
    clock.tick(FPS)
