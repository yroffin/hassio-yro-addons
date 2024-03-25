#!/bin/bash

echo starting ...
supervisord &

mkdir -p /config && cp /tmp/config/*.yaml /config
ls -lrt /config

exec /init
