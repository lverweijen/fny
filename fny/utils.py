import operator
from typing import Container

from fny.functions import PartialLeft, JuxtaPosition
from fny.operators import operation_symbols, getitem_fn


def as_callable(f):
    """
    Guarantee f is callable

    :param f:
    - callable - Will be used directly
    - '.method' written as string
    - operators '+'/'-','*' and most others as string
    - int or slice - Access nth element
    - tuple - All elements of the tuple will be applied to an argument
    - set - Is argument contained in the set
    - dict or list - Maps keys to values
    :return: A callable
    """

    if callable(f):
        return f
    elif isinstance(f, str):
        if f.startswith('.') and len(f) > 1:
            return PartialLeft(_methodcall, f[1:])
        else:
            return operation_symbols[f]
    elif isinstance(f, tuple):
        return JuxtaPosition([as_callable(f_i) for f_i in f])
    elif isinstance(f, set):
        return PartialLeft(operator.contains, f)
    elif isinstance(f, Container):
        return getitem_fn.left(f)
    elif isinstance(f, int):
        return getitem_fn.right(f).unpack
    elif isinstance(f, slice):
        return getitem_fn.right(f)
    else:
        raise ValueError


def _methodcall(method, self, *args, **kwargs):
    return getattr(self, method)(*args, **kwargs)