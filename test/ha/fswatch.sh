#!/bin/bash

> /var/log/fswatch.log
fswatch --event-flags --recursive /config/custom_components/yro_hassio_beem | grep '\.py Updated'
