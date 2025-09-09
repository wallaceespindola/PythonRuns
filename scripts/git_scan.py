#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def is_git_repo(path: Path) -> bool:
    """Check if a folder is a git repository."""
    return (path / ".git").exists()


def search_git_log(repo_path: Path, query: str, ignore_case: bool = False) -> bool:
    """Search git log output for a query string, similar to `git log | grep -i <query>`.

    This matches anywhere in the raw `git log` text (authors, dates, subjects, bodies, etc.).
    Returns True if a match is found.
    """
    cmd = ["git", "-C", str(repo_path), "log", "--all"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        haystack = result.stdout or ""
        if ignore_case:
            return query.lower() in haystack.lower()
        return query in haystack
    except Exception as e:
        print(f"Error scanning {repo_path}: {e}")
        return False


def scan_repos(root: Path, query: str, ignore_case: bool = False):
    found, not_found = [], []

    for path in root.iterdir():
        if path.is_dir() and is_git_repo(path):
            matched = search_git_log(path, query, ignore_case)
            if matched:
                print(f"[FOUND] {path.name}")
                found.append(path.name)
            else:
                print(f"[---- ] {path.name}")
                not_found.append(path.name)

    print("\n==== Summary ====")
    print(f"Matched: {len(found)}")
    for repo in found:
        print(f"  - {repo}")
    print(f"Not matched: {len(not_found)}")


def list_repos(root: Path):
    repos = [p.name for p in root.iterdir() if p.is_dir() and is_git_repo(p)]
    print("Projects under:", root)
    for repo in repos:
        print(f" - {repo}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan git repos for a string in commit logs.")
    parser.add_argument("-q", "--query", help="String to search in git logs")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    parser.add_argument("-d", "--dir", type=str, default=".", help="Root directory containing repos")
    parser.add_argument("--list", action="store_true", help="List repos only, no search")

    args = parser.parse_args()
    root = Path(args.dir).resolve()

    if args.list:
        list_repos(root)
    elif args.query:
        scan_repos(root, args.query, args.ignore_case)
    else:
        parser.print_help()

# Examples:
#
# List all repos:
#
# ./git_scan.py --list
#
#
# Search commit messages for "fix login" (case-insensitive):
#
# ./git_scan.py -q "fix login" -i
#
#
# Search in a different root path:
#
# ./git_scan.py -q "API_KEY" -d /path/to/git/folder
