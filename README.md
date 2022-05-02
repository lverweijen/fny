Functional library for python

### Examples

```python
from functional import fn, it, Pipe, OptionalPipe
```

Different ways to create functions:
```python
inc2 = it + 2
inc3 = fn('+', 3)
inc5 = inc2 @ inc3
inc5(3)  # => 8
```

Or by taking the inverse:
```
dec5 = inc5.inverse
dec5(8)  # => 3
```

Multiple arguments:
```
add_fn2 = fn(0) + fn(1) + fn(2)
add_fn2(1, 2, 3)  # => 6
```

Combine left or right partials with composition (use `@` for this) to create more powerful functions.

```python
dotproduct = sum @ fn(map).left(fn('*'))
dotproduct([1, 2, 3], [3, 2, 1])  # => 10
```

Pipe values through different functions:

```python
fac5 = (Pipe(5)
        .into_head('+', 1)
        .into_last(range, 1)
        .into_head('f/', fn('*'), 1)  # fold is experimental
        .value)  # => 120
```

### Related

- [itertools](https://docs.python.org/3/library/itertools.html) - Combine with this library to manipulate sequences.
- [fn.py](https://github.com/kachayev/fn.py) - Package with similar ideas but taking a different approach.
- [functional-python](https://pypi.org/project/functional-python/) - Functional datatypes for python.
