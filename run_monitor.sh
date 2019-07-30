#!/bin/bash

WORK_DIR=/opt/DataUsageMonitor

source ${WORK_DIR}/venv/bin/activate

start-stop-daemon --start -b -m --pidfile /var/run/data_usage_monitor.pid --exec ${WORK_DIR}/manage.py runscript monitor
