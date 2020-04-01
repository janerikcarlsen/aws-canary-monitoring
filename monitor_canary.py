#!/bin/python

import os
import time
import sys
import logging
import boto3

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("aws-canary-monitoring")

MONITORING_TIME = int(os.getenv("INPUT_MONITORING-TIME"))
ALARM_NAME = os.getenv("INPUT_ALARM-NAME")
POLLING_INTERVAL = int(os.getenv("INPUT_POLLING-INTERVAL"))

client = boto3.client("cloudwatch")

now = time.time()
timeout = now + MONITORING_TIME*60

log.info(f"Starting AWS Canary Monitoring with duration: {MONITORING_TIME} minutes, polling interval: {POLLING_INTERVAL} seconds")
while time.time() < timeout:
    alarms = client.describe_alarms(
        AlarmNames=[ALARM_NAME],
        AlarmTypes=["CompositeAlarm", "MetricAlarm"],
        StateValue="ALARM"
    )
    if not (alarms["CompositeAlarms"] or alarms["MetricAlarms"]) : 
        log.info(f"Monitoring returned no alarms in ALARM state, polling again in {POLLING_INTERVAL} seconds")
        time.sleep(POLLING_INTERVAL)
    else: 
        log.warning(f"CompositeAlarms: {alarms['CompositeAlarms']}")
        log.warning(f"MetricAlarms: {alarms['MetricAlarms']}")
        log.error("Cloudwatch Canary Alarm in ALARM state")
        log.error("Aborting with exit code 1")
        exit(1)