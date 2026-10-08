---
name: parallel-ci
description: "Use when the user asks to speed up GitHub Actions jobs with parallel or background steps"
license: "MIT"
compatibility: Requires gh (GitHub CLI) and jq.
---

# Parallel steps in GitHub Actions

GitHub Actions can run steps of one job at the same time (announced 2026-06-25).
Use this to overlap steps that do not depend on each other. Do not split jobs.

## Syntax

```yaml
steps:
  # Start a step and continue. Give it an id so you can wait for it.
  - name: Install deps
    id: deps
    background: true
    run: ./install.sh

  - run: ./other-setup.sh

  # Block until the step finishes. Takes an id or a list of ids.
  - name: Wait for deps
    wait: deps          # or: wait: [deps, other]

  # Shorthand: run all steps in the group, then wait for all of them.
  - parallel:
      - name: Python tests
        run: python -m pytest
      - name: Docs
        run: make docs
```

Also: `wait-all:` (no value) waits for all background steps, and `cancel: <id>`
stops a background step (SIGTERM, then SIGKILL).

Rules:

* A maximum of 10 background steps run at the same time in one job.
* Outputs and `$GITHUB_ENV`/`$GITHUB_PATH` changes from a background step are
  only visible after a `wait`/`wait-all` that includes it.
* A failed background step fails the job at the next `wait` that includes it.
* `wait`, `wait-all`, and `cancel` always run. They do not accept `if:`.
* Composite actions cannot contain `background` or `parallel`.
* The current reference is the "workflow syntax" page in the GitHub docs
  (`jobs.<job_id>.steps[*].background`). Read it if a rule here seems wrong.

## Step 1: measure

Do not guess. Get the step times from the last successful run on the default
branch:

```bash
id=$(gh run list -w <workflow> -b <default-branch> -s success -L1 --json databaseId -q '.[0].databaseId')
gh api "repos/<owner>/<repo>/actions/runs/$id/jobs?per_page=100" --paginate -q '
  .jobs[] | "\(.name)\n" + ([.steps[] | select(.started_at and .completed_at)
  | "  \(((.completed_at|fromdateiso8601)-(.started_at|fromdateiso8601)))s \(.name)"] | join("\n"))'
```

Find the job with the longest total time. That job sets the wall-clock time of
the run, so a saving there is worth the most.

## Step 2: find candidates

Good candidates:

* Slow installs (apt, brew, downloads) that run before steps that do not need
  them. Put them in the background and `wait` just before the first step that
  needs them.
* Test steps after a build that are independent, when at least one of them uses
  only one core (for example, pytest without xdist). The other steps can use the
  idle cores.
* Disk cleanup steps next to downloads.

Bad candidates (say so, and skip them):

* Steps that already use all cores, like a parallel compile. Running two of them
  at the same time saves nothing.
* Steps that take less than ~10 s.

## Step 3: check for conflicts

Two steps can run at the same time only if they do not share state. Check each
pair for:

* **Same build tree.** Do not run two `cmake --build`, `ninja`, `make`, or
  MSBuild calls on one build directory at the same time. Ninja has no lock, and
  MSBuild runs `ZERO_CHECK` in each call. Call one tool directly instead (for
  example `python -m pytest` with `working-directory:` set to the build test
  directory, in place of `cmake --build build --target pytest`). Make sure the
  direct call uses the same arguments and directory as the build target did.
* **Package manager locks.** Two `apt-get`/`dpkg` calls (this includes
  `apt-get clean`) cannot run at the same time. Same for `brew`.
* **Changes to a shared environment.** Do not install packages into an
  environment while another step runs tests from it. Move the install to an
  earlier step.
* **Environment from earlier steps.** A step that needs `$GITHUB_ENV` or
  `$GITHUB_PATH` from a background step must come after the `wait`.
* **Disk space.** A download that runs during a cleanup can fill the disk before
  the cleanup frees space.
* **CPU-sensitive tests.** Tests with timeouts or thread timing can become flaky
  when another step uses the CPU. Report this risk.

## Step 4: edit

* Steps with `if:` that select an OS: a `wait` on a skipped step is not
  documented. Merge them into one step with `shell: bash` and a
  `case "$RUNNER_OS"` so that the `wait` always has a step that ran.
* Keep step names the same, so that the logs stay easy to compare.
* If you call a tool directly to avoid a build-tree conflict, add a short
  comment that says why.
* Keep comments that were on the steps you moved.

## Step 5: validate

* Run `prek -a --quiet` if the repo uses pre-commit. Schema checks such as
  `check-github-workflows` and linters such as actionlint or zizmor can reject
  the new keys if they are old. If one does, report it; do not remove the check.
* Push and look at the first run. A workflow with a syntax error fails at once
  with no jobs.
* When the run is done, compare the step times with the times from step 1, and
  report the saving per job. If a job got slower or flaky, say so.
