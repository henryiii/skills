# henryiii/skills

This is a collection of skills following the open <https://agentskills.io>
specification. They have been tested using OpenCode and the open models like
Kimi, GLM, and Gemma, but anything else should work too. Note that `pi` does
not tell the model what model it is.

Skills:

* branch-and-pr: Make a branch (if not on one), make a conventional commit, make a PR via `gh`
* add-minimum-job: Add a minimum version test job to a noxfile
* drop-python: Drop Python (provide version, or drops lowest)
* sp-recommends: Follow the Scientific-Python Developer Guide, using sp-repo-review
* secure-ci: Secure a repository's CI
* explore-issues: Mirror a repo's GitHub issues into SQLite, then triage/categorize them

To use:

Grab a folder and drop it in to your tool's location (`~/.agents/skills` works
for most tools). Or symlink it from the repo.

You can also install a skill using the `gh` tool, with:

gh skill install henryiii/skills

(Requires a recent version of GitHub's CLI.)

Scripts:

There's also a helper script, `scripts/opencode-copilot.py`, that launches
copilot CLI using an opencode model configuration. Useful if you have a custom
provider and want to try copilot CLI.

My global config (`~/.config/opencode/AGENTS.md`, `~/.pi/agent/APPEND_SYSTEM.md`, for example):

```
You are on <OS>. The github user is <USER>. `python3` can be used if python
without dependencies is needed. Use `uv run` if in a python package.

Use relative paths when possible.

Use `prek -a --quiet` instead of `pre-commit run -a` for linting

If you make a commit, follow conventional commits and add a trailer:
`Assisted-by: <harness>:<model>`, where `<harness>` is the current agent
harness, and `<model>` is the AI model.
```

* OS and USER can be replaced by your OS and GH username
* Relative paths help small models (local AI) which have trouble writing text correctly)
* Pi does not inject the model name, so it's usualy wrong
