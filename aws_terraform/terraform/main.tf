terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "5.6.2"
    }
  }
}

######################
#  Create S3 Bucket  #
######################

resource "aws_s3_bucket" "my_bucket" {
  bucket = "anyang-mlops"
  tags   = {
    Name        = "MLOps"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.my_bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}


######################
#  Create IAM Role   #
######################

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role" "predict_lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

######################
#    Attach policy   #
######################

resource "aws_iam_policy" "s3_policy" {
  name        = "s3_policy"
  description = "Policy for S3 access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:GetObject", "s3:PutObject"]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.my_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  policy_arn = aws_iam_policy.s3_policy.arn
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_policy" "ecr_policy" {
  name = "ecr_policy"
  description = "Policy for ECR access"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "ECRPermissions",
        "Effect" : "Allow",
        "Action" : [
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage"
        ],
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment" {
  policy_arn = aws_iam_policy.ecr_policy.arn
  role       = aws_iam_role.predict_lambda_role.name
}

########################
#      Create ECR      #
########################

resource "aws_ecr_repository" "aws_repo" {
  name = "aws_terraform"
}

# Build docker images and push to ECR
resource "docker_image" "my-docker-image" {
  name = "${aws_ecr_repository.aws_repo.repository_url}:latest"
  build {
    context    = ".."
    dockerfile = "Dockerfile"
  }
}


resource "docker_registry_image" "aws_repo" {
  name = "${aws_ecr_repository.aws_repo.repository_url}:latest"
}


########################
#  Create lambda func  #
########################

resource "aws_lambda_function" "my_lambda_function" {
  filename         = "lambda.zip"
  function_name    = "aws_terraform_model_training"
  runtime          = "python3.8"
  handler          = "lambda_trigger.lambda_handler"
  role             = aws_iam_role.lambda_role.arn
}

resource "aws_lambda_function" "predict_lambda" {
  function_name = "aws_terraform_model_prediction"
  role          = aws_iam_role.predict_lambda_role.arn
  image_uri     = "${aws_ecr_repository.aws_repo.repository_url}:latest"
  package_type  = "Image"
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda_function.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.my_bucket.arn
}


resource "aws_s3_bucket_notification" "my_bucket_notification" {
  bucket = aws_s3_bucket.my_bucket.id

  lambda_function {
    lambda_function_arn         = aws_lambda_function.my_lambda_function.arn
    events                      = ["s3:ObjectCreated:*"]
    filter_prefix               = "aws/data/"
    filter_suffix               = ".csv"
  }
  depends_on = [aws_lambda_permission.allow_bucket]
}



########################
#  Create API Gateway  #
########################

resource "aws_api_gateway_rest_api" "rest_api" {
  name = "aws_lambda"
}

resource "aws_api_gateway_resource" "api_resource" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "/predict"
}

resource "aws_api_gateway_method" "api_method" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.api_resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

# Create integration between lambda function and the API gateway
resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.api_resource.id
  http_method             = aws_api_gateway_method.api_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.predict_lambda.invoke_arn
}


# Allow the API Gateway to talk to the lambda function
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.predict_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.region}:${var.accountId}:${aws_api_gateway_rest_api.rest_api.id}/*/${aws_api_gateway_method.api_method.http_method}${aws_api_gateway_resource.api_resource.path}"
}

resource "aws_api_gateway_deployment" "apigw_deployment" {
  depends_on = [
    aws_api_gateway_integration.integration,
  ]

  rest_api_id = "${aws_api_gateway_rest_api.rest_api.id}"
  stage_name  = "dev"
}