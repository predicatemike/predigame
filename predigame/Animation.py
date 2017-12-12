from . import globs

class Animation:
    def __init__(self, obj, duration, callback, **kwargs):
        self.obj = obj
        self.start = {}
        self.attributes = kwargs
        for attribute in self.attributes:
            self.start[attribute] = getattr(obj, attribute)
        self.time = float(0)
        self.duration = float(duration)

        # prevent div by 0
        if self.duration == 0.0:
            self.duration = 0.001

        self.callback = callback
        self.finished = False

    def update(self, delta):
        self.time += delta / 1000
        n = self.time / self.duration

        if n >= 1:
            self.finished = True
            n = 1

        for attribute in self.attributes:
            step = self.attributes[attribute] - self.start[attribute]
            setattr(self.obj, attribute, n * step + self.start[attribute])

    def finish(self):
        if not self.obj in globs.sprites:
            return

        if self.callback:
            self.callback()
