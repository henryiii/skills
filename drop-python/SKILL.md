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

* GitHub Actions (`.github/workflow/*.yml`)
* Other common CI systems

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

* Python 3.7: Read resources/python-37.md
* Python 3.8: Read resources/python-38.md
* Python 3.9: Read resources/python-39.md
* Python 3.10: Read resources/python-310.md
* Python 3.11: Read resources/python-311.md
* Python 3.12: Read resources/python-312.md
* Python 3.13: Read resources/python-313.md
* Python 3.14: Read resources/python-314.md

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

```bash
# Search for 3.<minor> references
git grep "\b3\.<minor>\b"
git grep "\bpy3<minor>\b"
git grep "3, <minor>"
```

