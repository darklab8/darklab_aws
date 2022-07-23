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

variable AWS_ACCESS_KEY_ID {
  type = string
}
variable AWS_SECRET_ACCESS_KEY {
  type = string
}
variable AWS_REGION {
  type = string
}
variable SSH_PUBLIC_KEY {
  type = string
}

provider "aws" {
  region = local.aws_region
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_lightsail_container_service" "example" {
  name        = "container-service-1"
  power       = "nano"
  scale       = 1
  is_disabled = false

  tags = {
    foo1 = "bar1"
    foo2 = ""
  }
}

resource "aws_lightsail_container_service_deployment_version" "example" {
  container {
    container_name = "hello-world"
    image          = "amazon/amazon-lightsail:hello-world"

    command = []

    environment = {
      MY_ENVIRONMENT_VARIABLE = "my_value"
    }

    ports = {
      80 = "HTTP"
    }
  }

  public_endpoint {
    container_name = "hello-world"
    container_port = 80

    health_check {
      healthy_threshold   = 2
      unhealthy_threshold = 2
      timeout_seconds     = 2
      interval_seconds    = 5
      path                = "/"
      success_codes       = "200-499"
    }
  }

  service_name = aws_lightsail_container_service.example.name
}

output "url" {
  value = aws_lightsail_container_service.example.url
}