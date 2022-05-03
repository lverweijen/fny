from fny.functions import ComposedOperation, Function
from fny.operators import bin_operations, mono_operations


def monkeypatch_ops(cls):
    for name, f in mono_operations.items():
        op = _make_monop(name, f)
        setattr(cls, name, op)

    for name, f in bin_operations.items():
        op = _make_binop(name, f)
        setattr(cls, name, op)


def _make_monop(name, op):
    def created_op(self):
        return op @ self

    created_op.__name__ = name
    return created_op


def _make_binop(name, op):
    def created_op(self, other):
        if callable(other):
            f = Function(ComposedOperation(op, self, other))
        else:
            f = op.right(other) @ self

        return f

    created_op.__name__ = name
    return created_op