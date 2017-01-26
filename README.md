# AWS IoT Button lap counter

simple example of using the IoT button to record lap counts over wifi to the cloud, and a dashboard to render the lap info via a single page application.

Uses the following AWS services / components:

- AWS IoT Button - each click sends a "lap" to AWS
- DynamoDB button - maintains counter of laps
- S3 - hosts single page application dashboard
- Lambda - two functions; one receives event from IoT Button and updates the DynamoDB table, and the other backs the API and returns data from DynamoDB
- API Gateway - presents lap count programatically

## User guide (to be completed later)

- get your IoT Button set up using the AWS IoT Button Getting Started walkthrough
- to get more familiar, try the walkthrough demo to send emails on button press events (but make sure to disable the trigger of that lambda function so you don't continue to get emails in the future)
- provision your CloudFormation stack with template.yml, providing your button DSN as a parameter
- update the "myUrl" variable in index.html to point to the URL of your API. This can be found in the API gateway console -> API name -> Stages -> Prod -> Invoke URL. Overwrite the existing myUrl value with this value.
- upload index.html and favicon.ico to the S3 bucket that gets created, enabling public permissions to those files and enabling static website hosting for the bucket, and pointing to index.html
- to enable your lap counter app to respond to button clicks, in the Lambda console you need to define the AWS IoT Button as the trigger for the ButtonPressFunction. Select "AWS IoT" as the integration, "IoT type" as "IoT Button", and include your button's DSN and click "Submit".
- Give it a try! A single button click will increment the counter. A double-click will reset the lap counter.
