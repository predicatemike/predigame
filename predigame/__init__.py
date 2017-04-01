import sys, os
from . import predigame, api
from types import ModuleType

WIDTH = 16
HEIGHT = 16
TITLE = 'PrediGame'
SIZE = 50

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

    consts = ['WIDTH', 'HEIGHT', 'TITLE', 'SIZE']

    for const in code.co_names:
        if const in consts:
            globals()[const] = code.co_consts[code.co_names.index(const)]

    predigame.init(WIDTH * SIZE, HEIGHT * SIZE, TITLE, grid = SIZE)

    exec(code, mod.__dict__)

    while True:
        predigame.main_loop()
