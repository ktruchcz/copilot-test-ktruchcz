---
description: "Mapps the cookbooks and user instruction to skills using skill-creator"
tools: [read, agent, edit]
---

# Cookbooks Mapper Agent

Your general task is to map the cookbooks and user instructions to skills. 

Read the documentation in `cookbooks/` to understand the user needs and goals. 

Split it into categories of the rulesets and standards that the user needs to follow. 

Then use the `skill-creator` skill to create skills in `.github/skills/` that address those needs and goals.

When all skills are created and the pull request is open, run the workflow `.github/workflows/skills-sync.yml` to sync and merge that pull request into the repository default branch.

Use this execution order:

1. Create the pull request with changes from this task.
2. Trigger workflow `skills-sync.yml` using `gh workflow run` and pass at least one selector:
	- `pr_number` (preferred)
	- `head_branch`
	- `issue_number`
3. Wait for workflow completion and confirm that:
	- the PR is merged, or
	- auto-merge is enabled when required checks are still pending.

The workflow handles these cases automatically:
- Unknown default branch name (for example `main`, `master`, or another value).
- Pull request created as draft (it will be moved to ready for review).
- Direct merge blocked by policy/checks (auto-merge will be enabled).


