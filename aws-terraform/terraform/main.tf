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
    filter_prefix               = "/aws/data/"
    filter_suffix               = ".csv"
  }
  depends_on = [aws_lambda_permission.allow_bucket]
}
