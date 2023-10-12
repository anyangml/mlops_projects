# TODO

A regression problem need to be retrained every time new batch data is available.
- training workflow orchestrated by prefect.
- training monitered by mlfolw.
- model registery based on s3.
- model inference served with aws api gateway & lambda.
- circleci to manage integration/prod deployment.
- monitering with grafana.


# References
- [prepare lambda deployment package](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [zip too large for lambda](https://medium.com/geekculture/deploying-a-sklearn-model-on-aws-lambda-b649ce58bac2#:~:text=If%20the%20file%20is%20larger,cannot%20be%20used%20in%20Lambda.)