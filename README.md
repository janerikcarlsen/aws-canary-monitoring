# aws-canary-monitoring
GitHub Action for monitoring an AWS Cloudwatch alarm and erroring if the Canary alarm enters an ALARM state

# Usage
The action is used like this:

```
  - name: AWS Canary Monitoring
    uses: janerikcarlsen/aws-canary-monitoring@master
    with:
      alarm-name: your-service-canary-alarm-name
```

In a workflow, you can use the action typically after a deployment to conditionally trigger a rollback step or other compensating action:

```
steps:
  - name: <Your deployment step>
    uses: <Your deployment action>
  - name: AWS Canary Monitoring
    uses: janerikcarlsen/aws-canary-monitoring@master
    with:
      alarm-name: your-service-canary-alarm-name
  - name: Your rollback step
    if: failure()
    uses: <Your rollback action>
```