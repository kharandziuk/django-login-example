terraform {
  backend "s3" {
    bucket = "terraform-max-states"
    key    = "secrets"
    region = "eu-central-1"
  }
}

variable "aws_region" {
  default     = "eu-central-1"
  description = "AWS region"
}

provider "aws" {
  region = var.aws_region
}

variable "s_prefix" {
  default     = "max-testing/dev"
  description = "prefix for secrets"
}


resource "aws_secretsmanager_secret" "admin_pass" {
  name = "${var.s_prefix}/backend/admin_pass"
}

resource "aws_secretsmanager_secret_version" "admin_pass_value" {
  secret_id     = aws_secretsmanager_secret.admin_pass.id
  secret_string = "example-string-to-protect"
}

resource "aws_secretsmanager_secret" "db_pass" {
  name = "${var.s_prefix}/postgres/password"
}

data "aws_secretsmanager_secret_version" "db_pass_value" {
  secret_id  = aws_secretsmanager_secret.db_pass.id
  version_id = aws_secretsmanager_secret_version.db_pass_value.version_id
}

resource "aws_secretsmanager_secret_version" "db_pass_value" {
  secret_id     = aws_secretsmanager_secret.db_pass.id
  secret_string = "secret@pass"
}
