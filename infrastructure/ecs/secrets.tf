resource "aws_secretsmanager_secret" "admin_pass" {
  name = "dev_max/backend/admin_pass"
}

resource "aws_secretsmanager_secret_version" "admin_pass_value" {
  secret_id     = aws_secretsmanager_secret.admin_pass.id
  secret_string = "example-string-to-protect"
}
