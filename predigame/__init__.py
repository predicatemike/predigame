import sys, os
from . import predigame
from .utils import load_module

def err():
    print('Error: Invalid Python file provided')
    sys.exit()

def main():
    try:
        run_mod = sys.argv[1:][0]
    except:
        err()

    path = os.path.join(os.getcwd(), run_mod)

    from . import api
    code, mod = load_module(path, api)

    try:
        exec(code, mod.__dict__)
    except:
        pass
    finally:
        WIDTH = getattr(mod, 'WIDTH', 16)
        HEIGHT = getattr(mod, 'HEIGHT', 16)
        TITLE = getattr(mod, 'TITLE', 'PrediGame')
        SIZE = getattr(mod, 'SIZE', 50)

    predigame.init(path, WIDTH * SIZE, HEIGHT * SIZE, TITLE, grid = SIZE)

    exec(code, mod.__dict__)

    while True:
        predigame.main_loop()
