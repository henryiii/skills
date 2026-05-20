# Dropping Python 3.11

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax / Type system

- **Type parameter syntax (PEP 695)**: Compact generics:
  `def max[T](args: Iterable[T]) -> T`, `class list[T]: ...`
- **`type` statement for aliases**: `type Point = tuple[float, float]`.
  Supports generics: `type Point[T] = tuple[T, T]`. Replaces `TypeAlias`.
- **F-string formalization (PEP 701)**: Reuse same quotes, multiline
  expressions, comments, and backslashes inside f-string expression parts.

## `typing`

- **`override()`**: Decorator marking methods that override a base class method.
  Helps catch signature mismatches in static analysis.
- **`Unpack[TypedDict]` for `**kwargs`**: Precise per-argument typing for
  keyword arguments.

## `collections.abc`

- **`Buffer`**: ABC for buffer objects. Use in annotations instead of
  `typing_extensions.Buffer`.

## `itertools`

- **`batched()`**: Collect iterators into fixed-size tuples (last may be shorter).

## `math`

- **`sumprod()`**: Sum of products with better accuracy than a manual loop.

## `os.path`

- **`splitroot()`**: Split path into `(drive, root, tail)`.

## `pathlib`

- **Subclassing `Path` / `PurePath`**: Now officially supported via
  `with_segments()` override.

## `shutil`

- **`rmtree(onexc=...)`**: Replaces deprecated `onerror` callback; receives the
  exception instance directly instead of `(typ, val, tb)`.

## `types`

- **`MappingProxyType` hashability**: Now hashable if the underlying mapping is.

## Other stdlib

- **`slice` hashability**: Can now be used as dict keys and set items.
- **`memoryview` half-float**: Supports the `"e"` format code.
- **`fractions.Fraction` formatting**: Supports float-style format specifiers.
- **`random.binomialvariate()`**: New distribution method.
- **`calendar.Month` / `calendar.Day`**: Enums for months and days of week.
