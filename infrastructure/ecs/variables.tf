
variable "context" {
  type = object({
    namespace           = string
    stage               = string
    tags                = map(string)
  })
  default = {
    namespace = "max"
    stage = "dev"
    tags = {}
  }
}

module "label" {
  source     = "git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.22.1"
  namespace = "max"
  stage = "dev"
  tags = {}
}

variable "db_instance_class" {
  default     = "db.t3.micro"
}

variable "db_user" {
  default = "user"
  description = "Name of the user to be created in the database"
}

variable "db_password" {
  default = "to-change"
  description = "Your database password"
}

variable "db_port" {
  default     = 5432
  description = "The port your database is running on"
}

variable "snapshot_identifier" {
  default = ""
}
