#!/bin/bash
# Daily camp availability updater — runs via launchd at 9 AM CDT
# Updates summer camp spot counts from FormBuilder API, commits + pushes if changed.
# Log: /tmp/makerlab-availability.log

set -euo pipefail

REPO="/Users/vishal/code/makerlab"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
LOG="/tmp/makerlab-availability.log"

export SSL_CERT_FILE="/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/certifi/cacert.pem"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

echo "=== $(date) ===" >> "$LOG"

cd "$REPO"

# Fetch latest to avoid conflicts
git pull --ff-only >> "$LOG" 2>&1 || { echo "git pull failed" >> "$LOG"; exit 1; }

# Run the update script
$PYTHON scripts/update_availability.py >> "$LOG" 2>&1

# Check if anything changed
if git diff --quiet; then
    echo "No changes detected" >> "$LOG"
else
    git add summer.html summer/*.html data/session-availability.json data/registrations-snapshot.json
    git commit -m "Update camp availability ($(date +%Y-%m-%d))" >> "$LOG" 2>&1
    git push >> "$LOG" 2>&1
    echo "Committed and pushed" >> "$LOG"
fi

echo "Done" >> "$LOG"
echo "" >> "$LOG"
