#!/bin/bash

# This script sets up a cron job to run bookclub.pi -sync daily at 2:00 AM

# Get the absolute path to the bookclub.pi script
BOOKCLUB_PATH=$(realpath $(dirname $0)/bookclub.pi)

# Log file path
LOG_FILE="/var/log/bookclub_sync.log"

# Cron schedule (daily at 2:00 AM)
CRON_SCHEDULE="0 2 * * *"

# Construct the cron command
CRON_COMMAND="$CRON_SCHEDULE $BOOKCLUB_PATH -sync >> $LOG_FILE 2>&1"

# Check if cron job already exists
if crontab -l | grep -q "$BOOKCLUB_PATH"; then
    echo "Cron job already exists. Updating..."
    # Remove existing cron job
    crontab -l | grep -v "$BOOKCLUB_PATH" | crontab -
else
    echo "Creating new cron job..."
fi

# Add the cron job
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

echo "✅ Cron job set up to run daily at 2:00 AM."
echo "   Logs will be written to: $LOG_FILE"
echo "   You can edit the schedule by modifying this script."
echo "   To view current cron jobs, run: crontab -l"
echo "   To remove the cron job, run: crontab -e and delete the line."
