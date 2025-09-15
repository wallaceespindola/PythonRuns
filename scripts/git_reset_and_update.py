#!/usr/bin/env python3
import argparse
import subprocess
import shutil
from pathlib import Path
import sys


def run_command(cmd, cwd=None):
    """Run a shell command and return (success, output)."""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def copy_folder(src: Path, dst: Path, exclude=None):
    """Copy folder contents, excluding specified directories."""
    exclude = exclude or set()
    dst.mkdir(exist_ok=True)
    for item in src.iterdir():
        if item.name in exclude:
            continue
        if item.is_dir():
            shutil.copytree(item, dst / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dst)


def remove_all_except(path: Path, exclude=None):
    """Remove all files/folders in path except those in exclude."""
    exclude = exclude or set()
    for item in path.iterdir():
        if item.name in exclude:
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def main(project_folder=None):
    if project_folder is None:
        parser = argparse.ArgumentParser(description="Reset git repo to initial commit and update files.")
        parser.add_argument("project", help="Project folder name")
        args = parser.parse_args()
        project_folder = args.project

    root = Path.home() / "git"
    proj = root / project_folder
    backup = root / f"{project_folder}-copy"
    exclude = {'.git', '.idea'}

    if not proj.exists() or not proj.is_dir():
        print(f"Project folder '{project_folder}' not found.")
        sys.exit(1)
    if not (proj / '.git').exists():
        print(f"'{project_folder}' is not a git repository.")
        sys.exit(1)

    print(f"1. Duplicating folder to: {backup}")
    shutil.copytree(proj, backup, dirs_exist_ok=True)

    print("2. Resetting to initial commit...")
    ok, log = run_command(["git", "log", "--reverse", "--oneline"], cwd=proj)
    if not ok or not log.strip():
        print("Could not get git log.")
        shutil.rmtree(backup)
        sys.exit(1)
    first_commit = log.strip().split('\n')[0].split()[0]
    ok, out = run_command(["git", "reset", "--hard", first_commit], cwd=proj)
    if not ok:
        print(f"Git reset failed: {out}")
        shutil.rmtree(backup)
        sys.exit(1)

    print("3. Setting git user email...")
    ok, out = run_command(["git", "config", "user.email", "wallace.espindola@gmail.com"], cwd=proj)
    if not ok:
        print(f"Git config failed: {out}")
        shutil.rmtree(backup)
        sys.exit(1)

    print("4. Copying files from backup (excluding .git/.idea)...")
    remove_all_except(proj, exclude)
    copy_folder(backup, proj, exclude)

    print("5. Committing files...")
    ok, out = run_command(["git", "add", "."], cwd=proj)
    if not ok:
        print(f"Git add failed: {out}")
        shutil.rmtree(backup)
        sys.exit(1)
    ok, out = run_command(["git", "commit", "-m", "updating configs"], cwd=proj)
    if not ok and "nothing to commit" not in out:
        print(f"Git commit failed: {out}")
        shutil.rmtree(backup)
        sys.exit(1)

    print("6. Pushing...")
    ok, out = run_command(["git", "push", "--force"], cwd=proj)
    if not ok:
        print(f"Git push failed: {out}")
        shutil.rmtree(backup)
        sys.exit(1)

    print("7. Deleting backup folder...")
    shutil.rmtree(backup)

    print("8. Final status:")
    ok, out = run_command(["git", "status"], cwd=proj)
    print(out)
    ok, out = run_command(["git", "log", "--oneline", "-5"], cwd=proj)
    print("Recent commits:")
    print(out)
    print(f"\n✅ Done for '{project_folder}'")


if __name__ == "__main__":
    main("fast-api-test")
    # main()
