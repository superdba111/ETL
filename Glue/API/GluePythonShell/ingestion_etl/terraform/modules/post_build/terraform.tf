terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

}


variable "terraform_state_path" {
  type = string
}