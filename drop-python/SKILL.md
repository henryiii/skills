---
name: drop-python
description: Use when dropping a Python version from a project
license: MIT
compatibilty: Requires uv
---

# Dropping Python Support

This guide provides step-by-step instructions for removing a Python support
from a project. If the user doesn't specify a version, assume the lowest
supported version is being bumped by one. Always drop one Python version at a
time.

Below, `<minor>` is used instead of a specific digit; if dropping 3.9, then
`<minor>` is 9.

## Before You Start

- `uv` is required, quit if they are not installed. You can run any
  other project-specific tools via `uvx`, such as `nox` -> `uvx nox` and `prek`
  -> `uvx prek` if they are not present.
- `prek` is a faster Rust rewrite of `pre-commit` with the same config and
  similar options. `prek -a --quiet` is best for running it.

## Key Steps

### 1. Update `pyproject.toml` (or `setup.cfg` or `setup.py`)

Update Python version classifiers and requirements with the new minimum
version. For example, if dropping Python 3.9:

```toml
[project]
requires-python = ">=3.10"
classifiers = [
    "Programming Language :: Python :: 3",
    # Remove "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    # ...
]
```

### 2. Update CI/CD Configuration

If the next version is already tested, drop it. If not, update from the old to the new.

* GitHub Actions (`.github/workflows/*.yml`). Read every file, not only the main
  one. Reusable workflows, nightly jobs and packaging jobs each pin a version.
* AppVeyor (`.appveyor.yml` or `appveyor.yml`)
* Other CI systems: `.gitlab-ci.yml`, `.circleci/config.yml`,
  `azure-pipelines.yml`, `.travis.yml`
* Docs and task runners: `.readthedocs.yml`, `tox.ini`, `noxfile.py`

Some CI systems write the version without a dot, as a path or a bare number.
AppVeyor is the common example:

```yaml
environment:
  matrix:
  - PYTHON: 38     # expands to C:\Python38
```

A search for `3.8` does not find this. Use the undotted search in step 10.
Linux container jobs do the same, for example `dnf install python38-devel`.

### 3. Update Pre-commit Hooks

Check `.pre-commit-config.yaml` for anything pinned to to the old version.

### 4. Update other configuration

Some tools also pin in pyproject.toml. Check for `3.<minor> and 3<minor>` text. Some common locations:

* ruff: Usually Ruff reads `project.requires-python`, but if it's hardcoded, it's `tool.ruff.target-version` in pyproject.toml or `ruff.target-version` in `ruff.toml` or `.ruff.toml`
* mypy: `tool.mypy.python_version`
* pylint: `tool.pylint.py-version` (can also be `tool.pylint.master.py-version` (deprecated) or `tool.pylint.main.py-version`)

### 5. If cibuildwheel is used

Check for usage of `cp3<minor>` / pp3<minor>` in `[tool.cibuildwheel]` as well as in the CI.

### 6. Run Automated Upgrades

```bash
prek -a --quiet
```

### 7. Review & Modernize Code


Custom patterns to look for, for specific versions of Python are provided:

* Python 3.7: Read resources/python-3.7.md
* Python 3.8: Read resources/python-3.8.md
* Python 3.9: Read resources/python-3.9.md
* Python 3.10: Read resources/python-3.10.md
* Python 3.11: Read resources/python-3.11.md
* Python 3.12: Read resources/python-3.12.md
* Python 3.13: Read resources/python-3.13.md
* Python 3.14: Read resources/python-3.14.md

### 8. Update Documentation

- Update README, CONTRIBUTING, and docs
- Update installation requirements

### 9. Test & Validate


If the project has::

```toml
[dependency-groups]
dev = # ...
```

Then run:

```
uv run pytest
```

Otherwise check for nox or tox, and run that.

### 10. Double-check for Remaining References

Run all of these. Each one finds references that the others miss.

```bash
# 1. Dotted: 3.<minor>
git grep -nE '(^|[^0-9.])3\.<minor>([^0-9]|$)'

# 2. Undotted, with the prefix attached. This is the one people forget.
#    Finds C:\Python38, python38-devel, cp38, pp38, py38, abi3-py38
git grep -nE '(py|cp|pp|python|PYTHON|Python)-?3<minor>'

# 3. Version tuples
git grep -nE '3, ?<minor>'

# 4. Bare number. Run this one too: it is the only search that finds a version
#    held apart from its name, such as `PYTHON: 38` or `PY=38`, which search 2
#    misses. Expect noise from unrelated numbers, so read the hits instead of
#    trusting the count.
git grep -nE '(^|[^0-9.])3<minor>([^0-9]|$)'
```

Exclude generated and vendored paths to cut the noise, for example
`':!docs/changelog.md' ':!*.svg'`.

#### C and C++ projects

Extension and header projects gate on `PY_VERSION_HEX`. The minor version is
hex, so 3.8 is `0x030800`, 3.9 is `0x030900`, and 3.10 is `0x030A00`.

```bash
git grep -nE '0x030<minor-hex>'
```

Docs often repeat test code in a `code-block`. If you change a guard in a test,
grep the docs for the same lines. A test file may say to keep the two in sync.

#### Reverse sweep: guards that are now always true

This step finds the real dead code. After the drop, any check for the new
minimum `<new>` is always true, so the branch it guards can go. Search for the
*new* version, not the old one.

```bash
git grep -nE '0x030<new-hex>'                 # C/C++: #if PY_VERSION_HEX >= <new>
git grep -n 'version_info < (3, <new>)'       # Python: always False now
git grep -n 'version_info >= (3, <new>)'      # Python: always True now
```

Remove the dead branch and un-indent the live one. Delete helpers that only the
dead branch used, and any include or import that then goes unused.

#### While you are there: always-False version checks

`sys.version_info` is a 5-element tuple, so `== (3, 9)` can never be true. This
bug hides for years because the guarded code simply never runs.

```bash
git grep -nE 'version_info[[:space:]]*==[[:space:]]*\(3, ?[0-9]+\)'
```

Note: `git grep -E` uses POSIX ERE, which has no `\s`. A pattern with `\s`
matches nothing and prints no error, so it looks like a clean result. Use
`[[:space:]]`, or use `git grep -P` for Perl syntax.

The fix is `sys.version_info[:2] == (3, 9)`. Do not repair it silently: a
comparison that was always False guards a branch that has never run, so
"fixing" it turns on untested code. Report it and let the user choose between
the fix and deleting the branch.

