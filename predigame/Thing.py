# something an Actor can use
class Thing:
	def __init__(self):
		self.damage = 100
		self.quantity = 1

	def use(self, actor, object=None):
		raise NotImplementedError('base class cannot be called directly')


