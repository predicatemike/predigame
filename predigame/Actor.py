import sys, random, math, pygame
from time import time
from .Sprite import Sprite
from .constants import *
from . import globs

class Actor(Sprite):
	def __init__(self, actions, rect, tag=None, abortable = False, name=None):

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
		self.flip_x = False
		self.flip_y = False
		surface = actions[self.action][self.index]
		Sprite.__init__(self, surface, rect, tag, abortable, name)

	def flip(self, flip_x = True, flip_y = False):

		actions = []
		for img in self.actions[WALK]:
			actions.append(pygame.transform.flip(img, flip_x, flip_y))
		self.actions[WALK] = actions

		actions = []
		for img in self.actions[IDLE]:
			actions.append(pygame.transform.flip(img, flip_x, flip_y))
		self.actions[IDLE] = actions
		return self

	def move(self, vector, **kwargs):
		if vector[0] < 0 and not self.flip_x:
			self.flip_x = True
			self.flip(flip_x=True)
		elif vector[0] > 0 and self.flip_x:
			self.flip_x = False
			self.flip(flip_x=True)

		self.act(WALK, FOREVER)					
		Sprite.move(self, vector, **kwargs)

	def _complete_move(self, callback = None):
		self.act(IDLE, FOREVER)
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
			self.action = IDLE
			self.action_loop = FOREVER		


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

