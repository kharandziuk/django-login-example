resource "aws_security_group" "db" {
  name   = "${module.label.id}-db-sg"
  vpc_id = aws_default_vpc.default.id
  tags = {
    Name = "${var.context.stage} db"
  }
}

resource "aws_security_group_rule" "db_from_ebs" {
  type                     = "ingress"
  from_port                = var.db_port
  to_port                  = var.db_port
  protocol                 = "tcp"
  source_security_group_id = module.ecs_fargate.security_group_id
  security_group_id        = aws_security_group.db.id
}



module "rds_instance" {
  source    = "git::https://github.com/cloudposse/terraform-aws-rds.git?ref=tags/0.22.0"
  namespace = var.context.namespace
  stage     = var.context.stage
  name      = "${module.label.id}-db"

  host_name = "${module.label.id}-db"

  security_group_ids = [
    module.ecs_fargate.security_group_id,
    aws_security_group.db.id
  ]

  allowed_cidr_blocks     = [aws_default_vpc.default.cidr_block]
  database_name           = "${module.label.id}-db"
  database_user           = var.db_user
  database_password       = var.db_password
  database_port           = var.db_port
  engine                  = "postgres"
  engine_version          = "10.13"
  instance_class          = var.db_instance_class
  publicly_accessible     = false
  subnet_ids              = aws_default_subnet.defaults.*.id
  vpc_id                  = aws_default_vpc.default.id
  apply_immediately       = true
  maintenance_window      = "Mon:03:00-Mon:04:00"
  skip_final_snapshot     = true
  copy_tags_to_snapshot   = true
  backup_retention_period = 7
  backup_window           = "22:00-03:00"
  allocated_storage       = 5
  db_parameter_group      = "postgres10"
  option_group_name       = "default:postgres-10"
  parameter_group_name    = "default.postgres10"
  db_parameter            = []
  snapshot_identifier     = var.snapshot_identifier

  db_options = []
}
