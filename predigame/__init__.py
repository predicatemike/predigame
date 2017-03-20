import sys, os
# import importlib.util
from .predigame import *

def err():
    print('Error: Invalid Python file provided')
    sys.exit()

def dep_injection(mod):
    # functions
    mod.grid = grid
    mod.img = img
    mod.shape = shape

    # shapes
    mod.RECT = RECT
    mod.CIRCLE = CIRCLE
    mod.ELLIPSE = ELLIPSE

    # colors
    mod.BLACK = BLACK
    mod.SILVER = SILVER
    mod.GRAY = GRAY
    mod.WHITE = WHITE
    mod.RED = RED
    mod.MAROON = MAROON
    mod.YELLOW = YELLOW
    mod.OLIVE = OLIVE
    mod.LIME = LIME
    mod.GREEN = GREEN
    mod.AQUA = AQUA
    mod.TEAL = TEAL
    mod.BLUE = BLUE
    mod.NAVY = NAVY
    mod.CYAN = CYAN
    mod.PINK = PINK
    mod.PURPLE = PURPLE

def main():
    if not len(sys.argv) > 1:
        err()

    run_mod = sys.argv[1:][0]
    run_path = os.getcwd() + '/' + run_mod
    run_mod = run_mod[:-3]

    if not os.path.isfile(run_path):
        err()

    init()

    sys.path.append(os.getcwd())
    script = __import__(run_mod)

    # spec = importlib.util.spec_from_file_location(run_mod, run_path)
    # script = importlib.util.module_from_spec(spec)
    # dep_injection(script)
    # spec.loader.exec_module(script)

    while True:
        main_loop()
