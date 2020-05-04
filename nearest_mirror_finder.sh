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
    find_the_nearest_mirror
    
    # Creating a Mirrors Source Backup
    create_a_source_backup
    
    # Switching The Existing Source File
    switch_it
    
    # Making sure everything is ok - if not it will be reverted
    revert_if_update_is_not_ok
    
    # If everything works - we will delclare it to the user! (if something was wrong
    # by now, the method would have exited in each critical step before).
    echo "Mirror is now the nearest!! (Whether if it was changed or not)"
}


# Functions

create_log(){
    # This method handles all Log's creation.
    
    # variables
    FILE_FULL_PATH=$0
    FILE_BASE_NAME=$(basename -- "$FILE_FULL_PATH")
    DIR_PATH="${FILE_FULL_PATH/$FILE_BASE_NAME/}" # just the file full path without the file_basename
    TIMESTAMP_WITHOUT_HOUR=$(date | awk '{print $1 "_" $2 "_" $3 "_" $6}')
    TIMESTAMP_WITH_HOUR=$(date | awk '{print $1 "_" $2 "_" $3 "_" $4 "_" $6}')
    LOG_NAME="$FILE_BASE_NAME"_"$TIMESTAMP_WITHOUT_HOUR"
    LOG_PATH="$DIR_PATH/$LOG_NAME"
    
    # Creates the Log
    LOG_CREATION_FAILED_MSG="Log's Creation Was Failed!"
    if ! echo "$FILE_BASE_NAME Was Run at $TIMESTAMP_WITH_HOUR" > "$LOG_PATH"; then echo "$LOG_CREATION_FAILED_MSG"; fi
}

run_python_file(){
    # This method runs the python file - it will save to a file the recent mirrors list
    
    # Variables
    MIRRORS_FINDER_ERROR_MSG="Error! Could Not Find Mirrors!"
    MIRRORS_FINDER_SUCCES_MSG="Mirrors Were Found Successfully!"
    PYTHON_FILE_PATH="$DIR_PATH/LinuxMintMirrosFinder.py"
    
    echo "Finding Recent Mirrors..."
    Log "Finding Recent Mirrors..."
    if ! python3 "$PYTHON_FILE_PATH"; then echo "$MIRRORS_FINDER_ERROR_MSG"
    else Log "$MIRRORS_FINDER_SUCCES_MSG"
    fi
}

find_the_nearest_mirror(){
    # This method pings every mirror on the "mirrors_list" file, and finds the nearest one (by comparing the ping time)
    
    # Variables
    MINIMAL_AVG_TIME=1000 # initial time
    TEMP_LOG_FILE="$DIR_PATH/temp_ping_details"
    
    echo "Start Pinging Mirrors...."
    for current_mirror in $(cat "$DIR_PATH/mirrors_list"); do
        
        # http://<domain>/<path>  -->  <domain>
        CURRENT_MIRROR_DOMAIN_TO_PING=$(echo "$current_mirror" | awk -F/ '{print $3}')
        Log "pinging $CURRENT_MIRROR_DOMAIN_TO_PING...."
        echo "pinging $CURRENT_MIRROR_DOMAIN_TO_PING...."
        
        # if no such mirror -> continue
        if ! ping -w 5 "$CURRENT_MIRROR_DOMAIN_TO_PING" > "$TEMP_LOG_FILE" 2> /dev/null; then continue; fi
        CURRENT_LIST_OF_TIMES=$(awk '/time=/ {print $8}' "$TEMP_LOG_FILE" | sed 's/.*=//')
        CURRENT_AVERAGE=$(echo "$CURRENT_LIST_OF_TIMES" | awk '{sum+=$1} END { print sum/NR }')
        Log "$CURRENT_MIRROR_DOMAIN_TO_PING has an average time of $CURRENT_AVERAGE ms"
        
        # if current is smaller than the minimal
        if (( $(echo "$CURRENT_AVERAGE < $MINIMAL_AVG_TIME" |bc -l) )) && (( $(echo "$CURRENT_AVERAGE > 0" |bc -l) )); then
            MINIMAL_AVG_TIME=$CURRENT_AVERAGE
            NEAREST_MIRROR=$CURRENT_MIRROR_DOMAIN_TO_PING
            NEAREST_MIRROR_FULL_PATH=$current_mirror
            Log "$CURRENT_MIRROR_DOMAIN_TO_PING is the current nearest Mirror with an average time of $CURRENT_AVERAGE ms"
        fi
    done
    echo "$NEAREST_MIRROR is the nearest mirror with an AVG of $MINIMAL_AVG_TIME"
    
    # Cleaning Temp Files
    rm "$TEMP_LOG_FILE"
    rm "$DIR_PATH/mirrors_list"
}

create_a_source_backup(){
    # This function creates a source backup.
    
    # Messages and Variables
    BACKUP_SOURCE_ERROR_MSG="Error! A Source Backup Was Not Created Successfully!"
    BACKUP_SOURCE_SUCCESS_MSG="A Source Backup Was Created Successfully!"
    SOURCES_PATH="/etc/apt/sources.list.d/official-package-repositories.list"
    
    # Handle the backup
    echo "Creating a Mirrors Source Backup..."
    Log "Creating a Mirrors Source Backup..."
    if ! cp "$SOURCES_PATH" "$SOURCES_PATH.bak"; then
        LOG "$BACKUP_SOURCE_ERROR_MSG"
        echo "$BACKUP_SOURCE_ERROR_MSG"
        exit 1
    fi
    Log "$BACKUP_SOURCE_SUCCESS_MSG"
}

switch_it(){
    # This method switches the mirror's url, and if it is not successful - it reverts it.
    
    # Variables
    SOURCES_PATH="/etc/apt/sources.list.d/official-package-repositories.list"
    CHANGED_SUCCESSFULLY_MSG="Mirror Was Changed Succesfully!"
    CHANGED_FAILED_MSG="Mirror Was NOT Changed!! Reverting The Sources File..."
    
    # Creates a new line with the new mirror's URL
    NEW_UPDATED_MIRROR_LINE=$(awk -v nearest="$NEAREST_MIRROR_FULL_PATH" '/main upstream import backport/ { $2 = nearest;printf("%s\n", $0)}' $SOURCES_PATH)
    
    # Saves the changes to a file
    sed "1 s~.*~${NEW_UPDATED_MIRROR_LINE}~" "$SOURCES_PATH" > temp_file
    FIRST_COMMAND="$?"
    mv temp_file "$SOURCES_PATH" # Changes the original file
    SECOND_COMMAND="$?"
    
    if (( ! "$FIRST_COMMAND" + "$SECOND_COMMAND" == 0)); then
        echo "$CHANGED_FAILED_MSG"
        Log "From switch_it method: $CHANGED_FAILED_MSG"
        mv "$SOURCES_PATH.bak" "$SOURCES_PATH"
        exit 1
    else
        echo "$CHANGED_SUCCESSFULLY_MSG"
        Log "From switch_it method $CHANGED_SUCCESSFULLY_MSG"
    fi
}

revert_if_update_is_not_ok(){
    # This method checks that an update is ok to be made - if not it reverts it.
    if ! apt update -y && apt upgrade -y > "$LOG_PATH" 2>&1; then
        echo "$CHANGED_FAILED_MSG"
        Log "From revert_if_not_ok method: $CHANGED_FAILED_MSG"
        mv "$SOURCES_PATH.bak" "$SOURCES_PATH"
        exit 1
    else
        Log "From revert_if_not_ok method: $CHANGED_SUCCESSFULLY_MSG"
    fi
}

Log(){
    echo "$1" >> "$LOG_PATH"
}

main "$@"; exit
