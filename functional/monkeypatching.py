from functional.functions import ComposedOperation, Function
from functional.operators import operations


def monkeypatch_ops(cls):
    for name, f in operations.items():
        op = make_op(name, f)
        setattr(cls, name, op)


def make_op(name, op):
    def created_op(self, other):
        if callable(other):
            f = Function(ComposedOperation(op, self, other))
        else:
            f = op.right(other) @ self

        return f

    created_op.__name__ = name

    return created_op