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
    # Use --no-pager to avoid interactive pager, and capture all output
    cmd = ["git", "-C", str(repo_path), "--no-pager", "log", "--all"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        haystack = result.stdout or ""
        if ignore_case:
            return query.lower() in haystack.lower()
        return query in haystack
    except Exception as e:
        print(f"Error scanning {repo_path}: {e}")
        return False


def find_git_named_dirs(root: Path):
    """Find directories under `root` (only immediate children) whose name contains 'git' (case-insensitive).

    This intentionally looks at the root itself and only its direct subdirectories (e.g. `~/git`, `~/git2`, `~/git-repo`).
    Returns a list of Path objects (resolved), sorted for stable output.
    """
    matches = set()
    try:
        # include the root itself if it matches
        if "git" in root.name.lower():
            matches.add(root.resolve())

        # look only at immediate children of root (so ~/git, ~/git2, etc.)
        try:
            for p in root.iterdir():
                try:
                    if p.is_dir() and "git" in p.name.lower():
                        matches.add(p.resolve())
                except Exception:
                    continue
        except Exception:
            # Could be permission error when listing root; handle gracefully
            pass

    except Exception as e:
        print(f"Error while scanning directories under {root}: {e}")

    return sorted(matches)


def scan_repos(root: Path, query: str, ignore_case: bool = False):
    found, not_found = [], []

    # First, limit search to folders whose name contains 'git'
    git_named_dirs = find_git_named_dirs(root)
    if not git_named_dirs:
        print(f"No directories with 'git' in the name found under {root}")
        return

    # Collect git repositories found inside those directories
    repos = []
    for d in git_named_dirs:
        # find .git directories under this folder
        try:
            for git_dir in d.rglob(".git"):
                try:
                    repo = git_dir.parent.resolve()
                    repos.append(repo)
                except Exception:
                    continue
        except Exception:
            # if permission denied or similar, skip this dir
            continue

        # also include the dir itself if it's a git repo
        if is_git_repo(d):
            repos.append(d.resolve())

    # Deduplicate while preserving order
    seen = set()
    unique_repos = []
    for r in repos:
        if r not in seen:
            seen.add(r)
            unique_repos.append(r)

    if not unique_repos:
        print(f"No git repositories found inside directories matching 'git' under {root}")
        return

    for path in unique_repos:
        matched = search_git_log(path, query, ignore_case)
        if matched:
            print(f"[FOUND] {path}")
            found.append(path)
        else:
            print(f"[---- ] {path}")
            not_found.append(path)

    print("\n==== Summary ====")
    print(f"Matched: {len(found)}")
    for repo in found:
        print(f"  - {repo}")
    print(f"Not matched: {len(not_found)}")


def list_repos(root: Path):
    """List git repositories found under directories whose name contains 'git'."""
    git_named_dirs = find_git_named_dirs(root)
    if not git_named_dirs:
        print(f"No directories with 'git' in the name found under {root}")
        return

    repos = set()
    for d in git_named_dirs:
        try:
            for git_dir in d.rglob(".git"):
                try:
                    repos.add(git_dir.parent.resolve())
                except Exception:
                    continue
        except Exception:
            continue

        if is_git_repo(d):
            repos.add(d.resolve())

    repos_list = sorted(repos)

    print("Projects under:", root)
    if not repos_list:
        print("  (none found inside matching 'git' folders)")
        return
    for repo in repos_list:
        print(f" - {repo}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan git repos for a string in commit logs. This script limits scan to folders whose name contains 'git' under the given root."
    )
    parser.add_argument("-q", "--query", help="String to search in git logs")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    parser.add_argument("-d", "--dir", type=str, default="~", help="Root directory containing repos (defaults to home)")
    parser.add_argument("--list", action="store_true", help="List repos only, no search")

    args = parser.parse_args()
    root = Path(args.dir).expanduser().resolve()
    print(f"Starting search in: {root}")

    if args.list:
        list_repos(root)
    elif args.query:
        scan_repos(root, args.query, args.ignore_case)
    else:
        parser.print_help()

# Examples:
#
# List all repos (only those under directories with 'git' in their name):
# ./git_scan.py --list
#
# Search commit messages for "fix login" (case-insensitive):
# ./git_scan.py -q "fix login" -i
#
# Search in a different root path:
# ./git_scan.py -q "API_KEY" -d /path/to/git/folder
#
# Other example queries:
# $ ~/git/PythonRuns/scripts/git_scan.py -q "user" -i
# $ ~/git/PythonRuns/scripts/git_scan.py -q "@company" -i
