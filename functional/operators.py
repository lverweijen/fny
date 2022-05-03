import functools
import operator as op
from itertools import filterfalse

from functional.functions import Function, InvertibleFunction, IdentityFunction

add = InvertibleFunction(op.add, op.sub)
radd = add.flip.with_inverse(add.inverse)
sub = InvertibleFunction(op.sub, op.__add__)
rsub = sub.flip.with_inverse(sub.flip)
mul = InvertibleFunction(op.mul, op.truediv)
rmul = mul.flip.with_inverse(mul.inverse)
div = InvertibleFunction(op.truediv, op.mul)
rdiv = div.flip.with_inverse(div.flip)
floordiv = Function(op.floordiv)
rfloordiv = Function(op.floordiv).flip
pow_ = Function(pow)
rpow = pow_.flip
mod = Function(op.mod)
rmod = mod.flip
neg = InvertibleFunction(op.neg, op.neg)

lt = Function(op.lt)
gt = Function(op.gt)
le = Function(op.le)
ge = Function(op.ge)
eq = Function(op.eq)
ne = Function(op.ne)

and_ = Function(op.__and__)
or_ = Function(op.__or__)
xor_ = InvertibleFunction(op.__xor__, op.__xor__)
invert = InvertibleFunction(op.invert, op.invert)
lshift = InvertibleFunction(op.lshift, op.rshift)
rshift = lshift.inverse
rlshift = lshift.flip.with_inverse(rshift.flip)
rrshift = rshift.flip.with_inverse(lshift.flip)

concat = Function(op.concat)
not_ = InvertibleFunction(op.not_, op.not_)
contains = Function(op.contains)
in_ = contains.flip
identity = IdentityFunction()

getattr_ = Function(getattr)
getitem = Function(op.getitem)


def _str_mul(text, n):
    """Join or repeat text depending on context."""
    if isinstance(n, str):
        return n.join(text)
    else:
        return text * n


def _map_inverse(iterable, f):
    return map(f.inverse, iterable)


str_mul = InvertibleFunction(_str_mul, str.split)
str_div = str_mul.inverse
map_fn = Function(map).rotate.with_inverse(_map_inverse)

mono_operations = {
    '__pos__': identity,
    '__neg__': neg,
    '__invert__': invert,
}

bin_operations = {
    '__add__': add,
    '__radd__': radd,
    '__sub__': sub,
    '__rsub__': rsub,
    '__mul__': mul,
    '__rmul__': mul,
    '__div__': div,
    '__rdiv__': rdiv,
    '__pow__': pow_,
    '__rpow__': rpow,
    '__mod__': mod,
    '__rmod__': rmod,
    '__lt__': lt,
    '__le__': le,
    '__gt__': gt,
    '__ge__': ge,
    '__eq__': eq,
    '__ne__': ne,
    '__and__': and_,
    '__or__': or_,
    '__xor__': xor_,
    '__lshift__': lshift,
    '__rlshift__': rlshift,
    '__rshift__': rshift,
    '__rrshift__': rrshift,
    '__getitem__': getitem
}

operation_symbols = {
    '': identity,
    '+': add,
    '-': sub,
    '_': neg,
    '*': mul,
    '/': div,
    '//': floordiv,
    '**': pow_,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge,
    '==': eq,
    '!=': ne,
    '&': and_,
    '|': or_,
    '^': xor_,
    '~': invert,
    '<<': lshift,
    '>>': rshift,
    '++': concat,
    'not': not_,
    'in': in_,
    '.': getattr_,
    '[]': getitem,
    # Experimental
    ':=': getitem.right(-1).unpack,
    's': Function(str.format).rotate,
    's+': concat,
    's*': str_mul,
    's/': str_div,
    's//': Function(str.count),
    's%': Function(str.replace).right('', -1),
    # Bird Meertens-formalism (experimental)
    'f/': Function(functools.reduce).flip,
    'f*': map_fn,
    'f<': Function(filter).flip,
    'f>': Function(filterfalse).flip,
}
