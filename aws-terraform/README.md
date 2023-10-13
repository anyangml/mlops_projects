# MLops Demo

A regression problem need to be retrained every time new batch data is available.

- Everytime a new batch of data is uploaded to the S3 bucket, a Lambda function is triggered.
- The Lambda function sends a command to trigger a git action workflow (can also use circleci).
- The workflow is orchestrated by prefect:
  - Download the data from S3
  - Validate the data
  - Train a regression model and dockerize the model
- The workflow then deploy the model with aws api gateway & lambda
- monitering with grafana.


# References
- [prepare lambda deployment package](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [zip too large for lambda](https://medium.com/geekculture/deploying-a-sklearn-model-on-aws-lambda-b649ce58bac2#:~:text=If%20the%20file%20is%20larger,cannot%20be%20used%20in%20Lambda.)