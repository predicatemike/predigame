import sys, os
from . import predigame, api
from types import ModuleType

def err():
    print('Error: Invalid Python file provided')
    sys.exit()

def main():
    try:
        run_mod = sys.argv[1:][0]
    except:
        err()

    path = os.path.join(os.getcwd(), run_mod)

    src = open(path).read()
    code = compile(src, os.path.basename(path), 'exec', dont_inherit = True)

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__dict__.update(api.__dict__)
    sys.modules[name] = mod

    try:
        exec(code, mod.__dict__)
    except:
        pass
    finally:
        WIDTH = getattr(code, 'WIDTH', 16)
        HEIGHT = getattr(code, 'HEIGHT', 16)
        TITLE = getattr(code, 'TITLE', 'PrediGame')
        SIZE = getattr(code, 'SIZE', 50)

    predigame.init(WIDTH * SIZE, HEIGHT * SIZE, TITLE, grid = SIZE)

    exec(code, mod.__dict__)

    while True:
        predigame.main_loop()
