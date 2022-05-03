import operator
from typing import Container

from fny.functions import Function, PartialLeft, JuxtaPosition
from fny.operators import operation_symbols, getitem_fn


def fn(f='', *args, **kwargs):
    """
    Construct a function from f.

    f can be:
    - callable - Will be used directly
    - '.method' written as string
    - operators '+'/'-','*' and most others as string
    - int or slice - Access nth element
    - tuple - All elements of the tuple will be applied to an argument
    - set - Is argument contained in the set
    - dict or list - Maps keys to values
    - default - Identity function

    If args or kwargs are passed a right-partial applied function will be created.
    """
    if callable(f):
        pass
    elif isinstance(f, str):
        if f.startswith('.') and len(f) > 1:
            f = PartialLeft(_methodcall, f[1:])
        else:
            f = operation_symbols[f]
    elif isinstance(f, (int, slice)):
        f = getitem_fn.right(f).unpack
    elif isinstance(f, tuple):
        f = JuxtaPosition([fn(f_i) for f_i in f])
    elif isinstance(f, set):
        f = PartialLeft(operator.contains, f)
    elif isinstance(f, Container):
        f = operator.itemgetter(*args, **kwargs)

    if not isinstance(f, Function):
        f = Function(f)

    if args or kwargs:
        f = f.right(*args, **kwargs)

    return f


def _methodcall(method, self, *args, **kwargs):
    return getattr(self, method)(*args, **kwargs)
