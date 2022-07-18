variable AWS_ACCESS_KEY_ID {
  type = string
}
variable AWS_SECRET_ACCESS_KEY {
  type = string
}
variable AWS_REGION {
  type = string
}

variable SSH_PUBLIC_KEY {
  type = string
}

variable DATABASE_PASSWORD {
  type = string
}

variable environment {
  type = string
  default="staging"
}