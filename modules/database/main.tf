resource random_password password {
  length  = 40
  special = true
  # Use only special chars supported by RDS
  override_special = "!#$%&*()-_=+[]{}<>:?"

  lifecycle {
    ignore_changes = all
  }
}

locals {
  // The database is either a replica (sync) or a clone (async) of
  // another database
  is_cloned_database = var.replicate_source_db != null || var.is_replica
}

resource aws_db_instance database {
  allow_major_version_upgrade     = false
  allocated_storage               = var.storage
  max_allocated_storage           = var.max_storage
  storage_type                    = "gp2"

  engine                          = var.replicate_source_db != null ? null : var.engine
  engine_version                  = var.replicate_source_db != null ? null : var.engine_version
  username                        = var.replicate_source_db != null ? null : var.engine
  password                        = var.replicate_source_db != null ? null : random_password.password.result
  db_name                         = var.replicate_source_db != null ? null : coalesce(var.db_name, var.name)

  instance_class                  = var.instance_class
  identifier                      = "${var.name}-${var.environment}"
  multi_az                        = var.multi_az
  replicate_source_db             = var.replicate_source_db

  vpc_security_group_ids          = [
    aws_security_group.database_sg.id,
  ]

  port                            = var.port
  # db_subnet_group_name            = "main"
  publicly_accessible=true

  lifecycle {
    ignore_changes = [
      name,
      username,
      password,
      maintenance_window,
    ]
  }
  skip_final_snapshot  = true

  backup_window                   = var.backup_window
  maintenance_window              = var.maintenance_window
  performance_insights_enabled    = var.performance_insights_enabled
  parameter_group_name            = coalesce(var.parameter_group_name, "default.${var.engine}${var.engine_version}")
}

module "parameter_group" {
  source               = "./parameter_group"
}


resource "aws_security_group" "database_sg" {
  name = "${var.environment}-database"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}