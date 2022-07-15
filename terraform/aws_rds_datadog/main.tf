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
  aws_region = "us-east-1"
  aws_availability_zone = "us-east-1a"
}


provider "aws" {
  region = local.aws_region
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}


module "database" {
  source               = "../../modules/database"
  name                 = "gill"
  engine               = "postgres"
  environment          = var.environment
  engine_version       = "13"
  storage              = 10
  instance_class       = "db.t3.micro"
  parameter_group_name = "custom-postgres-13"
  multi_az             = var.environment == "production"
  is_replica           = var.environment == "staging"

  # Legacy
  db_name = "postgres"
  # secret  = module.secret
}