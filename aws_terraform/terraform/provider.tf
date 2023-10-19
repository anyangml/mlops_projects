provider "aws" {
  region = "us-west-2"
}

# get authorization credentials to push to ecr
data "aws_ecr_authorization_token" "token" {}

# configure docker provider
provider "docker" {
  registry_auth {
      address = data.aws_ecr_authorization_token.token.proxy_endpoint
      username = data.aws_ecr_authorization_token.token.user_name
      password  = data.aws_ecr_authorization_token.token.password
    }
}