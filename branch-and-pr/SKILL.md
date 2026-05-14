---
name: branch-and-pr
description: "Use when a branch and PR is requested explicitly"
license: "MIT"
compatibility: "Requires git, gh CLI."
---

# Git branch, commit, and make a PR

## Rules:

* **No direct push to main or master** — always open a PR.
* The user's github handle comes from `gh api user --jq .login` unless you already know it
* Conventional Commits is followed

## Definitions:

`<user>`: the user's github handle
`<type>`: a conventional commits type (`feat`, `fix`, `chore`, `style`, `docs`, `test`, `refactor`, `ci`, `perf`). Can be specifed by user input. `chore` is for minor edits that are not fixes/ci/tests.
`<id>`: a short identifier based on the contents of this change.
`<summary>`: a one line description, can be specified by user input or summarize from the diff with main/master or current change.
`<description>`: a longer description, summarized from the diff with main/master or current changes.
`<trailer>`: An Assisted-by git trailer set to tool:model currently used, like `Assisted-by: OpenCode:Kimi-K2.6` or `Assisted-by: Pi:glm-5.1`, for example.


## Make a branch

If the current git branch is main or master, make a new branch with the pattern
`<user>/<type>/<id>`.

## Make a commit

If there are staged changes, make a commit. If there are no changes to commit,
abort the workflow and inform the user. If you are working on changes, you can
add those. The commit message should be `<type>: <summary>\n\n<description>\n\n<trailer>`

## Make a PR

Use the `gh` tool to make a PR. Push to the user's fork if there is one,
otherwise push to the upstream remote if the user has push permission. Make
sure you add this line at the start of the PR description:

:robot: *Human triggered, AI assisted PR. AI text below.* :robot:

So users know the text is generated. Add the `<trailer>` above at the end of
the description.
