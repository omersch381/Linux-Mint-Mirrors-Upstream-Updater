#!/bin/bash
#
# This is my nearest mirror finder script
#


main(){
    # Handling Log's creation
    create_log
    
    # Running The LinuxMintMirrosFinder.py File:
    run_python_file
    
    # Pinging Each Mirror on the List
    find_the_nearest_mirror "$1"
    
    # Creating a Mirrors Source Backup
    # create_a_source_backup            # It is commented because I don't want it to be backed-up for now
    
    
    # Switching The Existing Source File
    ROW_NUMBER=$(awk '/main upstream import backport/ {print NR}' "$SOURCES_PATH")
}


# Functions

create_a_source_backup(){
    # This function creates a source backup.
    
    # Messages and Variables
    BACKUP_SOURCE_ERROR_MSG="Error! A Source Backup Was Not Created Successfully!"
    BACKUP_SOURCE_SUCCESS_MSG="A Source Backup Was Created Successfully!"
    SOURCES_PATH="/etc/apt/sources.list.d/official-package-repositories.list"
    
    echo "Creating a Mirrors Source Backup..."
    Log "Creating a Mirrors Source Backup..."
    if ! sudo cp "$SOURCES_PATH" "$SOURCES_PATH.bak"; then
        LOG "$BACKUP_SOURCE_ERROR_MSG"
        echo "$BACKUP_SOURCE_ERROR_MSG"
        exit 1
    fi
    Log "$BACKUP_SOURCE_SUCCESS_MSG"
}

find_the_nearest_mirror(){
    # This method pings every mirror on the "mirrors_list" file, and finds the nearest one (by comparing the ping time)
    
    # Variables
    MINIMAL_AVG_TIME=1000 # initial time
    TEMP_LOG_FILE="$DIR_PATH/temp_ping_details"
    
    echo "Start Pinging Mirrors...."
    for current_mirror in $(cat "$DIR_PATH/mirrors_list"); do
        
        # http://<domain>/<path>  ->  <domain>
        CURRENT_MIRROR_DOMAIN_TO_PING=$(echo "$current_mirror" | awk -F/ '{print $3}')
        Log "pinging $CURRENT_MIRROR_DOMAIN_TO_PING...."
        if "$1" == "-v"; then echo "pinging $CURRENT_MIRROR_DOMAIN_TO_PING...."; fi
        
        # if no such mirror -> continue
        if ! ping -w 5 "$CURRENT_MIRROR_DOMAIN_TO_PING" > "$TEMP_LOG_FILE" 2> /dev/null; then continue; fi
        CURRENT_LIST_OF_TIMES=$(awk '/time=/ {print $8}' "$TEMP_LOG_FILE" | sed 's/.*=//')
        CURRENT_AVERAGE=$(echo "$CURRENT_LIST_OF_TIMES" | awk '{sum+=$1} END { print sum/NR }')
        Log "$CURRENT_MIRROR_DOMAIN_TO_PING has an average time of $CURRENT_AVERAGE ms"
        
        # if current is smaller than the minimal
        if (( $(echo "$CURRENT_AVERAGE < $MINIMAL_AVG_TIME" |bc -l) )) && (( $(echo "$CURRENT_AVERAGE > 0" |bc -l) )); then
            MINIMAL_AVG_TIME=$CURRENT_AVERAGE
            NEAREST_MIRROR=$CURRENT_MIRROR_DOMAIN_TO_PING
            Log "$CURRENT_MIRROR_DOMAIN_TO_PING is the current nearest Mirror with an average time of $CURRENT_AVERAGE ms"
        fi
    done
    echo "$NEAREST_MIRROR is the nearest mirror with an AVG of $MINIMAL_AVG_TIME"
    
    # Cleaning Temp Files
    rm "$TEMP_LOG_FILE"
    rm "$DIR_PATH/mirrors_list"
}

create_log(){
    FILE_FULL_PATH=$0
    FILE_BASE_NAME=$(basename -- "$FILE_FULL_PATH")
    DIR_PATH="${FILE_FULL_PATH/$FILE_BASE_NAME/}" # just the file full path without the file_basename
    TIMESTAMP_WITHOUT_HOUR=$(date | awk '{print $1 "_" $2 "_" $3 "_" $6}')
    LOG_NAME="$FILE_BASE_NAME"_"$TIMESTAMP_WITHOUT_HOUR"
    Log_PATH="$DIR_PATH/$LOG_NAME"
    TIMESTAMP_WITH_HOUR=$(date | awk '{print $1 "_" $2 "_" $3 "_" $4 "_" $6}')
    
    # LOG_CREATION=$(echo "$FILE_BASE_NAME Was Run at $TIMESTAMP_WITH_HOUR" > "$Log_PATH") # create the log
    LOG_CREATION_FAILED_MSG="Log's Creation Was Failed!"
    if ! echo "$FILE_BASE_NAME Was Run at $TIMESTAMP_WITH_HOUR" > "$Log_PATH"; then echo "$LOG_CREATION_FAILED_MSG"; fi
}


run_python_file(){
    echo "Finding Recent Mirrors..."
    Log "Finding Recent Mirrors..."
    MIRRORS_FINDER_ERROR_MSG="Error! Could Not Find Mirrors!"
    if ! python3 "$DIR_PATH/LinuxMintMirrosFinder.py"; then echo "$MIRRORS_FINDER_ERROR_MSG"
    else Log "Mirrors Were Found Successfully!"
    fi
}


Log(){
    echo "$1" >> "$Log_PATH"
}

main "$@"; exit
