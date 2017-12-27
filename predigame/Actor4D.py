import sys, random, math, pygame
from time import time
from .Sprite import Sprite
from .constants import *
from . import globs


# actor class for four directional movement
class Actor4D(Sprite):
	def __init__(self, actions, rect, tag=None, name=None):

		# - scale images
		self.actions = {}
		for action in actions:
			self.actions[action] = []
			for img in actions[action]:
				img = img.convert_alpha()
				img = pygame.transform.scale(img, rect.size)
				self.actions[action].append(img)

		self.index = 0
		self.action_iterations = 0
		self.action = IDLE
		self.action_loop = FOREVER
		self.prev_vector = None
		self.direction = LEFT

		surface = actions[self.action][self.index]
		Sprite.__init__(self, surface, rect, tag, name)

	def move(self, vector, **kwargs):

		direction = LEFT
		if vector[0] == 1:
			direction = RIGHT
		elif vector[0] == -1:
			direction = LEFT
		elif vector[1] == 1:
			direction = FRONT
		elif vector[1] == -1:
			direction = BACK

		if direction != self.direction:
			self.index = 0

		self.direction = direction

		self.act(WALK + '_' + direction, FOREVER)					
		Sprite.move(self, vector, **kwargs)

	def _complete_move(self, callback = None):
		self.act(IDLE + '_' + self.direction, FOREVER)
		Sprite._complete_move(self, callback)

	def _update(self, delta):
		img = self.actions[self.action][self.index]
		self.surface = img
		self.origin_surface = img
		Sprite._update(self, delta)
		if self.action_loop == FOREVER or self.action_iterations < self.action_loop:
			self.index = self.index + 1
			if self.index >= len(self.actions[self.action]):
				self.index = 0
				self.action_iterations = self.action_iterations + 1
		else:
			self.index = 0
			self.action = IDLE + '_' + self.direction
			self.action_loop = FOREVER		

	def _draw(self, surface):
		Sprite._draw(self, surface)

	def act(self, action, loop=FOREVER):
		if not action in self.actions:
			print('Unsupported action ' + str(action) + '. Valid options are:')
			for action in self.actions:
				print(action.upper())
			sys.exit(0)
		self.index = 0
		self.action = action
		self.action_loop = loop
		self.action_iterations = 0

