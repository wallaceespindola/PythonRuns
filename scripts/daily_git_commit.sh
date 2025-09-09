#!/bin/bash
set -e

# Minimal env for cron
export HOME="/home/aiyrh"
export PATH="/usr/local/bin:/usr/bin:/bin"

# Choose repo by weekday (1=Mon ... 7=Sun)
case "$(date +%u)" in
  1) REPO="$HOME/git/fast-api-test" ;;                      # Mon
  2) REPO="$HOME/git/PythonRuns" ;;                         # Tue
  3) REPO="$HOME/git/flashcards-app" ;;                     # Wed
  4) REPO="$HOME/git/investment-portfolio-python" ;;        # Thu
  5) REPO="$HOME/git/workflow-kafka-process-file-output" ;; # Fri
  6) REPO="$HOME/git/spring-kafka-batch-demo" ;;            # Sat
  7) REPO="$HOME/git/python-flask-app" ;;                   # Sun
  *) echo "Unknown weekday"; exit 2 ;;
esac

cd "$REPO" || { echo "Repo not found: $REPO"; exit 1; }
[ -d .git ] || { echo "Not a git repo: $REPO"; exit 1; }

# Apply identity ONLY for the selected repo (change path if you want a different one)
if [[ "$REPO" == "$HOME/git/fast-api-test" ]]; then
  git config --local user.name  "Wallace Espindola"
  git config --local user.email "wallace.espindola@gmail.com"
fi

# Use currently checked-out branch
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
MSG="Small fix"

git fetch --all --prune
git pull --rebase --autostash
git add -A
git commit --allow-empty -m "$MSG"
git push origin "$BRANCH"

echo "[$(date)] Commit and push in $REPO on branch $BRANCH."

