# henryiii/skills

This is a collection of skills following the open https://agentskills.io
specification. They have been tested using OpenCode and the open Kimi-K2.5
model, but anything else should work too.

Skills:

* add-minimum-job: Add a minimum version test job to a noxfile
* drop-python39: Drop Python 3.9
* sp-recommends: Follow the Scientific-Python Developer Guide, using sp-repo-review

To use:

Either check this repository out at `~/.agents`, or any of the tool specific
locations, or just grab a folder and drop it in to your tool's location.

You can also install a skill using the `gh` tool, with:

gh skill install henryiii/skills

(Requires a very recent version of GitHub's CLI.)

Scripts:

There's also a helper script, `scripts/opencode-copilot.py`, that launches
copilot CLI using an opencode model configuration. Useful if you have a custom
provider and want to try copilot CLI.
