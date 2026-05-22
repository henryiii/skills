---
name: secure-ci
description: "Use when user asks to secure a repo's CI"
license: "MIT"
compatibilty: Requires uvx (from uv) and npx (from nodejs).
---

# Secure actions

## Step 0: setup

* If the user doesn't specify a cooldown, assume 7 days.
* Check to see if `.pre-commit-config.yaml` exists; don't add one if it's not already there.
* Assume monthly grouped updates unless a user asks for weekly or quarterly instead.

## Step 1: actions

Fully pin GHA. Use `npx actions-up -y --min-age=7 --style=sha
--include-branches` to update and pin.  Make sure all the updates are to the
same or newer tags - the sorting mechanim for actions-up fails sometimes, like
going from year based releases to old SemVer releases, or grabbing a tag that's
not a normal release.

## Step 2: zizmor

The repo should use zizmor. If .pre-commit-config.yaml exists, this is a good hook:

```yaml
  - repo: https://github.com/zizmorcore/zizmor-pre-commit
    rev: a4727cbbcd26d7098e96b9cb738169b59711ae51  # frozen: v1.24.1
    hooks:
      - id: zizmor
        files: "^\\.github"
        args: [--persona=pendatic]
```

Run `uvx zizmor --persona=pedantic .github` directly. Fix up the problems reported.
You can request auto-fixes with `--fix=safe` or `--fix=all` for some of the checks.

Common problems / fixes:

* If you need configuration, it should go into `.github/zizmor.yaml`.
* The copilot-setup-steps.yml file is special - it does not need a concurrency setting. Ignore this check if zizmor thinks otherwise.
* Ask the user if unsure on a fix.
* Template expansion issues can be passed in via an environment variable instead.

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
have `autoupdate_schedule` set,  set it.

## Step 5: Isolate deploy jobs

All deploy jobs should run seperatly from build jobs, to minimize the number of
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

## Final report

Run `prek -a --quiet` if using pre-commit to make sure all changes pass.

Provide a concise bullet point summary of each change.
