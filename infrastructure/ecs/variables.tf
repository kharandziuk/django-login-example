
module "label" {
  source    = "git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.22.1"
  namespace = "max"
  stage     = "dev"
  name      = "test"
  tags      = {}
}

variable "db_instance_class" {
  default = "db.t3.micro"
}

variable "db_password" {
  default     = "to-change"
  description = "Your database password"
}

variable "db_port" {
  default     = 5432
  description = "The port your database is running on"
}

variable "snapshot_identifier" {
  default = ""
}
