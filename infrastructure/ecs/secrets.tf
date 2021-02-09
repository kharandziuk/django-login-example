variable "s_prefix" {
  default     = "max-testing/dev"
  description = "prefix for secrets"
}

data "aws_secretsmanager_secret" "admin_pass" {
  name = "${var.s_prefix}/backend/admin_pass"
}

data "aws_secretsmanager_secret" "db_pass" {
  name = "${var.s_prefix}/postgres/password"
}
