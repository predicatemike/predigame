class Animation:
    def __init__(self, obj, duration, callback, **kwargs):
        self.obj = obj
        self.start = {}
        self.attributes = kwargs
        for attribute in self.attributes:
            self.start[attribute] = getattr(obj, attribute)
        self.time = float(0)
        self.duration = float(duration)
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
        if self.callback:
            self.callback()
