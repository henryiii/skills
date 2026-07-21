---
name: explore-issues
description: Use when exploring, triaging, or categorizing all of a repository's GitHub issues, like finding verifiable bugs or grouping issues by topic
license: MIT
compatibility: Requires python3 and an authenticated gh CLI
---

# Exploring GitHub Issues

Mirror a repo's issues into a local SQLite database, then answer questions
about them with SQL and by reading issue bodies. Working locally avoids API
rate limits and lets you query and re-read issues cheaply.

## Step 1: Download the issues

Find the repo as `owner/name`. If the user didn't name one, use the current
directory's repo: `gh repo view --json nameWithOwner --jq .nameWithOwner`.

Store the database outside the repo so it can't be committed, then download:

```bash
scripts/github-issues-to-sqlite.py <owner>/<name> -c -d /tmp/<owner>-<name>-issues.db
```

Options worth knowing:

* `-c` also fetches comment bodies. Include it; comments often hold the answer.
* `-s all` (or `closed`) if the user's question covers closed issues; the
  default is open only.
* `--include-prs` if the user wants pull requests too.
* Re-running the same command refreshes the database (it upserts). If the
  database already exists from earlier in the session, refresh instead of
  re-exploring stale data.
* `--schema` prints the schema.

## Step 2: Get oriented

Tables: `issues` (number, title, state, state_reason, body, author, milestone,
comments, is_pull, locked, html_url, created_at, updated_at, closed_at),
`labels` and `assignees` (issue_number, name/login), `comments`
(issue_number, author, body, created_at).

Start with a shape check before reading anything:

```bash
sqlite3 /tmp/<name>-issues.db "SELECT count(*) FROM issues;
  SELECT name, count(*) FROM labels GROUP BY name ORDER BY 2 DESC;"
```

If `sqlite3` is missing, run queries through `python3 -c` with the `sqlite3`
module instead.

## Step 3: Explore

Use SQL to narrow, then read the survivors in full. Useful patterns:

```sql
-- Unlabeled issues (often the triage backlog)
SELECT number, title FROM issues WHERE state='open' AND is_pull=0
  AND number NOT IN (SELECT issue_number FROM labels);

-- Keyword search across bodies and comments
SELECT DISTINCT i.number, i.title FROM issues i
  LEFT JOIN comments c ON c.issue_number = i.number
  WHERE i.body LIKE '%segfault%' OR c.body LIKE '%segfault%';

-- Oldest open, most-discussed, etc.
SELECT number, title, comments FROM issues WHERE state='open'
  ORDER BY comments DESC LIMIT 20;
```

To read one issue with its comments, formatted:

```bash
scripts/github-issue-show.py <number> -d /tmp/<name>-issues.db
```

## Common tasks

### Categorize issues

Pull `number, title, substr(body, 1, 500)` for all matching issues and read
them in batches (100–200 at a time for large repos). Assign each issue to a
category; titles plus the body excerpt are usually enough, so only fetch the
full issue when they aren't. Present the result as a table of categories with
counts and issue numbers, and call out issues that fit no category rather
than forcing them.

### Find verifiable bugs

A bug is *verifiable* when the report contains enough to confirm it: concrete
reproduction steps or code, an error message or traceback, or a clearly wrong
output for a given input. Feature requests, questions, and "it doesn't work"
with no detail don't qualify.

1. Collect candidates by label (`bug`, `defect`, ...) and by keyword
   (`traceback`, `error`, `crash`, `regression`, `reproduce`).
2. Read each candidate in full, including comments — later comments often add
   the reproduction or reveal the issue was resolved or invalid.
3. Report each issue as verifiable / not verifiable / needs-info, with one
   line of justification.

### Reporting

Link issues by their `html_url` so the user can click through. State which
issue set you covered (open only? PRs included?) and when the data was
downloaded, since the mirror goes stale.

This skill is read-only. If the user then wants labels, comments, or state
changes applied on GitHub, that's `gh issue edit` / `gh issue comment` —
confirm the exact changes first.
