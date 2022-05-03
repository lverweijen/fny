def repr_function(f):
    try:
        name = f.__name__
    except AttributeError:
        name = repr(f)

    if hasattr(f, '__self__'):
        name = repr_function(f.__self__) + '.' + name

    return name


def repr_call(f, *args, **kwargs):
    fname = repr_function(f)
    fargs = ', '.join([repr_function(x) if callable(x) else repr(x) for x in args])
    fkwargs = ', '.join(f"{k}={v}" for k, v in kwargs.items())
    fall = ', '.join([arglist for arglist in (fargs, fkwargs) if arglist])
    return f"{fname}({fall})"
