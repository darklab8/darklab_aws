output "example_ip" {
  value = aws_instance.web_server.public_ip
}

output "example_id" {
  value = aws_instance.web_server.id
}

output "example_dns" {
  value = aws_instance.web_server.public_dns
}