#!/bin/python

import os
import time
import sys
import logging
import boto3

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("aws-canary-monitoring")
# Get environment variables from action input:
MONITORING_TIME = int(os.getenv("INPUT_MONITORING-TIME"))
#MONITORING_TIME = 2
ALARM_NAME = os.getenv("INPUT_ALARM-NAME")
#ALARM_NAME = "Synthetics-Alarm-my-canary-monitor"
POLLING_INTERVAL = int(os.getenv("INPUT_POLLING-INTERVAL"))
#POLLING_INTERVAL = 10

if not MONITORING_TIME:
    log.error("No monitoring time set, aborting")
    exit(2)

if not ALARM_NAME:
    log.error("No alarm name set, aborting")
    exit(2)

client = boto3.client("cloudwatch")

now = time.time()
timeout = now + MONITORING_TIME*60

log.info(f"Starting Canary Monitoring with duration: {MONITORING_TIME} minutes, polling interval: {POLLING_INTERVAL} seconds")
while time.time() < timeout:
    alarms = client.describe_alarms(
        AlarmNames=[ALARM_NAME],
        AlarmTypes=["CompositeAlarm", "MetricAlarm"],
        StateValue="ALARM"
    )
    if not (alarms["CompositeAlarms"] or alarms["MetricAlarms"]) : 
        log.info(f"Cloudwatch returned no alarms in ALARM state, polling again in {POLLING_INTERVAL} seconds")
        time.sleep(POLLING_INTERVAL)
    else: 
        log.warning(f"CompositeAlarms: {alarms['CompositeAlarms']}")
        log.warning(f"MetricAlarms: {alarms['MetricAlarms']}")
        log.error("Cloudwatch Canary Alarm in ALARM state")
        log.error("Aborting with exit code 1")
        exit(1)