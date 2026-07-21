#!/usr/bin/env python3
"""Print an issue's body and comments from a SQLite DB built by
github-issues-to-sqlite.py."""

import argparse
import sqlite3
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int, help="Issue number to show")
    parser.add_argument("-d", "--db", default="issues.db", help="SQLite path (default: issues.db)")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    try:
        issue = conn.execute(
            "SELECT * FROM issues WHERE number = ?", (args.number,)
        ).fetchone()
        if issue is None:
            sys.exit(f"Issue #{args.number} not found in {args.db}")

        kind = "PR" if issue["is_pull"] else "Issue"
        print(f"{kind} #{issue['number']}: {issue['title']}")
        meta = f"{issue['state']} | by {issue['author']} | {issue['created_at']}"
        if issue["closed_at"]:
            meta += f" | closed {issue['closed_at']}"
        print(meta)

        labels = [r[0] for r in conn.execute(
            "SELECT name FROM labels WHERE issue_number = ? ORDER BY name", (args.number,)
        )]
        if labels:
            print(f"labels: {', '.join(labels)}")
        print(f"{issue['html_url']}\n")

        print(issue["body"] or "(no body)")

        comments = conn.execute(
            "SELECT author, body, created_at FROM comments "
            "WHERE issue_number = ? ORDER BY created_at",
            (args.number,),
        ).fetchall()
        for c in comments:
            print(f"\n{'-' * 60}")
            print(f"@{c['author']} — {c['created_at']}\n")
            print(c["body"] or "(empty)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
