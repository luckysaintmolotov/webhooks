#!/bin/bash

APP_SCRIPT="webhook_server.py"
APP_PID="webhook_server.pid"
FUNNEL_PID="funnel.pid"

start() {
    nohup .venv/bin/python $APP_SCRIPT > webhook_server.log 2>&1 &
    echo $! > $APP_PID

    sudo tailscale up
    nohup sudo tailscale funnel 5000 > funnel.log 2>&1 &
    echo $! > $FUNNEL_PID

    echo "Both services started"
}

stop() {
    if [ -f $APP_PID ]; then
        kill $(cat $APP_PID) && rm $APP_PID
    fi
    if [ -f $FUNNEL_PID ]; then
        sudo kill $(cat $FUNNEL_PID) && rm $FUNNEL_PID
    fi
    echo "Both services stopped"
}

restart() {
    stop
    start
    echo "Both services restarted"
}

status() {
    if [ -f $APP_PID ] && ps -p $(cat $APP_PID) > /dev/null 2>&1; then
        echo "Webhook Server is running (PID $(cat $APP_PID))"
    else
        echo "Webhook Server is NOT running"
    fi

    if [ -f $FUNNEL_PID ] && ps -p $(cat $FUNNEL_PID) > /dev/null 2>&1; then
        echo "Tailscale funnel is running (PID $(cat $FUNNEL_PID))"
    else
        echo "Tailscale funnel is NOT running"
    fi
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    status) status ;;
    *) echo "Usage: $0 {start|stop|restart|status}" ;;
esac
