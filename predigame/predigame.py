import sys, os, random, datetime, mimetypes, pygame
from time import time as get_time
from pygame.locals import *
from . import globs
from .utils import load_module, register_keydown, rand_pos, rand_color, roundup, animate
from .Sprite import Sprite
from .Actor import Actor
from .Actor4D import Actor4D

show_grid = False
update_game = True
sounds = {}
images = {}
callbacks = []

def init(path, width = 800, height = 800, title = 'PrediGame', background = (220, 220, 220), fullscreen = False, **kwargs):
    global RUN_PATH, WIDTH, HEIGHT, BACKGROUND, FPS, GRID_SIZE, SURF, clock, start_time, sounds

    RUN_PATH = path
    WIDTH, HEIGHT = width, height
    FPS = kwargs.get('fps', 60)
    GRID_SIZE = kwargs.get('grid', 50)
    BACKGROUND = background

    globs.init(WIDTH, HEIGHT, GRID_SIZE, BACKGROUND)

    pygame.mixer.pre_init(22050, -16, 2, 1024) # sound delay fix
    pygame.init()
    pygame.display.set_caption(title)
    SURF = None
    if fullscreen:
        SURF = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        SURF = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    SURF.fill((0, 0, 0))
    loading_font = pygame.font.Font(None, 72)
    SURF.blit(loading_font.render('LOADING...', True, (235, 235, 235)), (25, 25))
    pygame.display.update()

    images['__error__'] = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images', 'error.png'))
    images['__screenshot__'] = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images', 'screenshot.png'))

    start_time = get_time()

def _create_image(name, pos, size, tag):
    img = images[name]
    rect = img.get_rect()
    new_width = 0
    new_height = 0
    if rect.width >= rect.height:
        new_width = size * float(globs.GRID_SIZE)
        new_height = rect.height * (new_width / rect.width)
    elif rect.width < rect.height:
        new_height = size * float(globs.GRID_SIZE)
        new_width = rect.width * (new_height / rect.height)
    rect.size = new_width, new_height
    rect.topleft = (pos[0] * float(globs.GRID_SIZE)) - rect.width/2.0, (pos[1] * float(globs.GRID_SIZE)) - rect.height/2.0

    return Sprite(img, rect, tag, name=name)

def _create_actor(actions, name, pos, size, directions, tag):
    img = actions['idle'][0]
    rect = img.get_rect()
    new_width = 0
    new_height = 0
    if rect.width >= rect.height:
        new_width = size * float(globs.GRID_SIZE)
        new_height = rect.height * (new_width / rect.width)
    elif rect.width < rect.height:
        new_height = size * float(globs.GRID_SIZE)
        new_width = rect.width * (new_height / rect.height)
    rect.size = new_width, new_height
    rect.topleft = (pos[0] * float(globs.GRID_SIZE)) - rect.width/2.0, (pos[1] * float(globs.GRID_SIZE)) - rect.height/2.0

    if directions == 4:
        return Actor4D(actions, rect, tag, name=name)
    else:
        return Actor(actions, rect, tag, name=name)

def _create_rectangle(color, pos, size, outline, tag):
    rect = pygame.Rect(pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE, size[0] * globs.GRID_SIZE, size[1] * globs.GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(globs.BACKGROUND_COLOR)
    surface.set_colorkey(globs.BACKGROUND_COLOR)
    pygame.draw.rect(surface, color, (0, 0, rect.width, rect.height), outline)

    return Sprite(surface, rect, tag)

def _create_circle(color, pos, size, outline, tag):
    rect = pygame.Rect(pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE, size * globs.GRID_SIZE, size * globs.GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(globs.BACKGROUND_COLOR)
    surface.set_colorkey(globs.BACKGROUND_COLOR)
    pygame.draw.circle(surface, color, (rect.width // 2, rect.height // 2), rect.width // 2, outline)

    return Sprite(surface, rect, tag)

def _create_ellipse(color, pos, size, outline, tag):
    rect = pygame.Rect(pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE, size[0] * globs.GRID_SIZE, size[1] * globs.GRID_SIZE)
    surface = pygame.Surface(rect.size)
    surface.fill(globs.BACKGROUND_COLOR)
    surface.set_colorkey(globs.BACKGROUND_COLOR)
    pygame.draw.ellipse(surface, color, (0, 0, rect.width, rect.height), outline)

    return Sprite(surface, rect, tag)

def image(name = None, pos = None, size = 1, tag = ''):
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
        if os.path.isdir('images/'):
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
        else:
            name = '__error__'

    if not pos:
        pos = rand_pos(size - 1, size - 1)

    img = _create_image(name, pos, size, tag)
    globs.sprites.append(img)
    return globs.sprites[-1]

def actor(name = None, pos = None, size = 1, directions = 2, tag = ''):
    if not name:
        sys.exit('Actor name is missing!')

    loaded = False
    states = {}
    path = 'actors/' + name
    if os.path.isdir(path):
        for state in os.listdir(path):
            if os.path.isdir(path + '/' + state):
                for img_file in os.listdir(path + '/' + state):
                    if not state in states:
                        states[state] = []
                    try:
                        print(path + '/' + state + '/' + img_file)
                        states[state].append(pygame.image.load(path + '/' + state + '/' + img_file))
                        loaded = True
                    except:
                        continue

    if not loaded:
        sys.exit('Unable to find or load actor ' + str(name) + '. Does actors/' + str(name) + ' exist?')    


    if not pos:
        pos = rand_pos(size - 1, size - 1)

    img = _create_actor(states, name, pos, size, directions, tag)
    globs.sprites.append(img)
    return globs.sprites[-1]    

def at(pos):
    if pos in globs.cells:
        return globs.cells[pos]

def get(name):
    if name in globs.tags:
        return globs.tags[name]
    else:
        return []

def shape(shape = None, color = None, pos = None, size = (1, 1), tag = '', **kwargs):
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
        shape = _create_circle(color, pos, size[0], outline, tag)
    elif shape == 'rect':
        shape = _create_rectangle(color, pos, size, outline, tag)
    elif shape == 'ellipse':
        shape = _create_ellipse(color, pos, size, outline, tag)
    else:
        print('Shape, ' + shape + ', is not a valid shape name')
        return False

    globs.sprites.append(shape)
    return globs.sprites[-1]

def text(string, color = None, pos = None, size = 1, tag = ''):
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
    text = Sprite(surface, pygame.Rect(pos[0], pos[1], font_width, font_height), tag)

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

def callback(function, wait):
    callbacks.append({'cb': function, 'time': get_time() + wait})

def score(value = 0, **kwargs):
    global score_dict
    try:
        score_dict
        globs.sprites.remove(score_dict['sprite'])
    except:
        score_dict = {
            'value': 0,
            'sprite': None,
            'size': 28,
            'color': (25, 25, 25),
            'pos': (25, 25)
        }

    score_dict['color'] = kwargs.get('color', score_dict['color'])
    size = kwargs.get('size', None)
    pos = kwargs.get('pos', None)

    if size:
        score_dict['size'] = int(size * globs.GRID_SIZE)
    if pos:
        score_dict['pos'] = pos[0] * globs.GRID_SIZE, pos[1] * globs.GRID_SIZE

    score_dict['value'] += value

    string = str(score_dict['value'])
    font = pygame.font.Font(None, score_dict['size'])
    font_width, font_height = font.size(string)
    surface = font.render(string, True, score_dict['color'])
    score_dict['sprite'] = Sprite(surface, pygame.Rect(score_dict['pos'][0], score_dict['pos'][1], font_width, font_height))

    globs.sprites.append(score_dict['sprite'])

    return score_dict['value']

def destroyall():
    del globs.sprites[:]

def pause():
    pygame.event.post(pygame.event.Event(USEREVENT, action = 'pause'))

def resume():
    global update_game
    update_game = True

def reset(*kwargs):
    destroyall()
    globs.keys_registered['keydown'] = {}
    globs.keys_registered['keyup'] = {}
    globs.tags = {}
    del globs.animations[:]
    del callbacks[:]

    from . import api
    code, mod = load_module(RUN_PATH, api)
    exec(code, mod.__dict__)

    global start_time
    start_time = get_time()
    resume()

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

    for callback in callbacks:
        if callback['time'] <= get_time():
            callback['cb']()
            callbacks.remove(callback)

def _draw(SURF):
    if isinstance(globs.BACKGROUND, pygame.Surface) :
        SURF.blit(globs.BACKGROUND, (0,0))
    else:
        SURF.fill(globs.BACKGROUND)
    
    globs.cells = {}
    for sprite in globs.sprites:
        globs.cells[sprite.pos] = sprite
        sprite._draw(SURF)

    if show_grid:
        _draw_grid()

def main_loop():
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:            

            # ignore all the other key presses
            # complete any in process animations
            # TODO: there should be restrictions on
            #       on how this can be used
            for key in globs.keys_pressed:
                globs.keys_pressed.remove(key)

            for animation in globs.animations:
                animation.abort()

            key = pygame.key.name(event.key)
            if key in globs.keys_registered['keydown']:
                for callback in globs.keys_registered['keydown'][key]:
                    callback()

            if not key in globs.keys_pressed:
                globs.keys_pressed.append(key)

            if key == 'escape':
                pygame.event.post(pygame.event.Event(QUIT))

            if key == 'f12':
                screenshot()

        if event.type == KEYUP:
            key = pygame.key.name(event.key)
            if key in globs.keys_registered['keyup']:
                for callback in globs.keys_registered['keyup'][key]:
                    callback()

            if key in globs.keys_pressed:
                globs.keys_pressed.remove(key)

        if event.type == MOUSEBUTTONDOWN:
            for sprite in globs.sprites:
                if sprite.rect.collidepoint(event.pos):
                    sprite._handle_click(event.button, event.pos)

        if event.type == USEREVENT:
            global update_game
            if event.action == 'pause' and update_game:
                update_game = False
                _update(clock.get_time())
                _draw(SURF)

    if update_game:
        _update(clock.get_time())
        _draw(SURF)

    pygame.display.update()
    clock.tick(FPS)
