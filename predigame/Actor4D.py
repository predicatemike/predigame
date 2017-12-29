import sys, random, math, pygame
from time import time
from .Sprite import Sprite
from .Actor import Actor
from .constants import *
from . import globs


# actor class for four directional movement
class Actor4D(Actor):
	def __init__(self, actions, rect, tag=None, abortable=False, name=None):
		self.frame_count = 0
		self.frame_rate = 1
		self.prev_vector = None
		self.direction = LEFT
		Actor.__init__(self, actions, rect, tag, abortable, name)

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
			self.frame_count = self.frame_count + 1
			if self.frame_count >= self.frame_rate:
				self.index = self.index + 1
				self.frame_count = 0
			if self.index >= len(self.actions[self.action]):
				self.index = 0
				self.action_iterations = self.action_iterations + 1
		else:
			self.index = 0
			self.action = IDLE + '_' + self.direction
			self.action_loop = FOREVER		

	def act(self, action, loop=FOREVER):
		if action in self.actions:
			Actor.act(self, action, loop)
		else:
			# infer the action based on direction
			if str(action + '_' + self.direction) in self.actions:
				Actor.act(self, str(action + '_' + self.direction), loop)
			else:
				Actor.act(self, action, loop)

	def rate(self, frame_rate):
		""" the rate to swap animation frames, default is 1 per update call """
		if frame_rate < 0:
			frame_rate = 1
		if frame_rate > 60:
			frame_rate = 60
		self.frame_rate = frame_rate
		return self

	def facing(self):
		""" returns a position (off the screen) where this actor is facing """
		if self.direction == BACK:
			return self.x, -1
		elif self.direction == FRONT:
			return self.x, int(globs.HEIGHT/globs.GRID_SIZE)+1
		elif self.direction == LEFT:
			return -1, self.y
		elif self.direction == RIGHT:
			return int(globs.WIDTH/globs.GRID_SIZE)+1, self.y

	def next(self):
		""" the next position (in the current direction) """
		if self.direction == BACK:
			return self.x, self.y - 1
		elif self.direction == FRONT:
			return self.x, self.y + 1
		elif self.direction == LEFT:
			return self.x - 1, self.y
		elif self.direction == RIGHT:
			return self.x + 1, self.y

