import operator
from typing import Container

from functional.functions import Function, PartialLeft, JuxtaPosition
from functional.operators import operation_symbols, getitem


def fn(f='', *args, **kwargs):
    if callable(f):
        pass
    elif isinstance(f, str):
        if f.startswith('.') and len(f) > 1:
            f = PartialLeft(methodcall, f[1:])
        else:
            f = operation_symbols[f]
    elif isinstance(f, int):
        f = getitem.right(f).unpack
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


def methodcall(method, self, *args, **kwargs):
    return getattr(self, method)(*args, **kwargs)
