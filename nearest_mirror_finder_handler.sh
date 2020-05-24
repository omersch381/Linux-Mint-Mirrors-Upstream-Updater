#!/bin/bash
#
# This script handles the maintenance around the nearest_mirror_finder script.
# This is the script that the crontab runs daily.


# Variables
FILE_BASE_NAME=$(basename -- "$0")
TIMESTAMP_WITHOUT_HOUR=$(date | awk '{print $1 "_" $2 "_" $3 "_" $6}')
LOG_NAME="$FILE_BASE_NAME"_"$TIMESTAMP_WITHOUT_HOUR"
DIR_PATH="$(dirname "$(realpath "$0")")"
LOG_PATH="$DIR_PATH/$LOG_NAME"

# Deleting the last run's logs
sudo find "$DIR_PATH" -name "near*20*"  -exec rm "{}" \;

# Running the script
sudo bash "$DIR_PATH/nearest_mirror_finder.sh"

RECENT_LOG=$(ls "$DIR_PATH" | grep '20' )
HAS_ANYTHING_FAILED="$(awk '/Failed/ {print $0}' "$DIR_PATH/$RECENT_LOG")"
if [[ -n "$HAS_ANYTHING_FAILED" ]]; then cp "$LOG_PATH" /home/omer/Desktop/ERROR_IN_LAST_MIRRROR_RUN; fi