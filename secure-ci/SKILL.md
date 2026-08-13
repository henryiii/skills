---
name: secure-ci
description: "Use when user asks to secure a repo's CI"
license: "MIT"
compatibility: Requires uvx (from uv) and npx (from nodejs).
---

# Secure actions

## Step 0: setup

* If the user doesn't specify a cooldown, assume 7 days. The steps below write
  this value in several places; use the same number in all of them.
* Check to see if `.pre-commit-config.yaml` exists; don't add one if it's not already there.
* Assume monthly grouped updates unless a user asks for weekly or quarterly instead.
* Keep the change set to CI security. If an update makes unrelated source code
  fail, see "Keep the scope small" below.

## Step 1: actions

Fully pin GHA. Use `npx actions-up -y --min-age=7 --style=sha
--include-branches` to update and pin (`--min-age` takes the cooldown in days).
Make sure all the updates are to the same or newer tags - the sorting mechanism
for actions-up fails sometimes, like going from year based releases to old
SemVer releases, or grabbing a tag that's not a normal release.

actions-up skips an action if its newest release is inside the cooldown, and
then the action stays unpinned. After the run, search the workflows for any ref
that is not a SHA. Pin each one by hand to the SHA of the tag it uses now. Do
not bump the version at the same time; dependabot does that later.

Each pin needs a version comment, like:

```yaml
      - uses: actions/checkout@<sha>  # v7.0.1
```

Report all major version changes in the final summary. They are the most likely
cause of a CI failure.

## Step 2: zizmor

The repo should use zizmor. If .pre-commit-config.yaml exists, this is a good hook:

```yaml
  - repo: https://github.com/zizmorcore/zizmor-pre-commit
    rev: 451b56af716f9f0d0c2b816503a3fd0cf8b036fa  # frozen: v1.29.0
    hooks:
      - id: zizmor
        files: "^\\.github"
        args: [--persona=pedantic]
```

Run `uvx zizmor --persona=pedantic .github` directly. Fix up the problems reported.
You can request auto-fixes with `--fix=safe` or `--fix=all` for some of the checks.

Common problems / fixes:

* `artipacked`: add `persist-credentials: false` to each checkout step. If a job
  really needs the credentials, like a job that pushes a tag, set
  `persist-credentials: true` and say why in a comment.
* `excessive-permissions`: add `permissions: {}` at workflow level, then give
  each job only the permissions it uses.
* `undocumented-permissions`: add a comment that says why the job needs each
  permission. The comment must be on the same line. A comment on the line above
  does not clear the finding:

  ```yaml
      permissions:
        id-token: write  # trusted publishing to PyPI
  ```
* `unpinned-uses`: see step 1.
* Add a `concurrency` group to each workflow.
* The copilot-setup-steps.yml file is special - it does not need a concurrency setting. Ignore this check if zizmor thinks otherwise.
* Template expansion issues can be passed in via an environment variable instead.
* If you need configuration, it should go into `.github/zizmor.yml`. zizmor also
  reads `.yaml`; if the repo has that spelling already, keep it. Prefer a fix
  over an ignore. If you must ignore, say why in a comment.
* Ask the user if unsure on a fix.

Template expansion fix example, before:

```yaml
      - run: uv run noxfile.py -s test-${{ matrix.python }}
```

After:

```yaml
      - run: uv run noxfile.py -s test-$PYTHON
        env:
          PYTHON: ${{ matrix.python }}
```

## Step 3: pre-commit (if applicable)

If the user is using pre-commit, run `prek auto-update --freeze --cooldown-days 7` to update and pin to sha.

This can move a hook by a major version, and a new linter version can add new
rules. Both make files fail that have nothing to do with CI security. See "Keep
the scope small".

Look at each new rev before you keep it. Do not accept a pre-release (alpha,
beta, rc). If the hook repo is archived, the newest tag can be a pre-release
that nobody supports; tell the user, and keep the current rev until they choose
a maintained replacement.

## Step 4: dependabot

If the user does not use `.github/dependabot.yml`, add one like this:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    groups:
      github-actions:
        patterns:
          - "*"
    cooldown:
      default-days: 7
```

The old alias `"actions"` can be updated to `"github-actions"`.

If the package has a `.pre-commit-config.yaml` but there's no `ci:` field in
it, add this to `.github/dependabot.yml`:

```yaml
  - package-ecosystem: "pre-commit"
    directory: "/"
    schedule:
      interval: "monthly"
    groups:
      pre-commit:
        patterns:
          - "*"
    cooldown:
      default-days: 7
```

If a user does have a `ci:` section in `.pre-commit-config.yaml`, but doesn't
have `autoupdate_schedule` set, set it.

## Step 5: Isolate deploy jobs

All deploy jobs should run separately from build jobs, to minimize the number of
packages that run with access to deploy permissions. Use artifact
upload/download to provide the required files for the deploy job.

## Step 6: Add cooldowns to common locations

If this repo uses uv anywhere and has a pyproject.toml, add:

```toml
[tool.uv]
exclude-newer = "7 days"
```

If there's any sign this repo uses `pixi`, add `exclude-newer = "7d"` to the
tool pixi table in `pyproject.toml` or `pixi.toml`

## Keep the scope small

This change set is about CI security. Do not change source code, lint
configuration, or test code to make a new tool version pass.

If a hook or action update makes unrelated code fail, hold that one item at the
version the repo uses now, still frozen to its SHA, and tell the user it needs
its own change set. Only fix the code if the user asks for it.

## Final report

Check the result before you report:

* `uvx zizmor --persona=pedantic .github` reports no findings.
* `prek -a --quiet` passes, if the repo uses pre-commit.
* No workflow ref is a tag or a branch; all are SHAs with a version comment.

Provide a concise bullet point summary of each change. Also list:

* Each major version change.
* Each item you held back, and why.
* Each zizmor ignore you added, and why.
