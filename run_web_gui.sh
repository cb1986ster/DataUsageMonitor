#!/bin/bash

WORK_DIR=/opt/DataUsageMonitor

source ${WORK_DIR}/venv/bin/activate

${WORK_DIR}/manage.py runserver
