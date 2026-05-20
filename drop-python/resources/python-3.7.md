# Dropping Python 3.7

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax

- **Walrus operator (`:=`)**: Assignment expressions for loops, conditions, and
  comprehensions to avoid duplicate function calls.
- **Positional-only parameters** (`/`): Force parameters to be positional (like C
  functions)
- **`return` / `yield` with unpacking**: `return a, *b, c` without parens

## f-strings

- **`f'{expr=}'`**: Self-documenting debug formatting

## Standard library

- **`importlib.metadata`**: Read package metadata (version, entry points) at
  runtime without needing `pkg_resources`.
- **`asyncio.run()`**: Stable API for running coroutines (formerly provisional).
- **`asyncio.Task` names**: `create_task(name=...)`, `set_name()`, `get_name()`.
- **`functools.cached_property`**: Cache computed properties for instance lifetime.
- **`functools.lru_cache`**: Can now be used as straight decorator `@lru_cache`.
- **`functools.singledispatchmethod`**: Generic methods via single dispatch.
- **`math.comb()`, `math.perm()`, `math.isqrt()`**: Combinatorics and integer
  square root.
- **`math.dist()`, `math.hypot()`**: N-dimensional Euclidean distance.
- **`statistics.fmean()`, `statistics.geometric_mean()`, `statistics.harmonic_mean()`**
- **`typing.Final`, `typing.Literal`**: At runtime (may need `typing_extensions`
  backport on 3.7).
- **`typing.Protocol`**: Structural subtyping at runtime (may need
  `typing_extensions`).
- **`pathlib.Path.link_to()`**: Create hard links.
