#!/usr/bin/with-contenv bashio

bashio::log.green "Preparing to start ..."

# Delete previous session log
rm -f $LOG_FILE

bashio::log.green "Starting hassio beem box ..."
