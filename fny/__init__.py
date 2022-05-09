from fny.factories import fn, lfn
from fny.functions import Function
from fny.monkeypatching import monkeypatch_ops
from fny.pipe import Pipe, OptionalPipe

__all__ = ['fn', 'lfn', 'it', 'Pipe', 'OptionalPipe']

it = fn()
monkeypatch_ops(Function)

__version__ = "0.1.0"
