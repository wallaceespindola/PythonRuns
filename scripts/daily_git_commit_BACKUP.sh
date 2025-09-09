#!/bin/bash

# Set variables
REPO_DIR="/home/my_user/git/my-runs"
COMMIT_MESSAGE="Updated documentation on $(date '+%Y-%m-%d')"

# Navigate to the repository directory
cd "$REPO_DIR" || {
    echo "Repository directory not found!"
    exit 1
}

# Ensure we're on the correct branch (e.g., main)
git checkout main

# Add all changes
git add .

# Force commit changes without checking for modifications
git commit --allow-empty -m "$COMMIT_MESSAGE"

# Push to GitHub
git push origin main

echo "Changes committed and pushed successfully on $(date)."

# Now add to crontab for 8AM commit: 0 8 * * * /bin/bash ~/scripts/daily_git_commit.sh >> ~/scripts/daily_git_commit.log 2>&1
