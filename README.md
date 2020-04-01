# aws-canary-monitoring
GitHub Action for monitoring an AWS Cloudwatch alarm and erroring if the alarm enters an ALARM state



This GitHub Action lets you monitor a Canary by polling the state of a Cloudwatch alarm. Canaries can be set up using the Cloudwatch Synthetics feature that is currently in preview. Read more about Cloudwatch Synthetics here: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html

This action is intended to be run following a deployment. 
 
If the specified CloudWatch alarm enters an ALARM state during the provided monitoring time, the action will return with an exit code 1. 
You can then use the `failure()` conditional in the following step to perform a rollback or compensating action.

The action assumes that AWS credentials is configured and available in environment variables by a previous step in the workflow. 

# Example Usage
The action can be used like this:

```
  - name: AWS Canary Monitoring
    uses: janerikcarlsen/aws-canary-monitoring@v1
    with:
      alarm-name: your-service-canary-alarm-name
```

You can specify a custom monitoring time in minutes (default 5 minutes), and a polling interval in seconds (default 10 seconds):

```
  - name: AWS Canary Monitoring
    uses: janerikcarlsen/aws-canary-monitoring@v1
    with:
      alarm-name: Synthetics-Alarm-my-canary-monitor
      monitoring-time: 5
      polling-interval: 15
```

In a workflow, you can use the action typically after a deployment to conditionally trigger a rollback step or other compensating action:

```
steps:
  - name: <Your deployment step>
    uses: <Your deployment action>
  - name: AWS Canary Monitoring
    uses: janerikcarlsen/aws-canary-monitoring@v1
    with:
      alarm-name: your-service-canary-alarm-name
  - name: Your rollback step
    if: failure()
    uses: <Your rollback action>
```