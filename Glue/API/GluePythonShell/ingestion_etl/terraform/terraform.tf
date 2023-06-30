
terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source               = "hashicorp/aws"
      configuration_aliases = [aws.environment]
    }

    datadog = {
      source = "DataDog/datadog"
    }
  }

  backend "s3" {
    bucket         = "terraform.shared-services.e.inc"
    key            = "reporting/us-east-1/development/development.tfstate"
    region         = "us-east-1"
    role_arn       = "arn:aws:iam::711182801733:role/Terraform"
    encrypt        = true
  }
}

// Do not use this provider. Exists only to prevent Terraform to ask for default region
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "shared-services"
  region = var.terraform_environment_region

  assume_role {
    role_arn = "arn:aws:iam::711182801733:role/Terraform"
  }
}

provider "aws" {
  alias  = "environment"
  region = var.terraform_environment_region

  assume_role {
    role_arn = var.terraform_environment_iam_role
  }
}

// Environment variables

variable "terraform_environment_name" {
  type = string
}

variable "terraform_environment_iam_role" {
  type = string
}

variable "terraform_environment_region" {
  type = string
}
// Repository variables

variable "terraform_repository_name" {
  type = string
}

variable "terraform_workspace_name" {
  type = string
}

variable "terraform_workspace_branch" {
  type = string
}

variable "terraform_repository_commit_hash" {
  type = string
}

// Container registry

variable "terraform_container_registry" {
  type = string
}

variable "terraform_state_path" {
  type = string
  default = ""
}

variable "container_version" {
  type = string
  default = ""
}

