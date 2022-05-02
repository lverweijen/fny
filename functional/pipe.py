from functional import fn


class Pipe:
    __slots__ = 'value'

    def __init__(self, value):
        self.value = value

    def into_head(self, f, *args, **kwargs):
        self.value = self._call(f, self.value, *args, **kwargs)
        return self

    def into_last(self, f, *args, **kwargs):
        self.value = self._call(f, *args, self.value, **kwargs)
        return self

    def do_head(self, f, *args, **kwargs):
        self._call(f, self.value, *args, **kwargs)
        return self

    def do_last(self, f, *args, **kwargs):
        self._call(f, *args, self.value, **kwargs)
        return self

    def _call(self, f, *args, **kwargs):
        if not callable(f):
            f = fn(f)

        return f(*args, **kwargs)


class OptionalPipe(Pipe):
    def _call(self, f, *args, **kwargs):
        if self.value is not None:
            return super(OptionalPipe, self)._call(f, *args, **kwargs)
