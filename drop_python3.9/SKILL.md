---
name: drop-python3-9
description: How to remove Python 3.9 support and upgrade to 3.10
license: MIT
---

# Dropping Python 3.9 Support

This guide provides step-by-step instructions for removing Python 3.9 support from a project.

## Before You Start

- Confirm Python 3.9 is the current minimum by looking at the locations listed
  in step 1. Only one version should be dropped at a time.
    - If 3.8 or earlier, stop and tell the user they need to drop 3.8 first.
    - If 3.10 or later, there's nothing to do, stop and congratulate the user.
- `uv` and `prek` are required, quit if they are not installed. You can run any
  other project-specific tools via `uvx`, such as `nox` -> `uvx nox`.

## Key Steps

### 1. Update `pyproject.toml` (or `setup.cfg` or `setup.py`)

Update Python version classifiers and requirements:

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

Remove Python 3.9 from test matrices:

**GitHub Actions (`.github/workflow/*.yml`):**

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12', '3.13']
    # Removed: '3.9'
```

### 3. Update Pre-commit Hooks

Check `.pre-commit-config.yaml` for anything pinned to 3.9 / 39. Note that we
use `prek` instead of `pre-commit`, it's a Rust rewrite with the same config.

### 4. Update other configuration

Usually Ruff reads `project.requires-python`, but if it's hardcoded:

```toml
[tool.ruff]
target-version = "py310"
```

MyPy is pretty common:

```toml
[tool.mypy]

```

As is pylint (may have a `master` (deprecated) or `main` prefix, but not required):

```toml
[tool.pylint]
py-version = "3.10"
```
### 5. If cibuildwheel is used

Check for usage of cp39 / pp39 in `[tool.cibuildwheel]` as well as in the CI.

### 6. Run Automated Upgrades

```bash
# Upgrade Python syntax to 3.10+ (ruff via prek)
prek -a
```

### 7. Review & Modernize Code

Manually review common Python 3.9 → 3.10+ patterns.

If Ruff is used, these should be handled already:

* `Dict`, `List`, `Optional` from `typing` now can use built-ins, like `dict`, `list`, `| None`
* `Union[X, Y]`  should now be `X | Y`

Check to see if anything reads better with pattern matching.

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
# Search for 3.9 references
git grep "\b3\.9\b"
git grep "\bpy39\b"
git grep "3, 9"
```

