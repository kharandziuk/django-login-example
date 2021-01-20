terraform {
  required_providers {
    aws = {
      source  = "-/aws"
      version = "< 3.0"
    }
  }
}

variable "aws_region" {
  default = "eu-central-1"
  type    = string
}

variable "backend_service_name" {
  type = string
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "backend" {
  name                 = var.backend_service_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "backend_repo_url" {
  value = aws_ecr_repository.backend.repository_url
}
