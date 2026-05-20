# henryiii/skills

This is a collection of skills following the open https://agentskills.io
specification. They have been tested using OpenCode and the open models like
Kimi, GLM, and Gemma, but anything else should work too. Note that `pi` does
not tell the model what model it is.

Skills:

* branch-and-pr: Make a branch (if not on one), make a conventional commit, make a PR via `gh`
* add-minimum-job: Add a minimum version test job to a noxfile
* drop-python: Drop Python (provide version, or drops lowest)
* sp-recommends: Follow the Scientific-Python Developer Guide, using sp-repo-review
* secure-ci: Secure a repository's CI

To use:

Grab a folder and drop it in to your tool's location.

You can also install a skill using the `gh` tool, with:

gh skill install henryiii/skills

(Requires a recent version of GitHub's CLI.)

Scripts:

There's also a helper script, `scripts/opencode-copilot.py`, that launches
copilot CLI using an opencode model configuration. Useful if you have a custom
provider and want to try copilot CLI.
