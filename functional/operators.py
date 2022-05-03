import functools
import operator as op
from itertools import filterfalse

from functional.functions import Function, InvertibleFunction, IdentityFunction

add_fn = InvertibleFunction(op.add, op.sub)
radd_fn = add_fn.flip.with_inverse(add_fn.inverse)
sub_fn = InvertibleFunction(op.sub, op.__add__)
rsub_fn = sub_fn.flip.with_inverse(sub_fn.flip)
mul_fn = InvertibleFunction(op.mul, op.truediv)
rmul_fn = mul_fn.flip.with_inverse(mul_fn.inverse)
div_fn = InvertibleFunction(op.truediv, op.mul)
rdiv_fn = div_fn.flip.with_inverse(div_fn.flip)
floordiv_fn = Function(op.floordiv)
rfloordiv_fn = Function(op.floordiv).flip
pow_fn = Function(pow)
rpow_fn = pow_fn.flip
mod_fn = Function(op.mod)
rmod_fn = mod_fn.flip
neg_fn = InvertibleFunction(op.neg, op.neg)

lt_fn = Function(op.lt)
gt_fn = Function(op.gt)
le_fn = Function(op.le)
ge_fn = Function(op.ge)
eq_fn = Function(op.eq)
ne_fn = Function(op.ne)

and_fn = Function(op.__and__)
or_fn = Function(op.__or__)
xor_fn = InvertibleFunction(op.__xor__, op.__xor__)
invert_fn = InvertibleFunction(op.invert, op.invert)
lshift_fn = InvertibleFunction(op.lshift, op.rshift)
rshift_fn = lshift_fn.inverse
rlshift_fn = lshift_fn.flip.with_inverse(rshift_fn.flip)
rrshift_fn = rshift_fn.flip.with_inverse(lshift_fn.flip)

concat_fn = Function(op.concat)
not_fn = InvertibleFunction(op.not_, op.not_)
contains_fn = Function(op.contains)
in_fn = contains_fn.flip
identity_fn = IdentityFunction()

getattr_fn = Function(getattr)
getitem_fn = Function(op.getitem)


def _str_mul(text, n):
    """Join or repeat text depending on context."""
    if isinstance(n, str):
        return n.join(text)
    else:
        return text * n


def _map_inverse(iterable, f):
    return map(f.inverse, iterable)


str_mul_fn = InvertibleFunction(_str_mul, str.split)
str_div_fn = str_mul_fn.inverse
map_fn = Function(map).rotate.with_inverse(_map_inverse)

mono_operations = {
    '__pos__': identity_fn,
    '__neg__': neg_fn,
    '__invert__': invert_fn,
}

bin_operations = {
    '__add__': add_fn,
    '__radd__': radd_fn,
    '__sub__': sub_fn,
    '__rsub__': rsub_fn,
    '__mul__': mul_fn,
    '__rmul__': mul_fn,
    '__div__': div_fn,
    '__rdiv__': rdiv_fn,
    '__pow__': pow_fn,
    '__rpow__': rpow_fn,
    '__mod__': mod_fn,
    '__rmod__': rmod_fn,
    '__lt__': lt_fn,
    '__le__': le_fn,
    '__gt__': gt_fn,
    '__ge__': ge_fn,
    '__eq__': eq_fn,
    '__ne__': ne_fn,
    '__and__': and_fn,
    '__or__': or_fn,
    '__xor__': xor_fn,
    '__lshift__': lshift_fn,
    '__rlshift__': rlshift_fn,
    '__rshift__': rshift_fn,
    '__rrshift__': rrshift_fn,
    '__getitem__': getitem_fn
}

operation_symbols = {
    '': identity_fn,
    '+': add_fn,
    '-': sub_fn,
    '_': neg_fn,
    '*': mul_fn,
    '/': div_fn,
    '//': floordiv_fn,
    '**': pow_fn,
    '<': lt_fn,
    '<=': le_fn,
    '>': gt_fn,
    '>=': ge_fn,
    '==': eq_fn,
    '!=': ne_fn,
    '&': and_fn,
    '|': or_fn,
    '^': xor_fn,
    '~': invert_fn,
    '<<': lshift_fn,
    '>>': rshift_fn,
    '++': concat_fn,
    'not': not_fn,
    'in': in_fn,
    '.': getattr_fn,
    '[]': getitem_fn,
    # Experimental
    ':=': getitem_fn.right(-1).unpack,
    's': Function(str.format).rotate,
    's+': concat_fn,
    's*': str_mul_fn,
    's/': str_div_fn,
    's//': Function(str.count),
    's%': Function(str.replace).right('', -1),
    # Bird Meertens-formalism (experimental)
    'f/': Function(functools.reduce).flip,
    'f*': map_fn,
    'f<': Function(filter).flip,
    'f>': Function(filterfalse).flip,
}
