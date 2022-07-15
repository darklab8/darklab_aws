output "database_address" {
  value = module.database.database.address
  depends_on = [
    module.database
  ]
}

output "database_id" {
  value = module.database.database.id
  depends_on = [
    module.database
  ]
}

output "database_password" {
  value = module.database.database.password
  depends_on = [
    module.database
  ]
  sensitive = true
}