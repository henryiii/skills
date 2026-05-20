# Dropping Python 3.14

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax

- **Lazy imports** (PEP 810): `lazy import module` or `lazy from pkg import name`
- **`frozendict`** (PEP 814): Immutable, hashable dict built-in
- **`sentinel`** (PEP 661): Built-in for creating unique sentinel values
- **Unpacking in comprehensions** (PEP 798): `[*L for L in lists]`, `{"a": 1, **d for d in dicts}`

## Built-ins

- **`bytearray.take_bytes()`**: Extract bytes from a `bytearray` without copying
- **`slice` is generic**: Supports subscripting in type hints

## Encoding

- **UTF-8 default** (PEP 686): `open(...)` defaults to UTF-8 regardless of locale
  (opt-in encoding warnings help find code that relied on locale)

## Typing

- **`TypeForm`** (PEP 747): Annotate type forms (e.g. `type[int]`)
- **TypedDict with extra items** (PEP 728): `class MyDict(TypedDict, extra=...)`

## New modules

- **`profiling`** (PEP 799): New package replacing `cProfile`/`profile`
  - `profiling.tracing` (replaces `cProfile`)
  - `profiling.sampling` (Tachyon profiler)
- **`math.integer`**: Integer mathematical functions

## Other stdlib

- **`.start` files** (PEP 829): Package startup configuration (replaces `.pth` import lines)
- **`__slots__` on `tuple` subclasses**: Including `namedtuple` subclasses
- **`__dict__` / `__weakref__` as valid `__slots__` entries**
