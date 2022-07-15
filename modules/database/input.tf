variable name {
  type = string
  description = "The name of the databse, by default it is generated from the service name"
}
variable db_name {
  type = string
  default = null
  description = "The name to use for the database.name attribute, 99% of time it defaults to 'name', but in production pyvar is named boby for bad historical reason"
}

variable multi_az {
  type = bool
  default = true
  description = "Replicate the database in mulitple availability zones"
}

variable engine {
  type = string
  description = "The engine of the database (postgres|mysql|mariadb)"
}
variable port {
  description = "The TCP port on which the database listens"
  default = null
}
variable backup_window {
  type = string
  default = "03:00-04:00"
  description = "The time range for the backup"
}
variable maintenance_window {
  type = string
  default = "tue:04:00-tue:05:00"
  description = "The time range for the maintenance"
}
variable performance_insights_enabled {
  type = bool
  default = false
  description = "Enable performance logs"
}

variable rotation_enabled {
  type = bool
  default = false
  description = "Enable rotation of the secret"
}

variable storage {
  type = number
  default = null
  description = "Size of the storage"
}
variable max_storage {
  type = number
  default = null
  description = "Maximum size of the storage when autoscale is enabled"
}

variable engine_version {
  type = string
  description = "Version of the database engine"
}

variable instance_class {
  type = string
  default = null
  description = "Class of the instance (for example db.t3, db.m1)"
}

variable environment {
  type = string
  description = "The level of the service (staging, production)"
}

variable parameter_group_name {
  type = string
  default = null
  description = "The name of the parameter group for the database"
}

variable replicate_source_db {
  type = string
  default = null
  description = "The name of the DB this one replicates"
}
# variable secret {
#   default = null
#   type = object({
#     application_secret_arn=string,
#     master_secret_arn=string,
#   })
# }
variable is_replica {
  type = bool
  default = false
  description = "The database is a offline replication"
}
