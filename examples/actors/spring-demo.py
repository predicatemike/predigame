WIDTH = 20
HEIGHT = 10
TITLE = 'Piggys Revenge'

# use a grass background
BACKGROUND = 'ville'

piggy = actor('Piggy', (-5, 7), size=3).speed(7)
piggy.act(RUN_RIGHT, FOREVER)


def zombies():
    z3 = actor('Zombie-3', (-9, 7), size=3)
    z1 = actor('Zombie-1', (-6, 7), size=3)
    z2 = actor('Zombie-2', (-3, 7), size=3)
    z1.act(WALK_RIGHT, FOREVER)
    z2.act(WALK_RIGHT, FOREVER)
    z3.act(WALK_RIGHT, FOREVER)
    z1.move_to((WIDTH+5,7))
    z2.move_to((WIDTH+5,7))
    z3.move_to((WIDTH+5,7))

def start():
    zombies()
    callback(piggy_run, 2)

def piggy_walkback():
    piggy.act(RUN_LEFT, FOREVER)
    piggy.move_to((8,7),callback=piggy_pose)

def piggy_pose():
    piggy.act('happy_front', FOREVER)
    text('Piggy\'s Revenge', color=WHITE)

def piggy_run():
    piggy.move_to((WIDTH+5,7),callback=piggy_walkback)

# register the 'r' key for resetting the game
keydown('r', reset)
keydown('space',start)
