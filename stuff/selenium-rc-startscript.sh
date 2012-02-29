#!/bin/bash
#
# selenium-rc-startscript
#
# 

if [ -z "$1" ]; then
    echo "`basename $0` {start|stop}"
    exit 2
fi

case "$1" in
    start)
    /usr/bin/Xvfb :99 -ac -screen 0 1024x768x8 &
    ;;

stop)
    killall Xvfb
    ;;
esac

