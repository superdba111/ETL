variable "create" {
  default = true
}

variable "name" {}

variable "netsuite_jobs" {}

variable "dayforce_jobs" {}

variable "zoho_crm_jobs" {}

variable "organization" {}

variable "environment" {}

variable "workspace_branch" {}

variable "tags" {
}

variable "type" {}

variable "schedule_zoho" {}

variable "enabled" {
  default = true
}

variable "description" {
  default = ""
}

variable "job_name" {}

variable "arguments" {
  type    = map(string)
  default = {}
}

variable "timeout" {
  default = 2880
}