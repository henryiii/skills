# Dropping Python 3.13

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax

- **Deferred annotations (PEP 649/749)**: Remove
  `from __future__ import annotations` and quoted forward references —
  annotations now evaluate lazily by default. Introspect with the new
  `annotationlib` module (`Format.VALUE` / `FORWARDREF` / `STRING`).
- **Template strings (PEP 750)**: `t"..."` literals producing
  `string.templatelib.Template`; safe SQL/HTML/shell building.
- **`except` without parentheses (PEP 758)**: `except A, B:` when there is
  no `as` clause.

## New modules

- **`compression.zstd` (PEP 784)**: Zstandard in the stdlib; `zipfile`,
  `tarfile`, and `shutil` archives support it too. `compression.*` is the
  new namespace for `gzip`/`bz2`/`lzma`/`zlib`.
- **`concurrent.interpreters` (PEP 734)**: Isolated subinterpreters, plus
  `concurrent.futures.InterpreterPoolExecutor`.

## Built-ins

- **`map(..., strict=True)`**: Like `zip`'s strict mode.
- **`bytes.fromhex()` / `bytearray.fromhex()`**: Accept bytes-like input.
- **`float.from_number()` / `complex.from_number()`**: Strict converting
  constructors; `Fraction.from_number()` and `Decimal.from_number()` too.
- **`memoryview` is generic**: Subscriptable in type hints.

## Typing

- **`int | str` now creates `typing.Union`**: `types.UnionType` and
  `Union` are unified — simplifies introspection code that handled both.
- **`io.Reader` / `io.Writer`**: Simple protocols replacing
  `typing.IO`/`TextIO`/`BinaryIO` in annotations.

## `pathlib`

- **`Path.copy()` / `copy_into()` / `move()` / `move_into()`**: Replace
  `shutil` calls for path-to-path operations.
- **`Path.info`**: Cached stat queries (`.info.is_dir()` etc.).

## `functools`

- **`Placeholder`**: Reserve positional slots in `partial()`.

## `heapq`

- **Max-heap functions**: `heapify_max()`, `heappush_max()`,
  `heappop_max()`, etc.

## `uuid`

- **`uuid6()` / `uuid7()` / `uuid8()`** (RFC 9562): `uuid7` gives
  timestamp-ordered keys.

## `argparse`

- **`suggest_on_error=True`**: Suggest fixes for mistyped arguments.
- **`color=True`**: Colored help output.

## Other stdlib

- **`date.strptime()` / `time.strptime()`**: Parse directly to `date`/`time`.
- **`os.reload_environ()`**: Pick up external environment changes.
- **`os.readinto()`**: Read from an fd into a buffer.
- **`contextvars.Token`**: Usable as a context manager.
- **`ProcessPoolExecutor.terminate_workers()` / `kill_workers()`**; also
  `Executor.map(buffersize=...)` to bound queued tasks.

## Behavior changes to check

- **`multiprocessing` default start method**: Now `forkserver` on
  non-macOS Unix (was `fork`) — code relying on inherited state breaks.
- **`NotImplemented` in boolean context**: Now raises `TypeError`.
