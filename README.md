# PrediGame
## API
### Classes

#### Sprite
```python
Sprite(self, surface, rect) -> Sprite
```
Takes a pygame surface and rectangle and returns a Sprite instance.

##### float
```python
Sprite.float(self, distance = 0.25) -> Sprite
```
Will allow the Sprite instance to float around within an area of distance * GRID_SIZE (i.e. with a grid size of 100, floating a distance of 0.25 would occur within 25 pixels or 25% of the grid size).

##### speed
```python
Sprite.speed(self, speed) -> Sprite
```
Take an integer speed value and sets the Sprite instance's speed.

##### move_keys
```python
Sprite.move_keys(self, right = 'right', left = 'left', up = 'up', down = 'down')
```
Inputs a series of key names which will be used for moving right, left, up, and down respectively.

---

### Functions

#### grid
```python
grid() -> None
```
Draws the coordinate grid atop all sprites

#### img
```python
img(name = None, pos = None, size = 1) -> Sprite
```
Takes an image name from the "images" directory and draws it at the given position with the given size. If no name is provided, a random image from the "images" directory will be chosen. If no position is provided, a random location will be chosen.

#### shape
```python
shape(shape = None, color = None, pos = None, size = (1, 1)) -> Sprite
```
Takes a shape constant and draws it at the given position with the given size and color. If no shape is provided, a random shape  will be chosen. If no color is provided, a random color will be chosen. If no position is provided, a random location will be chosen.

---

### Shapes

```python
RECT
CIRCLE
```

---

### Colors
```python
BLACK
WHITE
PINK
RED
GREEN
BLUE
YELLOW
CYAN
PINK
PURPLE
```

## Running
Python version 2 or 3 must be installed with the corresponding version of Pygame.

Download and clone this repository. Then make the "pg" script executable with:
```bash
chmod +x pg
```
Run the example file with
```bash
./pg example.py
```
