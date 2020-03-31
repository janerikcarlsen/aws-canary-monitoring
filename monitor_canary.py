#!/bin/python

import os
import time
import boto3

# Get environment variables from action input:
MONITORING_TIME = int(os.getenv("INPUT_MONITORING-TIME"))
ALARM_NAME = os.getenv("INPUT_ALARM-NAME")

client = boto3.client("cloudwatch")

now = time.time()
timeout = now + MONITORING_TIME*60000

while time.time() < timeout:
    alarms = client.describe_alarms(
        AlarmNames=[ALARM_NAME],
        AlarmTypes=["CompositeAlarm", "MetricAlarm"],
        StateValue="ALARM"
    )
    if not alarms: 
        time.sleep(5)
    else: 
        print("Canary Alarm in ALARM state")
        print("Aborting with exit code 1")
        exit(1)