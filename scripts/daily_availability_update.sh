#!/bin/bash
# Daily summer camp availability update
# Pulls registration data from FormBuilder API, updates website, commits, and pushes.
# Cron: 0 7 * * * /Users/vishal/code/makerlab/scripts/daily_availability_update.sh >> /tmp/makerlab-availability.log 2>&1

set -e

export PATH="/opt/homebrew/bin:$PATH"
cd /Users/vishal/code/makerlab

echo "=== $(date) ==="

# Pull latest
git pull --ff-only origin main

# Run availability update
python3 scripts/update_availability.py

# Check if anything changed
if git diff --quiet summer.html summer/*.html; then
    echo "No availability changes detected."
    exit 0
fi

# Commit and push
git add summer.html summer/*.html
git commit -m "Update camp availability ($(date +%Y-%m-%d))"
git push origin main

echo "Availability updated and deployed."
