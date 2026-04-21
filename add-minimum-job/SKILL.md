---
name: add-minimum-job
description: Add a minimum version test job to a noxfile
license: MIT
---

# Adding a Minimum Version Job to Noxfile

This skill helps you add a `minimums` session to your project's `noxfile.py` that tests your package with the lowest direct dependencies. This is useful for verifying that your package's declared minimum version constraints are correct.

## Before You Start

### Prerequisites

- Your project must have a `noxfile.py` file
- `uv` should be installed (for the `uv` venv backend)
- `nox` should be available

### Check Current Setup

Verify your noxfile doesn't already have a minimum version test:

```bash
grep -E "@nox\.session.*minimum|@nox\.session.*mintest" noxfile.py
```

If a session already exists, you may want to update it instead of creating a new one.

## Step-by-Step Guide

### 1. Understanding the Minimum Job

The minimum version job:
- Uses `uv` as the venv backend for fast environment creation
- Installs dependencies with `--resolution=lowest-direct` to get the minimum allowed versions
- Runs your test suite to ensure it works with minimum versions
- Helps catch cases where your version constraints are too loose

### 2. Add the Session to Your Noxfile

Add this session to your `noxfile.py`. The exact placement and details depend
on your project structure. Compare to the main "tests" or similar job.

#### Basic version (for projects using dependency-groups):

```python
@nox.session(venv_backend="uv", default=False)
def minimums(session: nox.Session) -> None:
    """
    Test the minimum versions of dependencies.
    """
    session.install("-e.", "--group=test", "--resolution=lowest-direct")
    session.run("pytest", *session.posargs)
```

#### For projects without dependency-groups (legacy approach):

```python
@nox.session(venv_backend="uv", default=False)
def minimums(session: nox.Session) -> None:
    """
    Test with minimum versions of all dependencies.
    """
    session.install("-e.[test]", "--resolution=lowest-direct")  # Adjust extras as needed
    session.run("pytest", *session.posargs)
```


### 3. Choose Your Configuration

The best configuration depends on your project. Consider:

- **Do you use dependency-groups?** Use `--group=test` approach
- **Do you use extras?** Use `-e.[test]` approach
- **Do you need to test a specific Python version?** Specify `python=VERSION`
- **Do you need binary-only installations?** Add `--only-binary=:all:`

### 4. Optional Enhancements

#### Show installed versions:

```python
session.run("uv", "pip", "list")
```

This helps debug version resolution issues.

#### Set coverage reporting (if using coverage):

```python
session.install("-e.", "--group=test", "--resolution=lowest-direct")
session.run("pytest", "--cov", "--cov-report=xml", *session.posargs)
```

### 5. Test Your New Session

Run your new session to verify it works:

```bash
# Run the minimums job
nox -s minimums

# Run with specific tests
nox -s minimums -- tests/test_core.py

# Run with pytest options
nox -s minimums -- -v -k specific_test
```

### 6. Verify Results

Check that:
- The session completes successfully
- Tests pass with minimum versions
- The reported installed versions are at or near your declared minimums

If tests fail:
1. The failure message will tell you which dependency has the problem
2. Check your `pyproject.toml` or `setup.py` for the version constraint
3. Either update the constraint to match what works, or update your code to handle the older version

### 7. Add to CI/CD

Consider adding the minimum version job to your GitHub Actions workflow:

```yaml
- name: Run minimum versions test
  run: nox -s minimums
```

This ensures minimum versions stay valid on every commit.

## Common Issues


### Issue: Resolution fails or conflicts occur

**Solution:** This usually means your version constraints are too loose. Review the error message and update minimum versions in `pyproject.toml`.

### Issue: Some tests fail with minimum versions

**Solution:** Your code may be using features only available in newer versions. Either:
1. Update your code to work with the minimum version
2. Increase the minimum version constraint

### Issue: `--resolution=lowest-direct` is not recognized

**Solution:** You need to use the `uv` backend.

## Examples from Real Projects

### pypa/pyproject-metadata

Uses dependency-groups and shows installed versions:

```python
@nox.session(venv_backend="uv", default=False, python=ALL_PYTHONS)
def minimums(session: nox.Session) -> None:
    """
    Check minimum requirements.
    """
    test_grp = nox.project.dependency_groups(PYPROJECT, "test")
    session.install("-e.", "--resolution=lowest-direct", *test_grp, silent=False)
    xmlcov_output = (
        Path(session.virtualenv.location) / f"coverage-{session.python}-min.xml"
    )
    session.run(
        "pytest",
        "--cov",
        f"--cov-report=xml:{xmlcov_output}",
        "--cov-report=term-missing",
        "--cov-context=test",
        "tests/",
        *session.posargs,
    )
```

### scikit-hep/hist

Simple and direct:

```python
@nox.session(venv_backend="uv", default=False)
def minimums(session):
    """
    Run with the minimum dependencies.
    """
    session.install("-e.", "--group=test", "--resolution=lowest-direct")
    session.run("uv", "pip", "list")
    session.run("pytest", *session.posargs)
```

### scikit-hep/iminuit

Tests the minimum Python version with minimum dependencies:

```python
@nox.session(python=MINIMUM_PYTHON, venv_backend="uv")
def mintest(session: nox.Session) -> None:
    """Run tests on the minimum python version."""
    session.install("--only-binary=:all:", "-e.", "--resolution=lowest-direct")
    session.install("pytest", "pytest-xdist")
    extra_args = session.posargs if session.posargs else ("-n=auto",)
    session.run("pytest", *extra_args)
```

## Verification Checklist

After adding the minimum version job:

- [ ] `nox -s minimums` runs without errors
- [ ] All tests pass with minimum versions
- [ ] `uv pip list` (or `pip list`) shows versions at or near minimums
- [ ] CI/CD passes (if integrated)
- [ ] Version constraints in `pyproject.toml` are accurate

## See Also

- [Nox documentation](https://nox.thea.codes/)
- [Scientific Python Developer Guide](https://scientific-python.org/contribute/dev-guide/)
- [uv documentation](https://docs.astral.sh/uv/)
- [PEP 440: Version Identification](https://www.python.org/dev/peps/pep-0440/)
