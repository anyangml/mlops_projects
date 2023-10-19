# MLops Demo

A regression problem need to be retrained every time new batch data is available.

- Everytime a new batch of data is uploaded to the S3 bucket, a Lambda function is triggered.
- The Lambda function sends a command to trigger a git action workflow (can also use circleci).
- The workflow is orchestrated by prefect:
  - Download the data from S3
  - Validate the data
  - Train a regression model and upload to S3
  - Build lambda function to serve inference and build with docker
- The workflow then deploy the model with aws api gateway & lambda
- monitering with grafana.

### To Do
- add inference lambda handler to pull model and inference
- add api gateway endpoint to handle inference lambda

# References
- [prepare lambda deployment package](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [zip too large for lambda](https://medium.com/geekculture/deploying-a-sklearn-model-on-aws-lambda-b649ce58bac2#:~:text=If%20the%20file%20is%20larger,cannot%20be%20used%20in%20Lambda.)
- [pull model from s3](https://stackoverflow.com/questions/43372919/reuse-a-scikit-learn-model-pkl-in-aws-lambda)
- [api gateway with lambda](https://stackoverflow.com/questions/76023874/terraform-with-containerized-lambda-function-and-api-gateway)
- [with ECR docker](https://www.bogotobogo.com/DevOps/AWS/aws-API-Gateway-Lambda-Terraform-with-ECR-Container.php)
- [lambda image not updating](https://stackoverflow.com/questions/74537322/terraform-aws-lambda-with-image-not-updating)