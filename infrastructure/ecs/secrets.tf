locals {
  s_prefix = "dev_max2"
}
resource "aws_secretsmanager_secret" "admin_pass" {
  name = "${local.s_prefix}/backend/admin_pass"
}

resource "aws_secretsmanager_secret_version" "admin_pass_value" {
  secret_id     = aws_secretsmanager_secret.admin_pass.id
  secret_string = "example-string-to-protect"
}

resource "aws_secretsmanager_secret" "db_pass" {
  name = "${local.s_prefix}/postgres/password"
}

data "aws_secretsmanager_secret_version" "db_pass_value" {
  secret_id  = aws_secretsmanager_secret.db_pass.id
  version_id = aws_secretsmanager_secret_version.db_pass_value.version_id
}

resource "aws_secretsmanager_secret_version" "db_pass_value" {
  secret_id     = aws_secretsmanager_secret.db_pass.id
  secret_string = "secret@pass"
}
