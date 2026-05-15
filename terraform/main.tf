terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ECR Repository for Docker Images
resource "aws_ecr_repository" "devops_app_repo" {
  name                 = "devops-pipeline-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Security Group for the Application
resource "aws_security_group" "app_sg" {
  name        = "devops_app_sg"
  description = "Allow HTTP inbound traffic"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance for deploying the app (Example)
resource "aws_instance" "app_server" {
  ami           = "ami-0c7217cdde317cfec" # Example Ubuntu 22.04 LTS AMI in us-east-1
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              EOF

  tags = {
    Name = "DevOps-Pipeline-Server"
  }
}
