---
name: secure-ci
description: "Use when user asks to secure a repo's CI"
license: "MIT"
---

# Secure actions

## Step 0: setup

* If the user doesn't specify a cooldown, assume 7 days.
* Check to see if `.pre-commit-config.yaml` exists; don't add one if it's not already there.
* Assume monthly grouped updates unless a user asks for weekly or quarterly instead.

## Step 1: actions


Fully pin GHA. Use `npx actions-up -y --min-age=7 --style=sha --include-branches` to update and pin.

## Step 2: zizmore

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

If the user does not have a pre-commit config file, or has any configuration in
the `ci:` block in that file, leave off the `pre-commit` ecosystem.

If a user does have a `ci:` section in `.pre-commit-config.yaml`, but doesn't
have `autoupdate_schedule` set,  set it.

The old alias `"actions"` can be updated to `"github-actions"`.

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
