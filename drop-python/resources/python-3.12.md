# Dropping Python 3.12

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Type system

- **Type parameter defaults (PEP 696)**: `class C[T = int]: ...`, also
  `TypeVar("T", default=int)`. Replaces `typing_extensions` defaults.
- **`TypeIs` (PEP 742)**: Better type narrowing than `TypeGuard` (narrows in
  both branches).
- **`ReadOnly` (PEP 705)**: Mark `TypedDict` items read-only.
- **`warnings.deprecated()` (PEP 702)**: Decorator marking deprecations for
  both type checkers and runtime. Replaces `typing_extensions.deprecated`.
- **`get_protocol_members()` / `is_protocol()`**: Protocol introspection.

## `copy`

- **`replace()`**: Modified copies of immutables; works with dataclasses,
  namedtuples, `datetime`, and anything defining `__replace__()`.

## `pathlib`

- **`Path.from_uri()`**: Build a `Path` from a `file://` URI.
- **`PurePath.full_match()`**: Shell-style matching including `**`.
- **`glob()` / `rglob(recurse_symlinks=...)`**: Control symlink recursion.
- **`follow_symlinks=` on `is_file()`, `is_dir()`, `owner()`, `group()`**.

## `itertools`

- **`batched(strict=True)`**: Raise if the final batch is short.

## `argparse`

- **`add_argument(deprecated=True)`**: Deprecate options and subcommands.

## `glob`

- **`translate()`**: Convert a shell wildcard pattern to a regex.

## `math` / `statistics`

- **`math.fma()`**: Fused multiply-add with a single rounding.
- **`statistics.kde()` / `kde_random()`**: Kernel density estimation.

## `queue` / `asyncio`

- **`Queue.shutdown()`** (both sync and asyncio): Terminate queues cleanly
  instead of sentinel items.
- **`asyncio.as_completed()`**: Now also an async iterator.

## Other stdlib

- **`base64.z85encode()` / `z85decode()`**: Z85 encoding.
- **`os.process_cpu_count()`**: CPUs usable by this process (vs `cpu_count()`).
- **`dbm.sqlite3`**: New default dbm backend.
- **`mimetypes.guess_file_type()`**: Guess from a path (vs URL).
- **`re.PatternError`**: Clearer name for `re.error`.
- **`enum.EnumDict`**: Now public for `EnumType` subclassing.
- **`str.replace()`**: `count` can be passed as a keyword.
- **`exec()` / `eval()`**: `globals` and `locals` as keywords.
- **`array.array('w')`**: Unicode type code replacing deprecated `'u'`;
  also new `clear()` method.
