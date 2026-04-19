---
name: sp-recommends
description: Review code quality and packaging usuing sp-repo-review for Scientific Python projects
license: BSD-3-Clause
---

# Responding to Scientific Python Repository Recommendations

This skill uses the sp-repo-review tool and helps users address common issues.

## Before You Start

To use this skill, you need `uv` (specifically, the `uvx` runner that `uv`
ships with).

## Step 1: Initial touchup.

Look for some basic things that repos should be doing, and report to the user if needed:

- Project should have `pyproject.toml`
- Project should have `.pre-commit-config.yaml`

These are recommendations from the Scientific Python guide that don't have
automated checks. Apply these first:

- For nox users: use `uv|virtualenv` as the default backend (or `uv` only)
- For GHA: set `FORCE_COLOR: 3` or `--forcecolor` for color output
- For GHA: set up a "pass job" using `re-actors/alls-green` for auto-merge support
- For GHA: configure `.github/release.yml` for changelog generation
- cibuildwheel: Use `build[uv]` as the build frontend for faster builds
- pre-commit: Use schema validation tools (`validate-pyproject`, `check-jsonschema`)
- pre-commit: Consider spell checkers (codespell or typos) if not in pre-commit
- pre-commit: Consider shellcheck for shell scripts

## Step 2: Dependency-groups

If there is no `[dependency-groups]` section (described in PEP 723) in
`pyproject.toml`, you should see if there are developer-focused extras
(`[project.optional-dependencies]`) that can be moved, like `docs`, `tests`, or
`dev`. For dependency-groups, one can reference another with an inline table,
like `dev = [{ include-group = "test" }]`.  It's quite common to want the `dev`
group to be built from other groups.

All mentions of developer extras like `[tests]`, `[docs]`, and `[dev]` need to
be converted to `--group tests` and the like. Most tools have integrated
support for dependency groups in their configuration, like tox and
cibuildwheel. Nox supports `--group` if pip/uv is new enough, which is probably
fine.

## Step 3: sp-repo-review

Run the tool to see what recommendations apply:

```bash
# Get structured JSON output for easier parsing
uvx "sp-repo-review[cli]" --format json | jq -r '.checks | to_entries[] | select(.value.result == false) | "\(.key): \(.value.description)"'

# Or see the human-readable output
uvx --with "sp-repo-review[cli]" sp-repo-review --show err .
```

Focus on checks with `result: false` - these need fixes. Checks with empty
`result` and `skip_reason` are skipped because a prerequisite failed (fix the
prerequisite first).

Only fix things that are fairly easy, and report any harder failures to the user.

A few notes to keep in mind with certain issues:

### Ruff checks

- If the user doesn't have all the recommended Ruff codes, you can run this to get recommendations:

```bash
uvx --from "sp-repo-review[cli]" sp-ruff-checks
```

If the user is using `"ALL"`, then this suggests some optional ignores that are
just sometimes needed.

### Dependabot

An example dependabot file is in `assets/dependabot.yml`.

### GitHub Releases

An example release file is in `assets/release.yml`.

### Nox version

If you add a dependencies at the top, remember to use `nox.needs_version`'s
version as the minimum version there.

## Step 4: Verification

After making changes, verify:

```bash
# Run the full check
uvx "sp-repo-review[cli]" --show err

# Test the package still builds
uv build

# Run tests if available
uv run pytest

# Run the pre-commit checks
uvx prek -a
```
