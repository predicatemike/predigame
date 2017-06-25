import sys, os
from . import predigame
from types import ModuleType

def err():
    print('Error: Invalid Python file provided')
    sys.exit()

def load_module(path, api):
    src = open(path).read()
    code = compile(src, os.path.basename(path), 'exec', dont_inherit = True)

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__dict__.update(api.__dict__)
    sys.modules[name] = mod

    return code, mod

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
