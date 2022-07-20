terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

locals {
  ssh_key_name = "example-key"
  aws_region = var.AWS_REGION
  aws_availability_zone = "${var.AWS_REGION}a"
  server_port = 8080
}

provider "aws" {
  region = local.aws_region
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}


resource "aws_ecr_repository" "example" {
  name                 = "example"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}