# Predigame Levels
from copy import deepcopy

class Level:
	def __init__(self):
		self.level = 100

	def setup(self):
		raise NotImplementedError('Level.setup() cannot be called directly')

	def teardown(self):
		raise NotImplementedError('Level.teardown() cannot be called directly')

	def completed(self):
		raise NotImplementedError('Level.completed() cannot be called directly')

	def next(self):
		raise NotImplementedError('Level.next() cannot be called directly')
