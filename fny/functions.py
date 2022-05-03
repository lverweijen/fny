from fny.formatting import repr_call


class Function:
    __slots__ = '_f'

    def __init__(self, f):
        if isinstance(f, Function):
            self._f = f._f
        else:
            self._f = f

    def __call__(self, *args, **kwargs):
        return self._f(*args, **kwargs)

    def __repr__(self):
        return repr_call(self.__class__, self._f)

    def __matmul__(self, other):
        """Functional composition"""
        return Function(Compose(self._f, other))

    def __rmatmul__(self, other):
        """Functional composition"""
        return Function(Compose(other, self._f))

    def left(self, *args, **kwargs):
        """Partially apply function to the left."""
        if not args and not kwargs:
            return self

        return Function(PartialLeft(self._f, *args, **kwargs))

    def right(self, *args, **kwargs):
        """Partially apply function to the right."""
        if not args and not kwargs:
            return self

        return Function(PartialRight(self._f, *args, **kwargs))

    def with_inverse(self, inv):
        """
        Create function with an inverse.

        It should hold that:
        - g = f @ f.inverse
        - g(x) == x
        """
        return InvertibleFunction(self._f, inv)

    @property
    def flip(self):
        """Swap first and second argument."""
        return Function(self._flip)

    @property
    def rotate(self):
        """Rotate first argument as last."""
        return Function(self._rotate)

    @property
    def pack(self):
        """Make function that operates on multiple arguments work on a list."""
        return Function(self._pack)

    @property
    def unpack(self):
        """Make function that operates on a list work on multiple arguments."""
        return Function(self._unpack)

    def _flip(self, *args, **kwargs):
        return self._f(args[1], args[0], *args[2:], **kwargs)

    def _rotate(self, *args, **kwargs):
        return self._f(args[-1], *args[:-1], **kwargs)

    def _pack(self, arg):
        return self._f(*arg)

    def _unpack(self, *args):
        return self._f(args)


class InvertibleFunction(Function):
    __slots__ = '_inverse'

    def __init__(self, f, inverse):
        super(InvertibleFunction, self).__init__(f)
        self._inverse = inverse

    def __matmul__(self, other):
        if isinstance(other, InvertibleFunction):
            return InvertibleFunction(Compose(self._f, other), 
                                      Compose(other.inverse, self.inverse))
        else:
            return super(InvertibleFunction, self).__matmul__(other)

    def __rmatmul__(self, other):
        if isinstance(other, InvertibleFunction):
            return InvertibleFunction(Compose(other, self._f, other),
                                      Compose(self.inverse, other.inverse))
        else:
            return super(InvertibleFunction, self).__matmul__(other)

    def right(self, *args, **kwargs):
        return InvertibleFunction(PartialRight(self._f, *args, **kwargs),
                                  PartialRight(self.inverse._f, *args, **kwargs))

    @property
    def inverse(self):
        """
        Return the inverse function.

        It should hold that:
        - g = f @ f.inverse
        - g(x) == x
        """
        inv = self._inverse
        if not isinstance(inv, InvertibleFunction):
            inv = InvertibleFunction(inv, self)
            self._inverse = inv
        return inv


class IdentityFunction(InvertibleFunction):
    @staticmethod
    def identity(x):
        return x

    def __init__(self):
        super(IdentityFunction, self).__init__(self.identity, self.identity)

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __matmul__(self, other):
        return other

    __rmatmul__ = __matmul__


class Compose:
    __slots__ = '_funcs'

    def __init__(self, *funcs):
        self._funcs = []
        for f in funcs:
            if isinstance(f, Compose):
                self._funcs.extend(f._funcs)
            else:
                self._funcs.append(f)

    def __repr__(self):
        return repr_call(self.__class__, *self._funcs)

    def __call__(self, *args, **kwargs):
        funcs = reversed(self._funcs)
        f = next(funcs)
        value = f(*args, **kwargs)

        for f in funcs:
            value = f(value)

        return value


class ComposedOperation:
    __slots__ = '_op', '_f', '_g'

    def __init__(self, op, left, right):
        self._op = op
        self._f = left
        self._g = right

    def __repr__(self):
        return repr_call(self.__class__, self._op, self._f, self._g)

    def __call__(self, *args, **kwargs):
        f_res = self._f(*args, **kwargs)
        g_res = self._g(*args, **kwargs)
        return self._op(f_res, g_res)


class PartialLeft:
    __slots__ = "_f", "_args", "_kwargs"

    def __init__(self, f, *args, **kwargs):
        if isinstance(f, PartialLeft):
            self._f = f._f
            self._args = (*args, *f._args)
            self._kwargs = {**kwargs, **f._kwargs}
        else:
            self._f, self._args, self._kwargs = f, args, kwargs

    def __call__(self, *args, **kwargs):
        return self._f(*self._args, *args, **self._kwargs, **kwargs)

    def __repr__(self):
        return repr_call(self.__class__)(self._f, *self._args, **self._kwargs)


class PartialRight:
    __slots__ = "_f", "_args", "_kwargs"

    def __init__(self, f, *args, **kwargs):
        if isinstance(f, PartialRight):
            self._f = f._f
            self._args = (*f._args, *args)
            self._kwargs = {**f._kwargs, **kwargs}
        else:
            self._f, self._args, self._kwargs = f, args, kwargs

    def __call__(self, *args, **kwargs):
        return self._f(*args, *self._args, **kwargs, **self._kwargs)

    def __repr__(self):
        return repr_call(self.__class__, self._f, *self._args, **self._kwargs)


class JuxtaPosition:
    __slots__ = '_funcs'

    def __init__(self, funcs):
        self._funcs = []
        for f in funcs:
            if callable(f):
                self._funcs.append(f)
            else:
                raise TypeError

    def __repr__(self):
        return repr_call(self.__class__, *self._funcs)

    def __call__(self, *args, **kwargs):
        return tuple(f(*args, **kwargs) for f in self._funcs)
