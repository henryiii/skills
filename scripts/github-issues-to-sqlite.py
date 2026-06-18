#!/usr/bin/env python3
"""Pull a GitHub repo's issues into a SQLite database.

Uses the `gh` CLI for authentication and pagination, so it works with whatever
account `gh auth status` reports. Re-running upserts, so the DB stays current.
"""

import argparse
import json
import sqlite3
import subprocess
import sys
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS issues (
    number       INTEGER PRIMARY KEY,
    title        TEXT,
    state        TEXT,
    state_reason TEXT,
    body         TEXT,
    author       TEXT,
    milestone    TEXT,
    comments     INTEGER,
    is_pull      INTEGER NOT NULL DEFAULT 0,
    locked       INTEGER NOT NULL DEFAULT 0,
    html_url     TEXT,
    created_at   TEXT,
    updated_at   TEXT,
    closed_at    TEXT
);

CREATE TABLE IF NOT EXISTS labels (
    issue_number INTEGER NOT NULL REFERENCES issues(number) ON DELETE CASCADE,
    name         TEXT NOT NULL,
    PRIMARY KEY (issue_number, name)
);

CREATE TABLE IF NOT EXISTS assignees (
    issue_number INTEGER NOT NULL REFERENCES issues(number) ON DELETE CASCADE,
    login        TEXT NOT NULL,
    PRIMARY KEY (issue_number, login)
);

CREATE TABLE IF NOT EXISTS comments (
    id           INTEGER PRIMARY KEY,
    issue_number INTEGER NOT NULL REFERENCES issues(number) ON DELETE CASCADE,
    author       TEXT,
    body         TEXT,
    html_url     TEXT,
    created_at   TEXT,
    updated_at   TEXT
);

CREATE INDEX IF NOT EXISTS idx_issues_state ON issues(state);
CREATE INDEX IF NOT EXISTS idx_labels_name ON labels(name);
CREATE INDEX IF NOT EXISTS idx_comments_issue ON comments(issue_number);
"""


def gh_paginate(path: str) -> list[dict[str, Any]]:
    """Fetch every page of an array endpoint via `gh api`, flattened."""
    cmd = ["gh", "api", "--paginate", "--slurp", path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"gh api failed:\n{proc.stderr.strip()}")
    pages = json.loads(proc.stdout)
    return [item for page in pages for item in page]


def fetch_issues(repo: str, state: str) -> list[dict[str, Any]]:
    """Return every issue (and PR) the issues endpoint reports for the repo."""
    return gh_paginate(f"repos/{repo}/issues?state={state}&per_page=100")


def fetch_comments(repo: str) -> list[dict[str, Any]]:
    """Return all issue/PR comments for the repo in one paginated sweep."""
    return gh_paginate(f"repos/{repo}/issues/comments?per_page=100")


def store(conn: sqlite3.Connection, issues: list[dict[str, Any]], include_prs: bool) -> int:
    count = 0
    for issue in issues:
        is_pull = "pull_request" in issue
        if is_pull and not include_prs:
            continue
        count += 1
        number = issue["number"]
        conn.execute(
            """
            INSERT INTO issues (number, title, state, state_reason, body, author,
                milestone, comments, is_pull, locked, html_url,
                created_at, updated_at, closed_at)
            VALUES (:number, :title, :state, :state_reason, :body, :author,
                :milestone, :comments, :is_pull, :locked, :html_url,
                :created_at, :updated_at, :closed_at)
            ON CONFLICT(number) DO UPDATE SET
                title=excluded.title, state=excluded.state,
                state_reason=excluded.state_reason, body=excluded.body,
                author=excluded.author, milestone=excluded.milestone,
                comments=excluded.comments, is_pull=excluded.is_pull,
                locked=excluded.locked, html_url=excluded.html_url,
                created_at=excluded.created_at, updated_at=excluded.updated_at,
                closed_at=excluded.closed_at
            """,
            {
                "number": number,
                "title": issue.get("title"),
                "state": issue.get("state"),
                "state_reason": issue.get("state_reason"),
                "body": issue.get("body"),
                "author": (issue.get("user") or {}).get("login"),
                "milestone": (issue.get("milestone") or {}).get("title"),
                "comments": issue.get("comments"),
                "is_pull": int(is_pull),
                "locked": int(bool(issue.get("locked"))),
                "html_url": issue.get("html_url"),
                "created_at": issue.get("created_at"),
                "updated_at": issue.get("updated_at"),
                "closed_at": issue.get("closed_at"),
            },
        )
        # Replace child rows so removed labels/assignees don't linger.
        conn.execute("DELETE FROM labels WHERE issue_number = ?", (number,))
        conn.executemany(
            "INSERT OR IGNORE INTO labels (issue_number, name) VALUES (?, ?)",
            [(number, lbl["name"]) for lbl in issue.get("labels", [])],
        )
        conn.execute("DELETE FROM assignees WHERE issue_number = ?", (number,))
        conn.executemany(
            "INSERT OR IGNORE INTO assignees (issue_number, login) VALUES (?, ?)",
            [(number, a["login"]) for a in issue.get("assignees", [])],
        )
    return count


def store_comments(conn: sqlite3.Connection, comments: list[dict[str, Any]]) -> int:
    """Store comments for issues already in the DB; skip orphans (e.g. PRs)."""
    known = {row[0] for row in conn.execute("SELECT number FROM issues")}
    count = 0
    for comment in comments:
        # issue_url ends in .../issues/<number>
        number = int(comment["issue_url"].rsplit("/", 1)[-1])
        if number not in known:
            continue
        count += 1
        conn.execute(
            """
            INSERT INTO comments (id, issue_number, author, body, html_url,
                created_at, updated_at)
            VALUES (:id, :issue_number, :author, :body, :html_url,
                :created_at, :updated_at)
            ON CONFLICT(id) DO UPDATE SET
                author=excluded.author, body=excluded.body,
                html_url=excluded.html_url, created_at=excluded.created_at,
                updated_at=excluded.updated_at
            """,
            {
                "id": comment["id"],
                "issue_number": number,
                "author": (comment.get("user") or {}).get("login"),
                "body": comment.get("body"),
                "html_url": comment.get("html_url"),
                "created_at": comment.get("created_at"),
                "updated_at": comment.get("updated_at"),
            },
        )
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", help="Repository as owner/name, e.g. henryiii/skills")
    parser.add_argument("-d", "--db", default="issues.db", help="SQLite path (default: issues.db)")
    parser.add_argument(
        "-s", "--state", choices=["open", "closed", "all"], default="open",
        help="Which issues to fetch (default: open)",
    )
    parser.add_argument(
        "--include-prs", action="store_true",
        help="Also store pull requests (the issues API returns them too)",
    )
    parser.add_argument(
        "-c", "--comments", action="store_true",
        help="Also fetch and store comment bodies into the comments table",
    )
    parser.add_argument(
        "--schema", action="store_true", help="Print the database schema and exit",
    )
    args = parser.parse_args()

    if args.schema:
        print(SCHEMA.strip())
        return
    if not args.repo:
        parser.error("repo is required (unless --schema is given)")

    issues = fetch_issues(args.repo, args.state)
    conn = sqlite3.connect(args.db)
    try:
        conn.executescript(SCHEMA)
        stored = store(conn, issues, args.include_prs)
        msg = f"Stored {stored} issues from {args.repo} into {args.db}"
        if args.comments:
            stored_comments = store_comments(conn, fetch_comments(args.repo))
            msg += f" ({stored_comments} comments)"
        conn.commit()
    finally:
        conn.close()

    print(msg)


if __name__ == "__main__":
    main()
