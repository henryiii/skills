# Dropping Python 3.9

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax

- **Pattern matching (`match`/`case`)**: Good for replacing complex `if/elif`
  chains and dispatch dictionaries.

## Built-ins

- **`zip(..., strict=True)`**: Replace manual length checks or
  `itertools.zip_longest` + validation when iterables must have equal length.
- **`int.bit_count()`**: Replace `bin(x).count("1")` or manual popcount
  implementations.
- **`aiter()` / `anext()`**: Replace manual async iteration boilerplate.

## `typing`

- **Explicit `TypeAlias`**: `Name: TypeAlias = "SomeType"` instead of plain
  assignments.
- **`ParamSpec`** / **`Concatenate`**: For decorator/higher-order function typing.
- **`TypeGuard`**: For user-defined type narrowing functions.

## `dataclasses`

- **`slots=True`**: Consider adding for memory efficiency.
- **`kw_only=True` / `KW_ONLY` marker**: For keyword-only fields.

## `contextlib`

- **`aclosing()`**: For async generators and async resources that need cleanup.

## `bisect`

- **`key` parameter**: Can simplify searches with custom ordering.

## Other stdlib

- **`base64.b32hexencode` / `b32hexdecode`**
- **`array.index(start, stop)`** parameter
- **`dict` view `.mapping`** attribute
- **`codecs.unregister()`**
