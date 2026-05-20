# Dropping Python 3.8

Things to look for that Ruff doesn't auto-fix (`UP*` rules):

## Syntax

- **Dictionary merge (`|=`, `|`)**: Replace manual `for k, v in d2: d1[k] = v` loops or
  `copy()` + `update()` chains.

## Strings

- **`str.removeprefix()` / `str.removesuffix()`**: Replace manual slice calculations or
  regex-based stripping for known prefixes/suffixes.

## `math`

- **`math.comb()` / `math.perm()`**: Replace manual combinatoric implementations.
- **`math.isqrt()`**: Replace `int(math.sqrt(n))`.
- **`math.prod()`**: Replace manual `reduce(operator.mul, iterable, 1)` or loop.

## `statistics`

- **`statistics.fmean()`**: Replace `mean()` when fast float arithmetic is desired.
- **`statistics.geometric_mean()` / `harmonic_mean()`**: Replace manual implementations.

## `typing`

- **`typing.Protocol` at runtime**: Before 3.8, `Protocol` was in `typing_extensions`.
- **`typing.Final` / `Literal`**: Same, check for backports.

## New modules

- **`graphlib`**: `graphlib.TopologicalSorter` can replace manual topological sort
  implementations.

## `zoneinfo`

- **`zoneinfo`**: Replace `dateutil` or `pytz` usage for standard timezone handling
  where possible.
