# Dropping Python 3.10

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax

- **`except*` (Exception Groups)**: Replace manual exception aggregation/collection
  patterns when handling multiple simultaneous errors.
- **`BaseException.add_note()`**: Enrich exceptions with extra context not
  available at raise time.
- **Starred unpacking in `for`**: `for x, *ys in iterable` now works.

## New modules

- **`tomllib`**: Replace `tomli` (and similar) for TOML reading. Still need
  `tomli_w` or `tomlkit` for writing.

## `asyncio`

- **`TaskGroup`**: Replace `gather()` + manual `create_task()` patterns for
  structured concurrency.
- **`timeout()`**: Prefer over `wait_for()` for timeout context managers.
- **`Barrier`**: New synchronization primitive for coordinating multiple tasks.
- **`StreamWriter.start_tls()`**: Upgrade existing stream connections to TLS.
- **`Runner`**: For programmatic control of event loop lifecycle.

## `typing`

- **`Self`**: For methods returning their own class (alternative constructors,
  context managers, fluent APIs). Replaces manual `TypeVar` patterns.
- **`Required` / `NotRequired`**: Per-field `TypedDict` requirements instead of
  `total=False` + inheritance workarounds.
- **`TypeVarTuple`**: Variadic generics (e.g., array shapes, type-safe variadic
  functions).
- **`LiteralString`**: For sensitive functions (SQL, shell) to enforce only
  literal strings and prevent injection bugs.
- **`dataclass_transform`**: For marking decorators / metaclasses that provide
  dataclass-like transformations.
- **`Never`**: Replaces `NoReturn` in type hints.

## `enum`

- **`StrEnum`**: Members that are strings. Replaces string-mixin enum patterns.
- **`ReprEnum`**: `__repr__` shows name, `__str__`/`__format__` show value.
- **`verify()` / `EnumCheck`**: Runtime validation of enum constraints.
- **`FlagBoundary`**: Control out-of-range flag behavior.
- **`member()` / `nonmember()`**: Explicit member vs non-member decoration.
- **`global_enum()`**: Adjust repr/str to show module-qualified names.

## `datetime`

- **`datetime.UTC`**: Replaces `datetime.timezone.utc`.
- **`fromisoformat()`**: Now parses most ISO 8601 formats.

## `contextlib`

- **`chdir()`**: Context manager for temporary directory changes.

## `inspect`

- **`getmembers_static()`**: Returns members without triggering descriptors.
- **`markcoroutinefunction()`**: Mark sync functions that return coroutines.
- **`getasyncgenstate()` / `getasyncgenlocals()`**: Async generator introspection.

## `logging`

- **`getLevelNamesMapping()`**: Map level names to their numeric values.

## `math`

- **`math.exp2()` / `math.cbrt()`**: Replace `2 ** x` / `x ** (1 / 3)`.

## `operator`

- **`operator.call()`**: `operator.call(obj, *args, **kwargs)`.

## `hashlib`

- **`file_digest()`**: Hash files without reading them entirely into memory.

## `functools`

- **`singledispatch`**: Now supports `types.UnionType` (`X | Y`) annotations.

## `locale`

- **`getencoding()`**: Get the current locale encoding (ignores UTF-8 mode).
