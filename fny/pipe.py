from fny import fn


class Pipe:
    """Class that holds an argument on which many different function calls are applied."""
    __slots__ = 'value'

    def __init__(self, value):
        self.value = value

    def into_head(self, f, *args, **kwargs):
        """Put argument in first position of function call and assign result to value."""
        self.value = self._call(f, self.value, *args, **kwargs)
        return self

    def into_last(self, f, *args, **kwargs):
        """Put argument in last position of function call and assign rsult to value."""
        self.value = self._call(f, *args, self.value, **kwargs)
        return self

    def do_head(self, f, *args, **kwargs):
        """Put argument in first position of function call but ignore return value."""
        self._call(f, self.value, *args, **kwargs)
        return self

    def do_last(self, f, *args, **kwargs):
        """Put argument in last position of function call but ignore return value."""
        self._call(f, *args, self.value, **kwargs)
        return self

    def _call(self, f, *args, **kwargs):
        if not callable(f):
            f = fn(f)

        return f(*args, **kwargs)


class OptionalPipe(Pipe):
    """Pipe but when the argument is None, all subsequent calls return None."""
    def _call(self, f, *args, **kwargs):
        if self.value is not None:
            return super(OptionalPipe, self)._call(f, *args, **kwargs)
