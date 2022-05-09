from fny.utils import as_callable
from fny.functions import Function


def fn(f='', *args, **kwargs):
    """
    Construct a function from f optionally partially applying arguments to the right.

    If args or kwargs are passed a right-partial applied function will be created.
    """
    f = as_callable(f)

    if not isinstance(f, Function):
        f = Function(f)

    if args or kwargs:
        f = f.right(*args, **kwargs)

    return f


def lfn(f, *args, **kwargs):
    """Same as fn, but arguments will be partially applied to the left.

    Similar to functools.partial
    """
    f = as_callable(f)

    if not isinstance(f, Function):
        f = Function(f)

    if args or kwargs:
        f = f.left(*args, **kwargs)

    return f
