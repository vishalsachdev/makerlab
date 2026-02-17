#!/bin/bash
# One-shot script: creates the Podio task then removes itself from cron
cd /Users/vishal/code/makerlab/scripts/podio
/opt/homebrew/bin/python3 create_chambanamoms_task.py >> /tmp/chambanamoms_task.log 2>&1

# Remove this job from crontab
crontab -l 2>/dev/null | grep -v "run_chambanamoms_task" | crontab -

echo "$(date): Cron job complete, self-removed." >> /tmp/chambanamoms_task.log
