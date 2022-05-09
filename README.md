Python is a quite capable of writing code functionally and 
[many libraries](https://github.com/sfermigier/awesome-functional-python) 
have been written to reimplement many of the functional tools.
The only obstacle left is python's ugly lambda-syntax.
This library remedies this by letting one construct python functions out of thin air.

### Examples

Create functions either using the `fn`-factory or by manipulating the `it`-function:
```python
from fny import fn, lfn, it

inc2 = it + 2
inc3 = fn('+', 3)
inc2(3)  # => 5
inc3(3)  # => 6
```

In some cases the inverse can be constructed automatically:
```python
dec3 = inc3.inverse
dec3(8)  # => 5
```

Functions with multiple arguments can be constructed as well:
```python
add_subtract = fn(0) + fn(1) - fn(2)
add_subtract(5, 7, 3)  # => 9
```

Combine partially applied functions (`lfn`) with composition (`@` is used):

```python
dotproduct = sum @ lfn(map, fn('*'))
dotproduct([1, 2, 3], [3, 2, 1])  # => 10
```

A `Pipe`-class makes it easy to pass values around:

```python
from fny import Pipe

fac5 = (Pipe(5)
        .into_head('+', 1)           # ^^ + 1
        .into_last(range, 1)         # range(1, ^^)
        .into_last(reduce, fn('*'))  # reduce(fn('*'), ^^)
        .value)  # => 120
```

### How to

| Name | How |
|---|---|
| Identity function | `it` |
| Unary operations | `-it`, `~it` |
| Binary operations | `it + 1`, `fn('+', 1)` |
| Attribute access | `fn('.', "x")`, `it.attr.x` |
| Method call | `fn(".upper")`, `it.mtd.upper()` |
| Composing functions | `fn(abs) @ fn(sum)` |
| Partially apply on the right | `fn(pow, 2)`, `fn(pow).right(2)` |
| Partial apply on the left | `lfn(pow, 2)`, `fn(pow).left(2)` |
| Juxtaposition | `fn((math.cos, math.sin))` |
| Constant function | `fn(':=', 42)` |
| Return `n`th argument | `fn(n)` |
| Container lookup | `fn({'a': 1, 'b': 2, 'c': 3})` |
| Test membership | `fn(set('aeiouy'))` |
| Flip first and second argument | `fn(divmod).flip` |

### See also

This library aims just for function creation.
To manipulate sequences, it can be combined with [itertools](https://docs.python.org/3/library/itertools.html).
