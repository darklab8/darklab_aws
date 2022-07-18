# resource aws_db_parameter_group custom_mariadb_10_2 {
#   name        = "custom-mariadb-10-2"
#   family      = "mariadb10.2"
#   description = "Custom MariaDB tailored as a base for all MariaDB RDS"

#   # default sql_mode is STRICT and cause problem
#   parameter {
#     name  = "sql_mode"
#     value = "NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
#   }
# }

# resource aws_db_parameter_group custom_mariadb_10_3 {
#   name        = "custom-mariadb-10-3"
#   family      = "mariadb10.3"
#   description = "Custom MariaDB tailored as a base for all MariaDB RDS"

#   # default sql_mode is STRICT and cause problem
#   parameter {
#     name  = "sql_mode"
#     value = "NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
#   }
# }

# resource aws_db_parameter_group custom_mariadb_10_4 {
#   name        = "custom-mariadb-10-4"
#   family      = "mariadb10.4"
#   description = "Custom MariaDB tailored as a base for all MariaDB RDS"

#   # default sql_mode is STRICT and cause problem
#   parameter {
#     name  = "sql_mode"
#     value = "NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
#   }
# }

# resource aws_db_parameter_group custom_mariadb_10_5 {
#   name        = "custom-mariadb-10-5"
#   family      = "mariadb10.5"
#   description = "Custom MariaDB tailored as a base for all MariaDB RDS"

#   # default sql_mode is STRICT and cause problem
#   parameter {
#     name  = "sql_mode"
#     value = "NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
#   }
# }

# resource aws_db_parameter_group readreplica_postgres_12 {
#   name        = "readreplica-postgres-12"
#   family      = "postgres12"

#   # kill statements after, in ms
#   parameter {
#     name  = "statement_timeout"
#     value = 7 * 60 * 1000
#   }

#   # keep up to 7 min in the past of archived data
#   parameter {
#     name  = "max_standby_archive_delay"
#     value = 7 * 60 * 1000
#   }

#   # keep up to 7 min in the past of archived data
#   parameter {
#     name  = "max_standby_streaming_delay"
#     value = 7 * 60 * 1000
#   }

#   # set the pg_stat_activity.query field, in bytes (log the whole query)
#   parameter {
#     name         = "track_activity_query_size"
#     value        = "4096"
#     apply_method = "pending-reboot"
#   }

#   # log any statement longer than, in ms
#   parameter {
#     name  = "log_min_duration_statement"
#     value = "120000"
#   }

#   # turn off logging of failing statements (which should be handled by the app)
#   parameter {
#     name  = "log_min_error_statement"
#     value = "panic"
#   }
# }

resource aws_db_parameter_group custom_postgres_13 {
  name        = "custom-postgres-13"
  family      = "postgres13"
  description = "Custom Postgres 13 tailored as a base for all postgres RDS"

  # I believe it's settings we have got problem with
  parameter {
    name  = "max_parallel_workers_per_gather"
    value = "0"
  }
  parameter {
    name  = "max_prepared_transactions"
    value = "0"
  }

  # kill statements after, in ms
  parameter {
    name  = "statement_timeout"
    value = 7 * 60 * 1000
  }

  # set the pg_stat_activity.query field, in bytes (log the whole query)
  parameter {
    name         = "track_activity_query_size"
    value        = "4096"
    apply_method = "pending-reboot"
  }

  # log any statement longer than, in ms
  parameter {
    name  = "log_min_duration_statement"
    value = "120000"
  }

  # turn off logging of failing statements (which should be handled by the app)
  parameter {
    name  = "log_min_error_statement"
    value = "panic"
  }

  # DATADOG integration START
  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }

  parameter {
    name  = "track_activity_query_size"
    value = "pg_stat_statements"
  }

  # DATADOG integration END section
}

# resource aws_db_parameter_group custom_postgres_12 {
#   name        = "custom-postgres-12"
#   family      = "postgres12"
#   description = "Custom Postgres 12 tailored as a base for all postgres RDS"

#   # I believe it's settings we have got problem with
#   parameter {
#     name  = "max_parallel_workers_per_gather"
#     value = "0"
#   }
#   parameter {
#     name  = "max_prepared_transactions"
#     value = "0"
#   }

#   # kill statements after, in ms
#   parameter {
#     name  = "statement_timeout"
#     value = 7 * 60 * 1000
#   }

#   # set the pg_stat_activity.query field, in bytes (log the whole query)
#   parameter {
#     name         = "track_activity_query_size"
#     value        = "4096"
#     apply_method = "pending-reboot"
#   }

#   # log any statement longer than, in ms
#   parameter {
#     name  = "log_min_duration_statement"
#     value = "120000"
#   }

#   # turn off logging of failing statements (which should be handled by the app)
#   parameter {
#     name  = "log_min_error_statement"
#     value = "panic"
#   }
# }

# resource aws_db_parameter_group custom_postgres_11 {
#   name        = "custom-postgres-11"
#   family      = "postgres11"
#   description = "Custom Postgres 11 tailored as a base for all postgres RDS"

#   # I believe it's settings we have got problem with
#   parameter {
#     name  = "max_parallel_workers_per_gather"
#     value = "0"
#   }
#   parameter {
#     name  = "max_prepared_transactions"
#     value = "0"
#   }

#   # kill statements after, in ms
#   parameter {
#     name  = "statement_timeout"
#     value = "420000"
#   }

#   # set the pg_stat_activity.query field, in bytes (log the whole query)
#   parameter {
#     name         = "track_activity_query_size"
#     value        = "4096"
#     apply_method = "pending-reboot"
#   }

#   # log any statement longer than, in ms
#   parameter {
#     name  = "log_min_duration_statement"
#     value = "120000"
#   }

#   # turn off logging of failing statements (which should be handled by the app)
#   parameter {
#     name  = "log_min_error_statement"
#     value = "panic"
#   }
# }
