from functional.fn import fn
from functional.functions import Function
from functional.monkeypatching import monkeypatch_ops
from functional.operators import identity as it
from functional.pipe import Pipe, OptionalPipe

__all__ = ['fn', 'it', 'Pipe', 'OptionalPipe']

monkeypatch_ops(Function)