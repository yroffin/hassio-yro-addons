#!/usr/bin/with-contenv bashio

bashio::log.green "Preparing to start ..."

# Set files to be used
export LOG_FILE="$(bashio::config 'log_file')"

# Delete previous session log
rm -f $LOG_FILE

bashio::log.green "Starting hassio beem box ..."
