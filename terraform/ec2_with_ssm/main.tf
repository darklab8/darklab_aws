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

resource "aws_security_group" "web_server_sg" {
  name = "terraform_web_server_sg"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ssm_iam_role" {
  name = "ssm_iam_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_managed_instance_core" {
  role = aws_iam_role.ssm_iam_role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

locals {
  instance_profile_name = "ssm_instance_profile_for_ec2"
}

resource "aws_iam_instance_profile" "iam_instance_profile" {
  name = local.instance_profile_name
  role = aws_iam_role.ssm_iam_role.name
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "web_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web_server_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p "${local.server_port}" &
              EOF

  tags = {
    Name = "terraform_web_server"
  }

  iam_instance_profile = local.instance_profile_name
}

output "ec2_id" {
  value = aws_instance.web_server.id  
}

output "ec2_state" {
  value = aws_instance.web_server.instance_state  
}

output "example_dns" {
  value = aws_instance.web_server.public_dns
}