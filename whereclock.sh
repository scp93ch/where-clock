#!/bin/sh

### BEGIN INIT INFO
# Provides:          whereclock
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: A simple webserver that moves a motor
# Description:       An interpretation of the clock in Weasley house (Harry Potter) that moves to show where members of the family are
### END INIT INFO

DIR=/usr/local/bin/whereclock
DAEMON=$DIR/whereclock.py
DAEMON_USER=root
DAEMON_NAME=whereclock
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile $PIDFILE --user $DAEMON_USER --startas $DAEMON
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" "system-wide $DAEMON_NAME" && exit 0 || exit $?
        ;;
    *)
        echo "Usage: /etc/init.d/$DEAMON_NAME {start|stop|force-stop|restart|status}"
        exit 1
        ;;

esac
exit 0
