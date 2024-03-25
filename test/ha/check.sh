#!/bin/bash
grep ".py Updated " /var/log/fswatch.log
[ $? = 0 ] && {
    exit 1
}
echo "No change" 1>&2
exit 0
